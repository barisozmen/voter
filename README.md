# 🗳️ Votely - Modern Django Voting Platform

A production-ready Django voting application demonstrating modern Django architecture with elegant, reusable components.

## 🎯 Features

- **Modern Django Architecture** - Clean, maintainable code structure
- **Reusable Components** - Built with `django-components`
- **Beautiful UI** - Bootstrap 5 with responsive design
- **Real-time Voting** - AJAX-powered voting with live results
- **User Authentication** - Login, registration, and user management
- **Tag-based Organization** - Categorize and filter polls
- **Advanced Filtering** - Search and filter polls by multiple criteria
- **Admin Interface** - Full Django admin integration

## 🛠️ Tech Stack

### Core
- **Django 5.0+** - Web framework
- **SQLite** - Database (easily configurable for PostgreSQL/MySQL)
- **Bootstrap 5** - Frontend framework

### Django Extensions
- **django-components** - Modular, reusable UI components
- **django-bootstrap5** - Bootstrap 5 integration
- **django-braces** - Class-based view mixins
- **django-extensions** - Development utilities
- **django-taggit** - Tagging system
- **django-filter** - Advanced filtering
- **django-crispy-forms** - Form rendering
- **django-allauth** - Authentication system
- **django-debug-toolbar** - Development debugging
- **Custom Voting System** - Elegant Django 5.x compatible voting (replaces django-vote)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
cd /path/to/your/projects
git clone <repository-url> votely
cd votely

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional - seed data includes admin user)
python manage.py createsuperuser

# Seed with sample data
python manage.py seed_data
```

### 3. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 to see the application!

## 👥 Default Accounts

The seed data creates the following accounts:

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full admin access via `/admin/`

### User Accounts
- **Usernames:** `user1`, `user2`, `user3`, `user4`, `user5`
- **Password:** `password123` (for all users)

## 📁 Project Structure

```
votely/
├── manage.py
├── requirements.txt
├── README.md
├── votely/                 # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── polls/                  # Main application
│   ├── models.py          # Poll, Choice, Vote models
│   ├── views.py           # Class-based views with mixins
│   ├── forms.py           # Forms with crispy-forms
│   ├── filters.py         # django-filter configurations
│   ├── admin.py           # Admin configurations
│   ├── components/        # Django components
│   │   ├── navbar.py
│   │   ├── poll_card.py
│   │   ├── vote_form.py
│   │   └── ...
│   └── management/        # Management commands
│       └── commands/
│           └── seed_data.py
└── templates/             # Templates
    ├── base.html
    └── polls/
        ├── poll_list.html
        ├── poll_detail.html
        └── components/    # Component templates
```

## 🧩 Key Components

### Models (`polls/models.py` & `polls/voting.py`)
- **Poll** - Main poll model with tagging support
- **Choice** - Poll choices with custom voting mixin
- **Vote** - Elegant voting system with generic relations
- **VotableMixin** - Reusable voting functionality for any model

### Views (`polls/views.py`)
- **PollListView** - Filtered, paginated poll listing
- **PollDetailView** - Poll details with voting
- **PollCreateView** - Poll creation form
- **VoteView** - AJAX voting endpoint

### Components (`polls/components/`)
- **NavbarComponent** - Site navigation
- **PollCardComponent** - Poll display cards
- **VoteFormComponent** - Voting interface
- **PollResultsComponent** - Results visualization
- **AlertsComponent** - Message display

## 🎨 UI Features

### Bootstrap 5 Integration
- Responsive grid system
- Modern component styling
- Custom CSS enhancements
- Bootstrap Icons

### Interactive Elements
- AJAX voting without page reload
- Live results updates
- Copy-to-clipboard poll sharing
- Responsive design for all devices

### User Experience
- Breadcrumb navigation
- Contextual alerts and messages
- Loading states and animations
- Accessible form controls

## ⚙️ Development

### Available Commands

```bash
# Seed database with sample data
python manage.py seed_data

# Clear and reseed data
python manage.py seed_data --clear

# Enhanced Django shell
python manage.py shell_plus

# Generate model graphs (requires graphviz)
python manage.py graph_models polls -o models.png

# Run development server with debug toolbar
python manage.py runserver
```

### Debug Tools
- **Django Debug Toolbar** - Available at `/debug/`
- **django-extensions** - Enhanced shell and utilities
- **Admin Interface** - Full model management at `/admin/`

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@localhost/dbname
```

### Database Configuration
For PostgreSQL in production:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'votely_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Poll list with filtering |
| `/create/` | GET/POST | Create new poll |
| `/poll/<id>/` | GET | Poll detail and voting |
| `/vote/<id>/` | POST | Submit vote (AJAX) |
| `/results/<id>/` | GET | Live results (AJAX) |
| `/accounts/login/` | GET/POST | User login |
| `/accounts/signup/` | GET/POST | User registration |
| `/admin/` | GET | Admin interface |

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure allowed hosts
- [ ] Set up HTTPS
- [ ] Configure email backend
- [ ] Set up monitoring and logging

### Static Files
```bash
python manage.py collectstatic
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with ❤️ using Django and modern web technologies
- Inspired by elegant software architecture principles
- Special thanks to the Django community and extension maintainers

---

**Votely** - *Elegant voting made simple* 🗳️
