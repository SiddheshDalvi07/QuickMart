# QuickMart

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [Testing](#testing)
9. [Contributing](#contributing)
10. [License](#license)

## Introduction
Django eKart is a comprehensive e-commerce application built with Django, designed to provide a robust and scalable solution for online retail businesses. This project includes features like user authentication, product management, order processing, and more.

## Features
- User Registration and Authentication
- Product Management (CRUD)
- Shopping Cart
- Order Management
- Payment Integration
- Responsive Design
- Admin Dashboard
- Search and Filtering

## Installation
To get started with Django eKart, follow these steps:

### Prerequisites
- Python 3.8+
- Django 3.2+
- SQLite (for development)

### Steps
1. **Clone the Repository:**
    ```sh
    git clone https://github.com/SiddheshDalvi07/QuickMart.git
    cd django project
    cd ecom
    ```

2. **Create a Virtual Environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up the Database:**
    - For SQLite (default), no additional configuration is needed.

5. **Apply Migrations:**
    ```sh
    python manage.py migrate
    ```

6. **Create a Superuser:**
    ```sh
    python manage.py createsuperuser
    ```

7. **Collect Static Files:**
    ```sh
    python manage.py collectstatic
    ```

## Usage
### Running the Development Server
To start the development server, run:
```sh
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to view the application.

### Admin Dashboard
Access the admin dashboard at `http://127.0.0.1:8000/admin/` using the superuser credentials created earlier.

## Configuration
### Static Files
Ensure you have configured the static files settings in `ecom/settings.py`:
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

## Running the Application
After completing the installation and configuration steps, you can run the development server using:
```sh
python manage.py runserver
```

## Testing
To run the tests for the application, use:
```sh
python manage.py test
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

### Steps to Contribute
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch`
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
