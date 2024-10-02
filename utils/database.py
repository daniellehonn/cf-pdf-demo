import streamlit as st
import pyrebase
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# # Initialize connection.
# # Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_connection():
#     return MongoClient(os.getenv("MONGO_DB_URI"), server_api=ServerApi('1'))


# client = init_connection()

# # Pull data from the collection.
# # Uses st.cache_data to only rerun when the query changes or after 10 min.

# def get_data():
#     db = client.cf_pdf_demo
#     items = db.userInfo.find()
#     items = list(items)  # make hashable for st.cache_data
#     return items

# userInfo = get_data()

# # Function to check credentials against the retrieved data
# def check_credentials(username, password):
#     for user in userInfo:
#         if user['username'] == username and user['password'] == password:
#             return True
#     print(userInfo)
#     return False

# # Function to check if a username already exists
# def username_exists(username):
#     for user in userInfo:
#         if user['username'] == username:
#             return True
#     return False

# # Function to check if a username already exists
# def username_exists(username):
#     for user in userInfo:
#         if user['username'] == username:
#             return True
#     return False

# # Function to add a new user to the database
# def add_user_to_db(username, password):
#     db = client.cf_pdf_demo
#     db.userInfo.insert_one({"username": username, "password": password})

# # Function to add a pdf_name under a user's 'loaded_pdfs' list
# def add_pdf_to_user(username, pdf_name):
#     db = client.cf_pdf_demo
#     db.userInfo.update_one({"username": username}, {"$push": {"loaded_pdfs": pdf_name}})


# Firebase configuration (from your Firebase project settings)
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
    # "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Function to sign up a new user
def sign_up(username, password):
    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user_with_email_and_password(username, password)
        
        # Add user details to Firestore or Realtime Database
        user_data = {
            "username": username,
            "loaded_pdfs": []
        }
        db.child("users").child(user['localId']).set(user_data)
        
        st.success("User created successfully")
        return True
    except Exception as e:
        st.error(f"Error creating user: {str(e)}")
        return False

# Function to sign in an existing user
def sign_in(username, password):
    try:
        # Sign in using Firebase Authentication
        user = auth.sign_in_with_email_and_password(username, password)
        return user
    except Exception as e:
        st.error("Invalid username or password")
        return None

# Function to check if a username already exists
def username_exists(username):
    try:
        users = db.child("users").get()
        for user in users.each():
            if user.val()["username"] == username:
                return True
        return False
    except Exception as e:
        st.error(f"Error checking username: {str(e)}")
        return False

# Function to add a PDF name under a user's 'loaded_pdfs' list
def add_pdf_to_user(username, pdf_name):
    try:
        db.child("users").child(username).child("loaded_pdfs").push(pdf_name)
        st.success(f"PDF '{pdf_name}' added to user {username}")
    except Exception as e:
        st.error(f"Error adding PDF: {str(e)}")
