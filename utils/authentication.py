import streamlit as st
import bcrypt
import pymysql
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")


# Function to establish a connection to the MySQL database
def get_connection():
    return pymysql.connect(
        host=DB_HOST, port=3306, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE
    )


# Hash and salt password for protection
def hash_password(pw):
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())


def check_password(entered_password, hashed_password):
    return bcrypt.checkpw(
        entered_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# Function to register a new user
def register_user(email, entered_password):
    hashed_password = hash_password(entered_password)
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s)",
                (email, hashed_password),
            )
        connection.commit()
        st.success(f"User '{email}' registered successfully!")
    finally:
        connection.close()


# Function to authenticate a user
def authenticate_user(email, entered_password):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # select hashed passwords where the username matches
            cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()[0]
            if result and check_password(entered_password, result):
                st.success(f"User '{email}' authenticated successfully!")
                return True
            else:
                st.error("Authentication failed. Incorrect email or password.")
                return False
    finally:
        connection.close()
