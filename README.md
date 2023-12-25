# Mad2 Project (Grocery Store)

Welcome to the Mad2 project, a grocery store application with a Vue.js frontend and a Flask (Python) backend.

## Project Structure

The project is organized into two main folders:

1. **frontend:**
   - Contains all the frontend code written in Vue.js.
   - Utilizes the Axios library to communicate with the backend API.

2. **backend:**
   - Consists of the Flask (Python) backend.
   - Handles API requests from the frontend and interacts with the database.

## Configuration

The application uses environment variables to manage its configuration. Create a `.env` file in the root of the `backend` folder with the following variables:

```env
SECRET_KEY=<your_secret_key>
DEBUG=<True_or_False>
SQLALCHEMY_DATABASE_URI=<your_database_uri>
SQLALCHEMY_ECHO=<True_or_False>
JWT_SECRET_KEY=<your_jwt_secret_key>

MAIL_SERVER=<your_mail_server>
MAIL_PORT=<your_mail_port>
MAIL_USERNAME=<your_mail_username>
MAIL_PASSWORD=<your_mail_password>
MAIL_DEFAULT_SENDER=<your_mail_default_sender>

USER_NAME=<your_default_user_name>
USER_EMAIL=<your_default_user_email>
USER_PASSWORD=<your_default_user_password>
```

## Running The Application

### Frontend

```bash
  cd frontend
```
```bash
  npm install
```
```bash
  npm run serve
```

### Backend

```bash
  cd backend
```
(Create Virtual Environment)

```bash
  pip install -r requirements.txt
```
```bash
  python run.py
```

### Celery and Redis

You will need WSL (ubuntu) to Run CELERY AND REDIS


```bash
  redis-server
```

```bash
  celery -A make_celery worker -l info
  
```
```bash
  celery -A make_celery beat -l info
```

Video Link For Reference

[Grocery Store Web App Demo Link](https://www.youtube.com/watch?v=W4YQrcDyZTc)


## Contributing

Contributions are welcome! If you have suggestions, improvements, or find any issues, feel free to open a pull request or create an issue.
