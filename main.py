from tkinter import *
from tkinter import messagebox
import sys, re
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("tealswe-ec5ca-firebase-adminsdk-syh62-7a87371f5c.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()



"""
log in, sign up
  5 unique accounts, 6th try "All permitted accounts have been created, please come back
later"
  password minimum 8 characters, maximum 12 characters, 1 capital letter, 1 digit, one special character 
"""

def sign_up_users(user_name, first_name, last_name, email, password):
  user_data = {
    "user_name": user_name,
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "password": password
  }

  doc_ref = db.collection("users").document(user_name)

  doc_ref.set(user_data)


def user_exists_by_first_name_last_name(first_name, last_name):
  users_ref = db.collection("users")
  users = users_ref.get()
  if users:
      for user in users:
          user_data = user.to_dict()
          if user_data.get("first_name") == first_name and user_data.get("last_name") == last_name:
            return True
  print("They are not a part of the InCollege system yet")
  return False


def count_users():
  users_ref = db.collection("users")
  users = users_ref.get()
  num_users = len(users)
  return num_users

def check_user_credentials(user_name, password) ->bool:
  user_ref = db.collection("users").document(user_name)
  user_data = user_ref.get().to_dict()

  if user_data and user_data.get('password') == password:
      return True
  else:
      return False


def check_password(password):
  if len(password) < 8 or len(password) > 12:
    return False

  if not any(char.isdigit() for char in password):
    return False

  if not re.search("(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&])", password):
    return False
  
  if not any(char.isupper() for char in password):
    return False
  
  return True

def post_job(title, description, employer, location, salary, posted_by):
  job_data = {
      "title": title,
      "description": description,
      "employer": employer,
      "location": location,
      "salary": salary,
      "posted_by": posted_by
  }

  db.collection("jobs").add(job_data)
  messagebox.showinfo("Success", "Job posted successfully!")

global flagLoggedInSignedUp
flagLoggedInSignedUp = False

def chooseLogInSignUp():
  global flagLoggedInSignedUp
  print("1. Log In ")
  print("2. Sign Up ")
  print("Enter your choice: ")
  
  choice = input()
  if choice == '1':
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if check_user_credentials(username, password):
      print("Log in successful!")
      flagLoggedInSignedUp =True
      
    else:
      print("Invalid username or password.")
  elif choice == '2':
    user_name = input("Enter your username: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    if count_users()<5:
      if check_password(password):
        sign_up_users(user_name, first_name, last_name, email, password)
        print("Sign up successful!")
        flagLoggedInSignedUp = True
        
      else:
        print("Invalid password. Password must be between 8 and 12 characters, contain at least one capital letter, one digit, and one special character.")

    else:
      print("All permitted accounts have been created, please come back later")
     
  else:
      print("Invalid choice. Please choose 1 for log in or 2 for sign up")


def display_success_story():
  print("College Student Success Story:")
  print("John Doe used InCollege to get his dream job at XYZ Company!")

def connect_with_people():
  first_name = input("Enter first name: ")
  last_name = input("Enter last name: ")
  if user_exists_by_first_name_last_name(first_name, last_name) is True:
    print("They are a part of the InCollege system")

def play_video():
  print("Video is now playing")
  
def main_menu():
  while True:
    print("\nMain Menu:")
    print("1. Display College Student Success Story")
    print("2. Play a Video")
    print("3. Log in or Create Account")
    print("4. Connect with People")
    print("5. Post a Job")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
      display_success_story()
    elif choice == '2':
      play_video()
    elif choice == '3':
      chooseLogInSignUp()
    elif choice == '4':
      connect_with_people()
    elif choice == '5':
      if flagLoggedInSignedUp is True:
        firstName = input("Enter first name: ")
        lastName = input("Enter last name: ")
        title = input("Enter job title: ")
        description = input("Enter job description: ")
        employer = input("Enter employer: ")
        location = input("Enter job location: ")
        salary = input("Enter salary: ")
        post_job(title, description, employer, location, salary, firstName+" "+lastName)
      else:
        print("Please log in or sign up first")
        
      
    elif choice == '6':
      print("Exiting program...")
      break
    else:
      print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main_menu()


