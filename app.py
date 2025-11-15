from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import markupsafe

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'
db_path = os.path.join(basedir, 'instance', 'microjob.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.template_filter('nl2br')
def nl2br_filter(value):
    """Convert newlines to <br> tags"""
    if value:
        return markupsafe.Markup(value.replace('\n', '<br>\n'))
    return value

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    skills = db.Column(db.String(200))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(200))
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks_posted = db.relationship('Task', backref='employer', foreign_keys='Task.employer_id')
    tasks_taken  = db.relationship('Task', backref='worker', foreign_keys='Task.worker_id')
    bids = db.relationship('Bid', backref='worker', lazy=True)
    reviews_received = db.relationship('Review', backref='reviewee', foreign_keys='Review.reviewee_id')
    reviews_given = db.relationship('Review', backref='reviewer', foreign_keys='Review.reviewer_id')
    sent_messages = db.relationship('Message', backref='sender', foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', backref='receiver', foreign_keys='Message.receiver_id')

    def average_rating(self):
        """Calculate average rating for workers"""
        if self.role != 'worker' or not self.reviews_received:
            return 0.0
        ratings = [r.rating for r in self.reviews_received if r.rating]
        return sum(ratings) / len(ratings) if ratings else 0.0

    def total_reviews(self):
        """Get total number of reviews"""
        return len(self.reviews_received) if self.reviews_received else 0


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget_azn = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(120))
    mode = db.Column(db.String(20))
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    required_skill = db.Column(db.String(120))
    difficulty = db.Column(db.String(20))

    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    worker_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    accepted_bid_id = db.Column(db.Integer, db.ForeignKey('bid.id'), nullable=True)

    bids = db.relationship('Bid', primaryjoin='Task.id == Bid.task_id', backref='task', lazy=True, cascade='all, delete-orphan')
    accepted_bid = db.relationship('Bid', foreign_keys=[accepted_bid_id], uselist=False, post_update=True)
    reviews = db.relationship('Review', backref='task', lazy=True)


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    proposal = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


