# 📚 Folio — Book Review Community

A full-featured Django book review community website. **Pure Python, no JavaScript required.**

## Features

- 📖 **Book Library** — Add, edit, search, and browse books by genre, rating, or newest
- ⭐ **Reviews & Ratings** — 1–5 star ratings with full written reviews per user
- 📌 **Reading Lists** — Track books as "Want to Read", "Currently Reading", or "Read"
- 👍 **Helpful Votes** — Mark reviews as helpful
- 👤 **User Profiles** — Bio, avatar, reading goal progress bar, favorite genre
- 🏘 **Community Page** — See top members and latest activity
- 🔐 **Auth** — Register, login, logout (Django built-in)
- 🛠 **Admin Panel** — Full Django admin at /admin/
- 🌱 **Seed Command** — Populate DB with sample data instantly

## Tech Stack

- **Backend**: Django 4.2 (Python only — no JavaScript)
- **Database**: SQLite (zero config)
- **Storage**: Local file system (Pillow for images)
- **Styling**: Pure CSS in templates (no external JS frameworks)
- **Templates**: Django template language

## Quick Start

```bash
# 1. Clone / extract project
cd folio

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Seed with sample data (optional but recommended)
python manage.py seed_data

# 5. Start the server
python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

## Login Credentials (after seed_data)

| Role  | Username     | Password     |
|-------|-------------|--------------|
| Admin | `admin`     | `admin123`   |
| User  | `alice_reads` | `password123` |
| User  | `bookworm_ben` | `password123` |

Admin panel: **http://127.0.0.1:8000/admin/**

## Project Structure

```
folio/
├── manage.py
├── requirements.txt
├── db.sqlite3              (created after migrate)
├── folio/                  # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/                  # Main app
│   ├── models.py           # Book, Review, UserProfile, ReadingList
│   ├── views.py            # All views + signal handlers
│   ├── forms.py            # All forms
│   ├── urls.py             # URL patterns
│   ├── admin.py            # Admin config
│   └── management/
│       └── commands/
│           └── seed_data.py
├── templates/
│   ├── base.html           # Layout + CSS
│   ├── books/
│   │   ├── home.html
│   │   ├── book_list.html
│   │   ├── book_detail.html
│   │   ├── book_form.html
│   │   ├── book_confirm_delete.html
│   │   ├── profile.html
│   │   ├── profile_edit.html
│   │   └── community.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── static/                 # Static files dir
└── media/                  # User uploads (covers, avatars)
```

## URL Map

| URL | View | Description |
|-----|------|-------------|
| `/` | home | Homepage with stats & recent activity |
| `/books/` | book_list | Browse/search/filter all books |
| `/books/add/` | book_add | Add a new book |
| `/books/<id>/` | book_detail | Book page with reviews |
| `/books/<id>/edit/` | book_edit | Edit a book |
| `/books/<id>/delete/` | book_delete | Delete a book |
| `/books/<id>/review/` | review_submit | POST: submit review |
| `/books/<id>/reading-list/` | reading_list_update | POST: update reading status |
| `/review/<id>/delete/` | review_delete | Delete a review |
| `/review/<id>/like/` | review_like | POST: toggle helpful vote |
| `/register/` | register | New user registration |
| `/profile/<username>/` | profile | User profile page |
| `/profile/edit/me/` | profile_edit | Edit own profile |
| `/community/` | community | Community activity feed |
| `/login/` | (built-in) | Sign in |
| `/logout/` | (built-in) | Sign out |
| `/admin/` | (built-in) | Django admin |
