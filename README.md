# Django Chat Application

## Overview
This is a real-time **chat application** built with **Django** and **Tailwind CSS**. It allows users to:

- Create an account and log in.
- View a list of friends and chat with them.
- Send and receive text messages **and voice notes**.
- See the last message and unread message count for each friend.
- Update profile information and settings.
- Perform basic actions such as changing language preferences and logging out.

The app is **mobile-responsive** and includes a fixed navbar, user info card, and clean, modern interface.

---

## Features

### User Authentication
- Sign up, log in, and log out.
- Profile pages display user info, including profile image, name, and contact info.

### Friends List & Messaging
- View friends with last message preview and unread count.
- Chat messages support:
  - **Text messages**
  - **Voice notes (audio recording & playback)**
- Messages are retrieved using Django `Q` objects to handle conversations in both directions.

### Voice Notes 🎤
- Record audio messages directly in the chat.
- Play voice notes inside the chat interface.
- Files are uploaded and stored in the `voice_notes/` directory.

### User Info Section
- Displays profile picture, full name, phone number, and status.
- Responsive layout: stacked on mobile, side-by-side on desktop.
- Prominent large profile image.

### Settings Section
- Accessible via navbar settings icon.
- Options include:
  - Profile
  - Help
  - App Language
  - Logout

### Responsive Navbar
- Fixed at the top with profile image, username, search bar, and settings icon.
- Mobile-friendly layout with stacked items.

---

## Technologies Used
- **Backend:** Django, Python  
- **Frontend:** Tailwind CSS, HTML, Django templates, JavaScript (for recording & playing voice notes)  
- **Database:** SQLite (default) or any Django-supported DB  
- **Utilities:** Django `Q` objects for complex queries, static/media files for images, icons, and audio  

---

## Installation & Setup

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
* Browser: `http://127.0.0.1:8000/`  
* Or expose online using **ngrok**:
```bash
ngrok http 8000
```

---

## Folder Structure
```
django-chat-app/
│
├── chat/                   # Main app
│   ├── templates/          # Django HTML templates
│   ├── static/             # CSS, images, JS
│   ├── models.py           # User, Profile, ChatMessage models
│   ├── views.py            # Views for chats and user info
│   └── urls.py             # App URLs
│
├── media/                  # User uploaded files (profile images, voice notes)
├── project_name/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3              # Database
├── manage.py               # Django management script
└── requirements.txt
```

---

## Example Code Snippets

### Fetch messages between two users
```python
from django.db.models import Q

messages = ChatMessage.objects.filter(
    Q(msg_sender=user, msg_receiver=friend.profile) |
    Q(msg_sender=friend.profile, msg_receiver=user)
).order_by('-created_at')
```

### Model with Voice Notes
```python
class ChatMessage(models.Model):
    body = models.TextField(blank=True)
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='msg_sender')
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='msg_receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    voice_note = models.FileField(upload_to='voice_notes/', blank=True, null=True)
```

---

## Contributing
* Fork the repo  
* Create a branch: `git checkout -b feature/your-feature`  
* Make changes  
* Commit: `git commit -m "Add new feature"`  
* Push: `git push origin feature/your-feature`  
* Open a Pull Request  

---

## License
MIT License © 2025 Your Name
