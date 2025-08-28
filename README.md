# Coral Bleaching Predictor with JWT Authentication

A FastAPI-based web application that predicts coral bleaching events using machine learning, with secure JWT authentication.

## Features

- 🔐 **JWT Authentication**: Secure login/logout system
- 🧠 **ML Prediction**: Coral bleaching prediction using trained model
- 🎨 **Modern UI**: Beautiful, responsive interface with Tailwind CSS
- 🔒 **Protected Endpoints**: API endpoints require authentication
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
coral_api/
├── coral_bleaching_model.joblib  # Your trained ML model
├── main.py                       # FastAPI application with endpoints
├── auth.py                       # JWT authentication logic
├── models.py                     # Pydantic data models
├── requirements.txt              # Python dependencies
├── index.html                    # Frontend interface
└── README.md                     # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### 3. Open the Frontend

Open `index.html` in your web browser. You can double-click the file or drag it into your browser.

## Usage

### Demo Credentials

- **Username**: `johndoe`
- **Password**: `secretpassword`

### How to Use

1. **Login**: Enter the demo credentials on the login page
2. **Adjust Parameters**: Use the sliders to set environmental factors:
   - Turbidity (0-5)
   - Depth in meters (0-50)
   - Maximum Temperature (°C) (20-40)
   - SSTA Degree Heating Week (0-20)
   - TSA Degree Heating Week (0-20)
3. **Predict**: Click the "Predict" button to get results
4. **Logout**: Use the logout button when finished

## API Endpoints

### Public Endpoints

- `GET /` - Welcome message
- `POST /token` - Login endpoint (returns JWT token)

### Protected Endpoints

- `POST /predict` - Coral bleaching prediction (requires JWT token)

## Authentication Flow

1. **Login**: User submits username/password to `/token`
2. **Token**: Server returns JWT access token
3. **Requests**: Frontend includes token in Authorization header
4. **Validation**: Server validates token for protected endpoints
5. **Logout**: Frontend removes token from localStorage

## Security Features

- **Password Hashing**: Passwords are hashed using bcrypt
- **JWT Tokens**: Secure, time-limited access tokens
- **CORS Protection**: Configured for local development
- **Input Validation**: All inputs validated using Pydantic models

## Customization

### Adding New Users

Edit the `fake_users_db` in `main.py`:

```python
fake_users_db = {
    "newuser": {
        "username": "newuser",
        "full_name": "New User",
        "email": "newuser@example.com",
        "hashed_password": get_password_hash("newpassword"),
        "disabled": False,
    }
}
```

### Changing Secret Key

Update the `SECRET_KEY` in `auth.py`:

```python
SECRET_KEY = "your-new-secret-key-here"
```

### Token Expiration

Modify `ACCESS_TOKEN_EXPIRE_MINUTES` in `auth.py`:

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
```

## Development

### API Documentation

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### Testing the API

You can test the protected endpoint using curl:

```bash
# First, get a token
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secretpassword"

# Then use the token for predictions
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"Turbidity": 0.5, "Depth_m": 10, "Temperature_Maximum": 30.0, "SSTA_DHW": 4.0, "TSA_DHW": 1.0}'
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend server is running on `http://127.0.0.1:8000`
2. **Model Loading Error**: Check that `coral_bleaching_model.joblib` exists in the project directory
3. **Authentication Failed**: Verify you're using the correct demo credentials
4. **Token Expired**: Re-login to get a new token

### Server Not Starting

- Check if port 8000 is available
- Ensure all dependencies are installed
- Verify Python version compatibility (3.7+)

## Production Considerations

For production deployment:

1. **Database**: Replace fake database with real database (PostgreSQL, MySQL, etc.)
2. **Secret Key**: Generate a strong, random secret key
3. **HTTPS**: Use HTTPS in production
4. **Environment Variables**: Store sensitive data in environment variables
5. **Rate Limiting**: Add rate limiting to prevent abuse
6. **Logging**: Add proper logging and monitoring

## License

This project is for educational purposes. Feel free to modify and use as needed.