def ai_learning_path(task: Task):
    """AI-powered learning path generator based on task requirements."""
    skill = (task.required_skill or task.category or '').lower()
    difficulty = task.difficulty.lower()
    category = (task.category or '').lower()

    learning_paths = {
        'social media': {
            'title': 'Social Media Marketing Mastery',
            'description': 'Learn how to create engaging social media content, understand platform algorithms, and grow your audience.',
            'resources': [
                {'type': 'Video Course', 'title': 'Social Media Marketing Basics', 'url': 'https://www.youtube.com/results?search_query=social+media+marketing+basics', 'duration': '2 hours'},
                {'type': 'Tool Tutorial', 'title': 'Canva for Social Media Design', 'url': 'https://www.youtube.com/results?search_query=canva+social+media+design', 'duration': '1 hour'},
                {'type': 'Article', 'title': 'Best Practices for Instagram Posts', 'url': 'https://www.google.com/search?q=instagram+post+best+practices', 'duration': '30 min'}
            ],
            'tips': [
                'Use high-quality images (at least 1080x1080px for Instagram)',
                'Write engaging captions with relevant hashtags',
                'Post consistently to maintain audience engagement',
                'Analyze your posts to see what works best'
            ],
            'estimated_time': '3-4 hours'
        },
        'design': {
            'title': 'Graphic Design Fundamentals',
            'description': 'Master the basics of graphic design, learn to use design tools, and create professional visuals.',
            'resources': [
                {'type': 'Video Course', 'title': 'Canva for Beginners', 'url': 'https://www.youtube.com/results?search_query=canva+for+beginners', 'duration': '1.5 hours'},
                {'type': 'Video Course', 'title': 'Design Principles & Color Theory', 'url': 'https://www.youtube.com/results?search_query=design+principles+color+theory', 'duration': '1 hour'},
                {'type': 'Tool Tutorial', 'title': 'Creating Professional Posters', 'url': 'https://www.youtube.com/results?search_query=how+to+create+posters', 'duration': '45 min'}
            ],
            'tips': [
                'Keep designs simple and focused',
                'Use contrasting colors for readability',
                'Maintain consistent fonts and styles',
                'Leave white space for better visual balance'
            ],
            'estimated_time': '3-4 hours'
        },
        'translation': {
            'title': 'Professional Translation Skills',
            'description': 'Learn translation techniques, understand context, and deliver accurate translations.',
            'resources': [
                {'type': 'Video Course', 'title': 'Translation Best Practices', 'url': 'https://www.youtube.com/results?search_query=translation+best+practices', 'duration': '1.5 hours'},
                {'type': 'Article', 'title': 'Common Translation Mistakes to Avoid', 'url': 'https://www.google.com/search?q=translation+mistakes+avoid', 'duration': '30 min'},
                {'type': 'Tool Tutorial', 'title': 'Using Translation Tools Effectively', 'url': 'https://www.youtube.com/results?search_query=translation+tools+tutorial', 'duration': '1 hour'}
            ],
            'tips': [
                'Always translate meaning, not just words',
                'Consider cultural context and idioms',
                'Proofread your translations carefully',
                'Maintain the original tone and style'
            ],
            'estimated_time': '3 hours'
        },
        'data entry': {
            'title': 'Data Entry & Excel Mastery',
            'description': 'Learn efficient data entry techniques and master Excel/Google Sheets for professional work.',
            'resources': [
                {'type': 'Video Course', 'title': 'Excel Basics for Beginners', 'url': 'https://www.youtube.com/results?search_query=excel+for+beginners', 'duration': '2 hours'},
                {'type': 'Video Course', 'title': 'Google Sheets Tutorial', 'url': 'https://www.youtube.com/results?search_query=google+sheets+tutorial', 'duration': '1.5 hours'},
                {'type': 'Article', 'title': 'Data Entry Speed Tips', 'url': 'https://www.google.com/search?q=data+entry+speed+tips', 'duration': '20 min'}
            ],
            'tips': [
                'Use keyboard shortcuts to work faster',
                'Double-check data for accuracy',
                'Organize data in clear columns and rows',
                'Use formulas to automate calculations'
            ],
            'estimated_time': '3-4 hours'
        },
        'writing': {
            'title': 'Professional Writing Skills',
            'description': 'Improve your writing skills, learn to write engaging content, and master different writing styles.',
            'resources': [
                {'type': 'Video Course', 'title': 'Content Writing Fundamentals', 'url': 'https://www.youtube.com/results?search_query=content+writing+fundamentals', 'duration': '2 hours'},
                {'type': 'Article', 'title': 'Grammar and Style Guide', 'url': 'https://www.google.com/search?q=grammar+style+guide', 'duration': '45 min'},
                {'type': 'Tool Tutorial', 'title': 'Writing Tools and Resources', 'url': 'https://www.youtube.com/results?search_query=writing+tools', 'duration': '1 hour'}
            ],
            'tips': [
                'Write clear and concise sentences',
                'Proofread your work before submitting',
                'Use active voice when possible',
                'Structure your content with headings'
            ],
            'estimated_time': '3-4 hours'
        },
        'programming': {
            'title': 'Programming Basics',
            'description': 'Learn programming fundamentals and start building your coding skills.',
            'resources': [
                {'type': 'Video Course', 'title': 'Programming for Beginners', 'url': 'https://www.youtube.com/results?search_query=programming+for+beginners', 'duration': '3 hours'},
                {'type': 'Article', 'title': 'Programming Best Practices', 'url': 'https://www.google.com/search?q=programming+best+practices', 'duration': '30 min'}
            ],
            'tips': [
                'Start with simple projects',
                'Practice coding daily',
                'Read and understand error messages',
                'Use version control (Git)'
            ],
            'estimated_time': '4-5 hours'
        }
    }
    
    for key, path in learning_paths.items():
        if key in skill or key in category:
            return path
    
    return {
        'title': 'Digital Skills Development',
        'description': 'Build essential digital skills to succeed in the modern workplace.',
        'resources': [
            {'type': 'Video Course', 'title': 'Digital Skills for Beginners', 'url': 'https://www.youtube.com/results?search_query=digital+skills+for+beginners', 'duration': '2 hours'},
            {'type': 'Article', 'title': 'Freelancing Tips and Tricks', 'url': 'https://www.google.com/search?q=freelancing+tips', 'duration': '30 min'}
        ],
        'tips': [
            'Start with the basics and build gradually',
            'Practice regularly to improve your skills',
            'Seek feedback from experienced professionals',
            'Stay updated with industry trends'
        ],
        'estimated_time': '2-3 hours'
    }


