# job_scraping



```markdown
# Django Authentication API

This is a Django-based web application that handles user authentication, including registration, login, profile view, and password management. It also supports JWT-based token authentication for secure API access.

## Features

- User registration with JWT token generation
- User login with JWT token generation
- Profile view (requires authentication)
- Forgot password functionality
- Password reset via email
- Password reset functionality via token

## Technologies Used

- **Django**: Web framework used to build the backend API.
- **Django Rest Framework (DRF)**: For building the API endpoints.
- **JWT (JSON Web Tokens)**: For secure authentication and token management.
- **Django Simple JWT**: For handling JWT tokens.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/alistair46/job_scraping.git
   ```

2. Navigate to the project directory:

   ```bash
   cd yourrepository
   ```

3. Create a virtual environment and activate it:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

The application will be running at `http://127.0.0.1:8000/`.

## API Endpoints

### User Registration
- **URL**: `/register/`
- **Method**: `POST`
- **Request**: JSON payload containing user information (email, password, etc.)
- **Response**: JWT token if registration is successful.

### User Login
- **URL**: `/login/`
- **Method**: `POST`
- **Request**: JSON payload containing email and password.
- **Response**: JWT token if login is successful.

### Profile View
- **URL**: `/profile/`
- **Method**: `GET`
- **Authentication**: Required (JWT token).
- **Response**: JSON payload containing the user's profile data.

### Forgot Password
- **URL**: `/ForgotPassword/`
- **Method**: `POST`
- **Request**: JSON payload containing user email.
- **Response**: Confirmation message indicating that the password reset link has been sent.

### Reset Password via Email
- **URL**: `/ResetMail/`
- **Method**: `POST`
- **Request**: JSON payload containing email.
- **Response**: Confirmation message indicating a password reset email was sent.

### Reset Password
- **URL**: `/ResetPassword/<uid>/<token>/`
- **Method**: `POST`
- **Request**: JSON payload containing new password.
- **Response**: Confirmation message indicating that the password has been successfully reset.

## Development

To contribute to this project, fork the repository, make your changes, and submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
```
