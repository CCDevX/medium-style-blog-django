# Plume - Medium-Style Blog

A modern and elegant blog platform inspired by Medium, built with Django. Plume provides an intuitive platform for sharing ideas, stories, and reflections.

**Live Demo**: [https://medium-style-blog-django.onrender.com/](https://medium-style-blog-django.onrender.com/)

## Features

### For Visitors
- Browse published articles
- Navigate by categories and tags
- Comment system with star ratings (1-5 stars)
- Contact form with file attachment support
- Responsive and modern interface

### For Authenticated Users
- Create and edit articles with CKEditor
- Image uploads via Cloudinary
- Personal dashboard
- Manage drafts and published articles
- Profile management
- Assign categories and multiple tags

## Tech Stack

### Backend
- **Django 5.2.7** - Python web framework
- **PostgreSQL** - Database
- **Cloudinary** - Cloud storage for images
- **WhiteNoise** - Static files management

### Frontend
- **Bootstrap 5.3.8** - CSS framework
- **CKEditor 5** - Rich text editor
- **Select2** - Enhanced multiple selection
- **Fonts**: Inter (body) & Lora (headings)

### Deployment
- **Render.com** - Hosting platform
- **Gunicorn** - WSGI server

## Local Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Cloudinary account

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd project
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file at the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/django_blog
PGCLIENTENCODING=utf8

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Cloudinary
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

5. **Apply migrations**
```bash
python manage.py migrate
```

6. **Create a superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Start the development server**
```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`

## Project Structure

```
project/
├── blog/                      # Main blog application
│   ├── models/               # Database models (Post, Category, Tag, etc.)
│   ├── views.py              # Views and business logic
│   ├── forms/                # Django forms
│   ├── templates/            # HTML templates
│   └── admin.py              # Django admin configuration
├── authenticated/            # Authentication application
│   ├── views.py              # Login, register, logout
│   ├── forms/                # Authentication forms
│   └── templates/            # Auth templates
├── config/                   # Django configuration
│   ├── settings.py           # Project settings
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
├── public/                   # Static files (CSS, JS, images)
├── .env                      # Environment variables
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Database Models

### Core Models

**Post**
- Title, content (rich text)
- Author (ForeignKey to User)
- Category (ForeignKey)
- Tags (ManyToMany)
- Image (CloudinaryField)
- Publication status

**Category**
- Name and description
- Timestamps

**Tag**
- Name and description
- Timestamps

**Comment**
- Content and rating (1-5)
- Author and associated post
- Timestamps

**Profile**
- User information extension
- First name, last name, email
- Biography

**Contact**
- Contact form submissions
- Civility, name, email, subject, message
- Optional file attachment

## Key Features Details

### Rich Text Editor
The blog uses CKEditor 5 for article creation and editing, providing:
- Text formatting (bold, italic, links)
- Lists (ordered and unordered)
- Blockquotes and tables
- Heading levels

### Image Management
Images are stored on Cloudinary with automatic:
- Upload and storage
- Deletion when articles are removed
- URL generation for display

### Dashboard
Authenticated users have access to a comprehensive dashboard with:
- Tabs for published articles and drafts
- Profile management
- Quick actions (view, edit, delete)
- Pagination for large lists

## Routes

### Public Routes
- `/` - Home page with featured articles
- `/post/` - All published articles
- `/post/<id>/` - Single article view
- `/contact/` - Contact form
- `/authenticated/login/` - Login page
- `/authenticated/register/` - Registration page

### Protected Routes (Login Required)
- `/dashboard/` - User dashboard
- `/dashboard/new-post/` - Create new article
- `/dashboard/edit-post/<id>` - Edit article
- `/dashboard/view-post/<id>` - View article details
- `/dashboard/delete-post/<id>` - Delete article
- `/dashboard/blog-dashboard-edit-profile/` - Edit profile

## Deployment on Render

### Configuration

1. **Create a new Web Service** on Render

2. **Environment Variables** to set:
```
DATABASE_URL=<your-postgresql-url>
SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
PYTHON_VERSION=3.9.0
```

3. **Build Command**:
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

4. **Start Command**:
```bash
gunicorn config.wsgi:application
```

## Admin Panel

Access the Django admin at `/admin/` to manage:
- Users and permissions
- Articles, categories, and tags
- Comments and moderation
- Contact form submissions

## Security Features

- CSRF protection enabled
- Password validation
- Secure session management
- Environment-based configuration
- Cloudinary secure uploads

## License

This project is open source and available under the MIT License.

---

**Note**: Make sure to never commit your `.env` file or expose sensitive credentials in your repository.
