# Django Chat Application

## Overview
This is a **real-time chat application** built with **Django** and **Tailwind CSS**, designed to provide a clean, modern, and mobile-friendly messaging experience.  

It supports full user authentication, profile management, friend lists with live updates, and a responsive interface optimized for both desktop and mobile devices.

---

## ✨ Features

### 🔐 User Authentication
- Create an account, log in, and log out.
- Profile pages show user info including profile image, name, phone, and status.
- Secure password storage with Django authentication system.

### 👫 Friends List & Messaging
- Displays all friends with:
  - **Last message preview** (latest chat between both users).
  - **Unread message count** (real-time badge).
  - **Timestamp of last message**.
- Messages are retrieved using Django’s `Q` objects for two-way querying.
- Messages are marked as read once viewed.

### 💬 Real-Time Updates
- Friends list automatically refreshes to display:
  - New messages
  - Updated unread counts
- Implemented using AJAX polling / `setInterval` (can be extended to WebSockets).

### 👤 User Info Section
- Profile picture (large, circular, and responsive).
- Full name, phone number, and status message.
- Layout adapts: stacked on mobile, side-by-side on larger screens.

### ⚙️ Settings Section
- Accessible via navbar settings icon.
- Options include:
  - Profile management
  - Help & Support
  - Change app language
  - Logout

### 🗑️ Profile & Data Management
- When a user deletes their account, their **profile and linked data** (friends, chats) are also deleted automatically using Django’s `on_delete=models.CASCADE`.

### 📱 Responsive Navbar
- Fixed at the top with:
  - Profile image
  - Username
  - Search bar
  - Settings icon
- Mobile-friendly stacked layout with Tailwind.

---

## 🛠 Technologies Used
- **Backend:** Django (Python)
- **Frontend:** Tailwind CSS, HTML, Django Templates
- **Database:** SQLite (default) or any Django-supported DB
- **Utilities:** Django ORM with `Q` objects, static/media handling

---

## 🚀 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/django-chat-app.git
cd django-chat-app
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Access the app**
- Browser: `http://127.0.0.1:8000/`
- Or expose online with **ngrok**:
```bash
ngrok http 8000
```

---

## 📂 Folder Structure
```
django-chat-app/
│
├── chat/                   # Main app
│   ├── templates/          # Django HTML templates
│   ├── static/             # CSS, images, JS
│   ├── models.py           # User, Friend, ChatMessage models
│   ├── views.py            # Views for chat, profiles, settings
│   └── urls.py             # App URLs
│
├── project_name/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3              # Database (default)
├── manage.py               # Django management script
├── requirements.txt
└── README.md
```

---

## 💻 Example Code Snippets

### Fetch messages between two users
```python
from django.db.models import Q

messages = ChatMessage.objects.filter(
    Q(msg_sender=user, msg_receiver=friend.profile) |
    Q(msg_sender=friend.profile, msg_receiver=user)
).order_by('-created_at')
```

### Count unread messages
```python
unread_count = ChatMessage.objects.filter(
    msg_sender=friend.profile, 
    msg_receiver=user, 
    is_read=False
).count()
```

---

## 🤝 Contributing
1. Fork the repo  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:  
   ```bash
   git commit -m "Add new feature"
   ```
4. Push branch:  
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request 🎉

---

## 📜 License
MIT License © 2025 Your Name
