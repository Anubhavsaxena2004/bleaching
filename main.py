# main.py
import joblib
import pandas as pd
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

# Import everything from your new files
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    verify_password,
    get_password_hash
)
from models import CoralData, Token, TokenData

# --- App Initialization and CORS ---
app = FastAPI()

origins = [
    "http://localhost", 
    "http://localhost:8080", 
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "null",
    "*"  # Allow all origins for development
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load Model and Fake Database ---
try:
    # Try to load the balanced model first
    model = joblib.load('coral_bleaching_model_balanced.joblib')
    print("✅ Loaded balanced coral bleaching model")
except FileNotFoundError:
    # Fallback to original model if balanced model doesn't exist
    model = joblib.load('coral_bleaching_model.joblib')
    print("⚠️  Loaded original coral bleaching model (may be biased)")

# FAKE DATABASE: In a real app, this would be a real database.
# Hashing the password for our fake user 'johndoe'
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": get_password_hash("secretpassword"),
        "disabled": False,
    }
}

# --- Authentication Endpoints ---
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint. Takes username and password, returns a JWT token.
    """
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Protected Prediction Endpoint ---
@app.post("/predict")
def predict_bleaching(
    data: CoralData,
    current_user: TokenData = Depends(get_current_user) # This dependency protects the endpoint
):
    """
    This endpoint is now protected. A valid JWT token must be provided.
    """
    training_columns = ['SSTA_DHW', 'TSA_DHW', 'Temperature_Maximum', 'Turbidity', 'Depth_m']
    input_df = pd.DataFrame([data.dict()])[training_columns]
    
    prediction = model.predict(input_df)
    result = int(prediction[0])
    
    return {"prediction": result, "user": current_user.username}


# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Coral API! Go to /docs for documentation."}