@app.route('/')
def index():
    search = request.args.get('search', '').strip()
    filter_mode = request.args.get('mode', 'all')
    category = request.args.get('category', 'all')
    min_budget = request.args.get('min_budget', type=float)
    max_budget = request.args.get('max_budget', type=float)
    difficulty = request.args.get('difficulty', 'all')
    
    q = Task.query.filter(Task.status == 'open')

    if search:
        q = q.filter(
            (Task.title.contains(search)) |
            (Task.description.contains(search)) |
            (Task.category.contains(search))
        )

    if filter_mode == 'online':
        q = q.filter(Task.mode == 'online')
    elif filter_mode == 'offline':
        q = q.filter(Task.mode == 'offline')

    if category != 'all' and category:
        q = q.filter(Task.category == category)

    if min_budget:
        q = q.filter(Task.budget_azn >= min_budget)
    if max_budget:
        q = q.filter(Task.budget_azn <= max_budget)

    if difficulty != 'all' and difficulty:
        q = q.filter(Task.difficulty == difficulty)

    tasks = q.order_by(Task.id.desc()).all()
    user = current_user()
    
    categories = db.session.query(Task.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('index.html', tasks=tasks, user=user, filter_mode=filter_mode,
                         search=search, category=category, categories=categories, 
                         min_budget=min_budget, max_budget=max_budget, difficulty=difficulty)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].lower()
        password = request.form['password']
        role = request.form['role']
        skills = request.form.get('skills', '')

        if User.query.filter_by(email=email).first():
            flash('Email already registered, please log in.', 'error')
            return redirect(url_for('login'))

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            skills=skills
        )
        db.session.add(user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Wrong email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    user = current_user()
    if not user or user.role != 'employer':
        flash('Only employers can post tasks.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        budget = float(request.form['budget'])
        category = request.form.get('category', '')
        mode = request.form.get('mode', 'online')
        required_skill = request.form.get('required_skill', '')
        difficulty = request.form.get('difficulty', 'beginner')

        task = Task(
            title=title,
            description=description,
            budget_azn=budget,
            category=category,
            mode=mode,
            required_skill=required_skill,
            difficulty=difficulty,
            employer_id=user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created!', 'success')
        return redirect(url_for('index'))

    return render_template('new_task.html', user=user)


@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    user = current_user()
    
    bids = Bid.query.filter_by(task_id=task_id).order_by(Bid.amount.asc()).all()
    
    user_bid = None
    if user and user.role == 'worker':
        user_bid = Bid.query.filter_by(task_id=task_id, worker_id=user.id).first()
    
    return render_template('task_detail.html', task=task, user=user, bids=bids, user_bid=user_bid)


@app.route('/task/<int:task_id>/bid', methods=['POST'])
def place_bid(task_id):
    user = current_user()
    if not user or user.role != 'worker':
        flash('You must be logged in as a worker to place bids.', 'error')
        return redirect(url_for('login'))

    task = Task.query.get_or_404(task_id)
    if task.status != 'open':
        flash('Task is no longer accepting bids.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    existing_bid = Bid.query.filter_by(task_id=task_id, worker_id=user.id).first()
    if existing_bid:
        flash('You have already placed a bid on this task.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    amount = float(request.form.get('amount', 0))
    proposal = request.form.get('proposal', '')

    if amount <= 0:
        flash('Bid amount must be greater than 0.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    bid = Bid(
        task_id=task_id,
        worker_id=user.id,
        amount=amount,
        proposal=proposal
    )
    db.session.add(bid)
    db.session.commit()
    flash('Your bid has been placed successfully!', 'success')
    return redirect(url_for('task_detail', task_id=task_id))


@app.route('/task/<int:task_id>/accept_bid/<int:bid_id>', methods=['POST'])
def accept_bid(task_id, bid_id):
    user = current_user()
    task = Task.query.get_or_404(task_id)
    
    if not user or user.id != task.employer_id:
        flash('Only the task owner can accept bids.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    bid = Bid.query.get_or_404(bid_id)
    if bid.task_id != task_id:
        flash('Invalid bid.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    Bid.query.filter_by(task_id=task_id).filter(Bid.id != bid_id).update({'status': 'rejected'})
    
    bid.status = 'accepted'
    task.status = 'assigned'
    task.worker_id = bid.worker_id
    task.accepted_bid_id = bid_id
    
    db.session.commit()
    flash(f'Bid accepted! {bid.worker.name} has been assigned to this task.', 'success')
    return redirect(url_for('task_detail', task_id=task_id))


@app.route('/task/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    user = current_user()
    task = Task.query.get_or_404(task_id)
    
    if not user or user.id != task.employer_id:
        flash('Only the task owner can mark tasks as complete.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    if task.status != 'assigned':
        flash('Task must be assigned before completion.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    task.status = 'completed'
    db.session.commit()
    flash('Task marked as completed! You can now leave a review.', 'success')
    return redirect(url_for('task_detail', task_id=task_id))


@app.route('/learn/<int:task_id>')
def learn(task_id):
    task = Task.query.get_or_404(task_id)
    learning_path = ai_learning_path(task)
    user = current_user()
    return render_template('learn.html', task=task, learning_path=learning_path, user=user)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    profile_user = User.query.get_or_404(user_id)
    user = current_user()
    
    if profile_user.role == 'employer':
        tasks = Task.query.filter_by(employer_id=user_id).order_by(Task.created_at.desc()).limit(10).all()
    else:
        tasks = Task.query.filter_by(worker_id=user_id).order_by(Task.created_at.desc()).limit(10).all()
    
    reviews = Review.query.filter_by(reviewee_id=user_id).order_by(Review.created_at.desc()).all()
    
    return render_template('profile.html', profile_user=profile_user, user=user, tasks=tasks, reviews=reviews)


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    user = current_user()
    if not user:
        flash('Please log in to edit your profile.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        user.name = request.form.get('name', user.name)
        user.bio = request.form.get('bio', '')
        user.location = request.form.get('location', '')
        user.skills = request.form.get('skills', '')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile', user_id=user.id))

    return render_template('edit_profile.html', user=user)


@app.route('/task/<int:task_id>/review', methods=['GET', 'POST'])
def add_review(task_id):
    user = current_user()
    if not user:
        flash('Please log in to leave a review.', 'error')
        return redirect(url_for('login'))

    task = Task.query.get_or_404(task_id)
    
    if task.status != 'completed':
        flash('Task must be completed before leaving a review.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    if user.id == task.employer_id:
        reviewee_id = task.worker_id
    elif user.id == task.worker_id:
        reviewee_id = task.employer_id
    else:
        flash('You can only review tasks you are involved in.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    existing_review = Review.query.filter_by(
        task_id=task_id,
        reviewer_id=user.id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this task.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    if request.method == 'POST':
        rating = int(request.form.get('rating', 5))
        comment = request.form.get('comment', '')

        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5.', 'error')
            return redirect(url_for('add_review', task_id=task_id))

        review = Review(
            task_id=task_id,
            reviewer_id=user.id,
            reviewee_id=reviewee_id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)
        db.session.commit()
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('task_detail', task_id=task_id))

    reviewee = User.query.get(reviewee_id)
    return render_template('add_review.html', task=task, user=user, reviewee=reviewee)


@app.route('/messages')
def messages():
    user = current_user()
    if not user:
        flash('Please log in to view messages.', 'error')
        return redirect(url_for('login'))

    sent_to = db.session.query(Message.receiver_id).filter_by(sender_id=user.id).distinct()
    received_from = db.session.query(Message.sender_id).filter_by(receiver_id=user.id).distinct()
    
    conversation_partners = set()
    for partner_id in sent_to:
        conversation_partners.add(partner_id[0])
    for partner_id in received_from:
        conversation_partners.add(partner_id[0])
    
    conversations = []
    for partner_id in conversation_partners:
        partner = User.query.get(partner_id)
        last_message = Message.query.filter(
            ((Message.sender_id == user.id) & (Message.receiver_id == partner_id)) |
            ((Message.sender_id == partner_id) & (Message.receiver_id == user.id))
        ).order_by(Message.created_at.desc()).first()
        
        unread_count = Message.query.filter_by(
            sender_id=partner_id,
            receiver_id=user.id,
            is_read=False
        ).count()
        
        conversations.append({
            'partner': partner,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else datetime.min, reverse=True)
    
    return render_template('messages.html', user=user, conversations=conversations)


@app.route('/messages/<int:partner_id>', methods=['GET', 'POST'])
def conversation(partner_id):
    user = current_user()
    if not user:
        flash('Please log in to view messages.', 'error')
        return redirect(url_for('login'))

    partner = User.query.get_or_404(partner_id)
    
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        task_id = request.form.get('task_id', type=int)
        
        if content:
            message = Message(
                sender_id=user.id,
                receiver_id=partner_id,
                task_id=task_id if task_id else None,
                content=content
            )
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('conversation', partner_id=partner_id))

    Message.query.filter_by(
        sender_id=partner_id,
        receiver_id=user.id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()

    messages = Message.query.filter(
        ((Message.sender_id == user.id) & (Message.receiver_id == partner_id)) |
        ((Message.sender_id == partner_id) & (Message.receiver_id == user.id))
    ).order_by(Message.created_at.asc()).all()

    return render_template('conversation.html', user=user, partner=partner, messages=messages)


@app.route('/dashboard')
def dashboard():
    user = current_user()
    if not user:
        flash('Please log in to view your dashboard.', 'error')
        return redirect(url_for('login'))

    if user.role == 'employer':
        posted_tasks = Task.query.filter_by(employer_id=user.id).order_by(Task.created_at.desc()).all()
        return render_template('dashboard_employer.html', user=user, tasks=posted_tasks)
    else:
        my_bids = Bid.query.filter_by(worker_id=user.id).order_by(Bid.created_at.desc()).all()
        assigned_tasks = Task.query.filter_by(worker_id=user.id, status='assigned').all()
        completed_tasks = Task.query.filter_by(worker_id=user.id, status='completed').all()
        return render_template('dashboard_worker.html', user=user, bids=my_bids, 
                             assigned_tasks=assigned_tasks, completed_tasks=completed_tasks)


@app.cli.command('init-db')
def init_db():
    """Create tables and add demo data. Run: flask init-db"""
    db.drop_all()
    db.create_all()

    employer = User(
        name='Demo Employer',
        email='employer@example.com',
        password_hash=generate_password_hash('123'),
        role='employer',
        skills='project management'
    )
    worker = User(
        name='Demo Worker',
        email='worker@example.com',
        password_hash=generate_password_hash('123'),
        role='worker',
        skills='social media, design'
    )

    db.session.add(employer)
    db.session.add(worker)
    db.session.commit()

    t1 = Task(
        title='Create 3 Instagram posts for local café',
        description='We need 3 simple posts (photo + text) for Instagram in Azerbaijani.',
        budget_azn=15,
        category='Social media',
        mode='online',
        required_skill='social media, canva, design',
        difficulty='beginner',
        employer_id=employer.id
    )
    t2 = Task(
        title='Translate 2 pages EN → AZ',
        description='Simple text, not technical. Around 600–800 words.',
        budget_azn=20,
        category='Translation',
        mode='online',
        required_skill='translation, english, azerbaijani',
        difficulty='intermediate',
        employer_id=employer.id
    )
    t3 = Task(
        title='Help at offline event (2 hours)',
        description='Assist with registration and photos at a youth event in Baku.',
        budget_azn=25,
        category='Event support',
        mode='offline',
        required_skill='communication',
        difficulty='beginner',
        employer_id=employer.id
    )

    db.session.add_all([t1, t2, t3])
    db.session.commit()
    print("Database initialized with demo data.")


if __name__ == '__main__':
    instance_dir = os.path.join(basedir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
