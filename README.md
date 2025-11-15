# MicroJob - Freelance Marketplace Platform

A modern, Fiverr-like freelance marketplace platform built with Flask, where employers can post jobs and workers can bid on them. Features AI-powered learning paths and professional job-oriented training courses to help workers build skills before taking on jobs.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Features
- **Job Posting & Bidding System** - Employers post jobs, workers place competitive bids
- **14 Job Categories** - Organized into Online and Offline jobs with structured categories
- **User Profiles** - Public profiles with ratings, reviews, skills, and portfolio
- **Advanced Search & Filters** - Search by keywords, category, difficulty, mode, and budget
- **Reviews & Ratings** - 5-star rating system with comments after job completion
- **Messaging System** - Real-time messaging between employers and workers
- **Dashboard** - Separate dashboards for employers and workers
- **AI Learning Paths** - Personalized learning resources for workers to build skills
- **Professional Courses** - Job-oriented training and certifications from leading companies
- **Modern UI** - Beautiful dark theme with responsive design

### Job Categories

#### Online Jobs
- **IT & Programming** - Web development, software, IT support
- **Graphic & Design** - Logo design, UI/UX, graphics
- **Writing & Translation** - Content writing, translation services
- **Marketing & SMM** - Social media, digital marketing, SEO
- **Education & Tutoring** - Online tutoring, teaching
- **Virtual Assistant** - Administrative tasks, data entry
- **Data / AI Tasks** - Data analysis, AI projects

#### Offline Jobs
- **Delivery** - Food delivery, package delivery
- **Home & Repair Services** - Plumbing, electrical, painting
- **Event & Photography** - Event planning, photography
- **Construction & Labor** - Construction work, manual labor
- **Agriculture** - Farming, harvesting
- **Transportation** - Driving, moving services

### User Roles
- **Employers** - Post jobs, review bids, accept workers, manage projects
- **Workers** - Browse jobs, place bids, complete tasks, build reputation

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MicroJob.git
   cd MicroJob
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   flask init-db
   ```
   This will create the database with demo data including:
   - Demo employer account (email: `employer@example.com`, password: `123`)
   - Demo worker account (email: `worker@example.com`, password: `123`)
   - 22 sample jobs across all categories

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
MicroJob/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── instance/
│   └── microjob.db      # SQLite database (created automatically)
├── static/
│   └── style.css        # CSS styles with modern dark theme
└── templates/
    ├── base.html        # Base template with logo and navigation
    ├── index.html       # Job listing page with filters
    ├── task_detail.html # Job detail page
    ├── new_task.html    # Post job page with category selection
    ├── profile.html     # User profile page
    ├── edit_profile.html # Edit profile page
    ├── dashboard_employer.html # Employer dashboard
    ├── dashboard_worker.html   # Worker dashboard
    ├── messages.html    # Messages list
    ├── conversation.html # Chat interface
    ├── add_review.html  # Review form
    ├── learn.html       # AI learning path page
    ├── courses.html     # Professional courses and certifications
    ├── login.html       # Login page
    └── register.html    # Registration page
```

## 🎯 Usage Guide

### For Employers

1. **Register/Login** - Create an account and select "Employer" role
2. **Post a Job** - Click "Post Job" and:
   - Select from 14 predefined categories
   - Mode (Online/Offline) is automatically set based on category
   - Set budget, difficulty level, and required skills
3. **Review Bids** - View and accept bids from workers
4. **Manage Jobs** - Track job progress in your dashboard
5. **Complete & Review** - Mark jobs as complete and leave reviews

### For Workers

1. **Register/Login** - Create an account and select "Worker" role
2. **Browse Jobs** - Search and filter available jobs by category, mode, difficulty
3. **Learn with AI** - Click "🤖 Learn with AI" to get personalized learning resources
4. **Take Courses** - Browse professional training courses and certifications
5. **Place Bids** - Submit competitive bids with proposals
6. **Complete Tasks** - Work on assigned jobs and deliver results
7. **Build Reputation** - Earn reviews and ratings

## 📚 Professional Courses & Certifications

The platform includes a comprehensive courses section featuring job-oriented training from leading companies:

- **IT & Programming** - Meta Front-End Developer, Google IT Support, AWS Cloud
- **Graphic & Design** - Google UX Design, Adobe Certified Professional
- **Writing & Translation** - Professional Writing, Content Marketing
- **Marketing & SMM** - Meta Social Media Marketing, Google Digital Marketing, HubSpot Certifications
- **Education & Tutoring** - TEFL Certification, Online Tutoring Best Practices
- **Virtual Assistant** - Excel Skills, Virtual Assistant Training
- **Data / AI Tasks** - IBM Data Science, AI Fundamentals

All courses include:
- Industry-recognized certifications
- Professional providers (Coursera, Google, Meta, HubSpot, etc.)
- Clear learning paths and topics
- Duration estimates

## 🤖 AI Learning Feature

The platform includes an AI-powered learning system that:
- Analyzes job requirements
- Generates personalized learning paths
- Provides multiple resources (videos, articles, tutorials)
- Offers pro tips specific to each job type
- Estimates learning time

Access it by clicking the "🤖 Learn with AI" button on any job page.

## 🎨 Design & Branding

- **Modern Logo** - Professional gradient logo with "MICRO JOB" branding
- **Tagline** - "ÖYRƏN, TƏTBİQ ET, QAZAN." (Learn, Apply, Earn)
- **Dark Theme** - Beautiful dark mode with gradient accents
- **Responsive Design** - Works on desktop, tablet, and mobile devices

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.2
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3 (Modern dark theme with gradients)
- **Authentication**: Flask sessions with password hashing (Werkzeug)

## 📊 Database Models

- **User** - User accounts (employers/workers) with profiles, skills, bio, location
- **Task** - Job postings with category, mode, budget, difficulty, status
- **Bid** - Worker bids on jobs with amount and proposal
- **Review** - Ratings and reviews between users
- **Message** - User messages with read/unread status

## 🔧 Configuration

The application uses default configuration. To customize:

- **Database**: Edit `SQLALCHEMY_DATABASE_URI` in `app.py`
- **Secret Key**: Change `SECRET_KEY` in `app.py` for production

## 📦 Sample Data

The `flask init-db` command creates:
- 2 demo user accounts (employer and worker)
- 22 sample jobs covering all categories:
  - 14 online jobs (IT, Design, Writing, Marketing, etc.)
  - 8 offline jobs (Delivery, Repair, Events, Construction, etc.)

## 🚧 Future Enhancements

- [ ] Payment integration
- [ ] File uploads for job deliverables
- [ ] Email notifications
- [ ] Advanced AI recommendations
- [ ] Portfolio uploads
- [ ] Real-time notifications
- [ ] Mobile app
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Fiverr for design inspiration
- Leading course providers (Coursera, Google, Meta, HubSpot, etc.)
- All contributors and users

---

**Made with ❤️ for freelancers and employers**

**ÖYRƏN, TƏTBİQ ET, QAZAN.** (Learn, Apply, Earn)
