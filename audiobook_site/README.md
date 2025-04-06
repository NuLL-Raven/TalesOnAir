# 👨‍💻 Author
**Dela** - [DelaTech]
**xkhalil** - [Khalil]
Computer Science Student | Web Developer

# Audiobook and PDF Books Website

## Overview

This project is a Django-based web application designed to create a platform for users to access audiobooks and PDF books. It features functionalities like user authentication, subscription plans, and personalized recommendations based on user preferences. The website includes features like sign-up/sign-in, user profile management, subscription management, and a clean and intuitive home page.

## Features

- **User Authentication**: Users can sign up, log in, and log out using either their username or email and password.
- **Subscription Plans**: The application includes subscription plans such as Free, Basic, and Premium. Users can select a plan at sign-up and enjoy benefits based on their subscription.
- **Book Catalog**: Users can view available books by genre, search, and filter through the catalog.
- **Personal Playlists**: Users can create and manage their own playlists by adding books to them.
- **Genre-based Sorting**: Books are categorized by genre, allowing users to explore different types of content.
- **Responsive Design**: The website is designed to work seamlessly on both desktop and mobile devices.
- **Database Management**: The project uses a relational database (e.g., SQLite or PostgreSQL) to store information about users, books, subscriptions, and playlists.

## Technologies Used

- **Backend**: Django (Python framework)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (or PostgreSQL in production)
- **Authentication**: Django's built-in authentication system, customized to support logging in with either username or email.
- **Forms**: Django Forms for user input handling (sign up, sign in, etc.)

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/audiobook-site.git
```

2. **Navigate to the project directory**:

```bash
cd audiobook-site
```

3. **Create a virtual environment**:

```bash
python -m venv .venv
```

4. **Activate the virtual environment**:

- For Windows:

```bash
.venv\Scriptsctivate
```

- For macOS/Linux:

```bash
source .venv/bin/activate
```

5. **Install dependencies**:

```bash
pip install -r requirements.txt
```

6. **Set up the database**:

```bash
python manage.py migrate
```

7. **Create a superuser to access the admin panel (optional)**:

```bash
python manage.py createsuperuser
```

8. **Run the development server**:

```bash
python manage.py runserver
```

Now, you can access the application by navigating to `http://127.0.0.1:8000` in your browser.

## File Structure

```
audiobook_site/
├── users/                     # User authentication, sign-up, and profile management
│   ├── migrations/
│   ├── templates/
│   └── views.py               # Handles user authentication views
├── books/                     # Book catalog and related models
│   ├── migrations/
│   └── models.py              # Models for Book, Subscription, Genre, etc.
├── templates/
│   ├── base.html              # Main layout for all pages
│   ├── home.html              # Homepage for users
│   └── sign_up.html           # Sign-up page
├── manage.py                  # Django management script
├── settings.py                # Project settings (includes database and middleware)
└── urls.py                    # URL routing for the application
```

## Models

### `User`

The custom `User` model inherits from Django's `AbstractUser` and includes a foreign key to the `Subscription` model.

```python
class User(AbstractUser):
    subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL, null=True, blank=True)
```

### `Subscription`

This model defines different subscription plans (Free, Basic, Premium), including their prices and durations.

```python
class Subscription(models.Model):
    SUBSCRIPTION_TYPES = [
        ('FREE', 'Free'),
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
    ]
    subscription_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
```

### `Book`

This model stores information about books, including title, author, genre, and availability in audio format.

```python
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    audio_availability = models.BooleanField(default=False)
```

## Views

### `sign_up` and `sign_in` Views

These views handle user registration and login, including custom validation for username/email login.

```python
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            subscription = Subscription.objects.get(type='FREE')
            user.subscription = subscription
            user.save()
            login(request, user)
            return redirect('home')
```

```python
def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
```

## How to Contribute

Feel free to fork the repository, make changes, and create pull requests. If you find any bugs or have suggestions, please open an issue.

## License

This project is licensed under the MIT License.
