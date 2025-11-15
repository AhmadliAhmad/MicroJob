# MicroJob - Freelance Marketplace Platform

A modern, Fiverr-like freelance marketplace platform built with Flask, where employers can post jobs and workers can bid on them. Features AI-powered learning paths to help workers build skills before taking on jobs.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Features
- **Job Posting & Bidding System** - Employers post jobs, workers place competitive bids
- **User Profiles** - Public profiles with ratings, reviews, skills, and portfolio
- **Search & Filters** - Advanced search by keywords, category, difficulty, mode, and budget
- **Reviews & Ratings** - 5-star rating system with comments after job completion
- **Messaging System** - Real-time messaging between employers and workers
- **Dashboard** - Separate dashboards for employers and workers
- **AI Learning Paths** - Personalized learning resources for workers to build skills

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
   - Sample jobs

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
│   └── style.css        # CSS styles
└── templates/
    ├── base.html        # Base template
    ├── index.html       # Job listing page
    ├── task_detail.html # Job detail page
    ├── new_task.html    # Post job page
    ├── profile.html     # User profile page
    ├── edit_profile.html # Edit profile page
    ├── dashboard_employer.html # Employer dashboard
    ├── dashboard_worker.html   # Worker dashboard
    ├── messages.html    # Messages list
    ├── conversation.html # Chat interface
    ├── add_review.html  # Review form
    ├── learn.html       # AI learning path page
    ├── login.html       # Login page
    └── register.html    # Registration page
```

## 🎯 Usage Guide

### For Employers

1. **Register/Login** - Create an account and select "Employer" role
2. **Post a Job** - Click "Post Job" and fill in job details
3. **Review Bids** - View and accept bids from workers
4. **Manage Jobs** - Track job progress in your dashboard
5. **Complete & Review** - Mark jobs as complete and leave reviews

### For Workers

1. **Register/Login** - Create an account and select "Worker" role
2. **Browse Jobs** - Search and filter available jobs
3. **Learn with AI** - Click "🤖 Learn with AI" to get personalized learning resources
4. **Place Bids** - Submit competitive bids with proposals
5. **Complete Tasks** - Work on assigned jobs and deliver results
6. **Build Reputation** - Earn reviews and ratings

## 🤖 AI Learning Feature

The platform includes an AI-powered learning system that:
- Analyzes job requirements
- Generates personalized learning paths
- Provides multiple resources (videos, articles, tutorials)
- Offers pro tips specific to each job type
- Estimates learning time

Access it by clicking the "🤖 Learn with AI" button on any job page.

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.2
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3 (Modern dark theme)
- **Authentication**: Flask sessions with password hashing

## 📊 Database Models

- **User** - User accounts (employers/workers) with profiles
- **Task** - Job postings
- **Bid** - Worker bids on jobs
- **Review** - Ratings and reviews
- **Message** - User messages

## 🔧 Configuration

The application uses default configuration. To customize:

- **Database**: Edit `SQLALCHEMY_DATABASE_URI` in `app.py`
- **Secret Key**: Change `SECRET_KEY` in `app.py` for production

## 🚧 Future Enhancements

- [ ] Payment integration
- [ ] File uploads for job deliverables
- [ ] Email notifications
- [ ] Advanced AI recommendations
- [ ] Portfolio uploads
- [ ] Real-time notifications
- [ ] Mobile app

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
- All contributors and users

---

**Made with ❤️ for freelancers and employers**

