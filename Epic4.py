#from tkinter import *
#from tkinter import messagebox
import sys, re
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate(
    "tealswe-ec5ca-firebase-adminsdk-syh62-7a87371f5c.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
# db.delete() such that database is wiped once progrgam is terminated
"""
log in, sign up
  10 unique accounts, 11th try "All permitted accounts have been created, please come back
later"
  password minimum 8 characters, maximum 12 characters, 1 capital letter, 1 digit, one special character 
"""


# create a new account and adds it to the database
def sign_up_users(user_name, first_name, last_name, email, password, university, major):
  default_language = "english"
  og_guest_controls = {"email": True, "sms": True, "target_adv": True}
  friends_list = {"user_name": False, "first_name": False, "last_name": False}
  pending_friends_list = {"user_name": False, "first_name": False, "last_name": False}
  
  user_data = {
      "user_name": user_name,
      "first_name": first_name,
      "last_name": last_name,
      "email": email,
      "password": password,
      "university": university,
      "major": major,
      "guest_controls": og_guest_controls,
      "language": default_language,
      "friends_list": friends_list,
      "pending_friends_list": pending_friends_list
  }

  doc_ref = db.collection("users").document(user_name)
  doc_ref.set(user_data)


# checks if a user is a part of the InCollege database
def user_exists_by_first_name_last_name(first_name, last_name):
  users_ref = db.collection("users")
  users = users_ref.get()
  search_topic = input(
      "How would you like to search for a friend? By 1. Last Name or 2. University or 3. Major? Enter choice number: "
  )

  # user has a choice of searching others by last name, university, or major
  if users:
    for user in users:
      user_data = user.to_dict()
      if user_data.get("first_name") == first_name:
        if search_topic == '1' and user_data.get("last_name") == last_name:
          print(
              'Results:\nUsername\tFirst Name\tLast Name\n' + user_data.get("user_name")+'\t'+ user_data.get("first_name")+'\t\t'+ user_data.get("last_name") + '\n')
          return True
        elif search_topic == '2':
          university = input("Enter university name: ")
          if user_data.get("university") == university:
            print(
                'Results:\nUsername\tFirst Name\tLast Name\tUniversity\n' + user_data.get("user_name")+'\t'+ user_data.get("first_name")+'\t\t'+ user_data.get("last_name")+ '\t\t'+ user_data.get("university") + '\n')
            return True
        elif search_topic == '3':
          major = input("Enter major: ")
          if user_data.get("major") == major:
            print(
                'Results:\nUsername\tFirst Name\tLast Name\tMajor\n' + user_data.get("user_name")+'\t'+ user_data.get("first_name")+'\t\t'+ user_data.get("last_name") +'\t\t'+ user_data.get("major") + '\n')
            return True
  print("They are not a part of the InCollege system yet")
  return False


# counter for number of users a part of the database
def count_users():
  users_ref = db.collection("users")
  users = users_ref.get()
  num_users = len(users)
  return num_users


# checks if user login info is correct and a part of the database
def check_user_credentials(user_name, password) -> bool:
  user_ref = db.collection("users").document(user_name)
  user_data = user_ref.get().to_dict()
  if user_data and user_data.get('password') == password:
    return True
  else:
    return False


# checks that created password meets requirements
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


# collects info to be included in a job post
def create_job():
  if flagLoggedInSignedUp is True:
    firstName = input("Enter first name: ")
    lastName = input("Enter last name: ")
    title = input("Enter job title: ")
    description = input("Enter job description: ")
    employer = input("Enter employer: ")
    location = input("Enter job location: ")
    salary = input("Enter salary: ")
    post_job(title, description, employer, location, salary,
             firstName + " " + lastName)
  else:
    print("Please log in or sign up first")


# posts the job entry to the database
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
  print("Job posted successfully!")


global flagLoggedInSignedUp
flagLoggedInSignedUp = False


# log-in or sign-in process
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
      flagLoggedInSignedUp = True

    else:
      print("Invalid username or password or account has not been created.")
  elif choice == '2':
    # max limit for accounts is 10
    if count_users() == 10:
      print("All permitted accounts have been created, please come back later")

    else:
      user_name = input("Enter your username: ")
      first_name = input("Enter your first name: ")
      last_name = input("Enter your last name: ")
      email = input("Enter your email: ")
      password = input("Enter your password: ")
      university = input("Enter your university: ")
      major = input("Enter your major: ")

      if check_password(password):
        sign_up_users(user_name, first_name, last_name, email, password,
                      university, major)
        print("Sign up successful!")
        flagLoggedInSignedUp = True

      else:
        print(
            "Invalid password. Password must be between 8 and 12 characters, contain at least one capital letter, one digit, and one special character."
        )
  else:
    print("Invalid choice. Please choose 1 for log in or 2 for sign up")


def display_success_story():
  print("College Student Success Story:")
  print("John Doe used InCollege to get his dream job at XYZ Company!")


# checks that searched person is a part of the database before allowing others to send a friend request and connect with them and updates pending friends list
def connect_with_people():
  f_first_name = input(
      "Who would you like to search for?\nEnter their first name: ")
  f_last_name = input("Enter their last name: ")

  if user_exists_by_first_name_last_name(f_first_name, f_last_name) is True:
    print("They are a part of the InCollege system")
    choice = input("Would you like to connect with someone? (y/n): ")

    if (choice == 'y' or choice == 'Y'):
      u_user_name = input("Enter your username: ")
      u_first_name = input("Enter your first name: ")
      u_last_name = input("Enter your last name: ")
      password = input("Enter your password: ")
      while (check_user_credentials(u_user_name, password) is False):
        print("Incorrect. Enter your information again\n")
        u_user_name = input("Enter your username: ")
        u_first_name = input("Enter your first name: ")
        u_last_name = input("Enter your last name: ")
        password = input("Enter your password: ")
      if check_user_credentials(u_user_name, password):
        f_user_name = input("Enter your friend's username: ")
        print("Friend request sent!")
        update_pending_list(u_user_name, f_user_name, f_first_name, f_last_name)
        #prints user's pending friends list
        print(db.collection("users").document(u_user_name).get().to_dict().get("pending_friends_list"))
        update_pending_list(f_user_name, u_user_name, u_first_name, u_last_name)

      
  

def play_video():
  print("Video is now playing")


def underConstruct():
  print("Under Construction")


# menu for General Links (a submenu for Useful Links)
def general_links():
  while True:
    print("\nGeneral Links:")
    print("1. Sign Up")
    print("2. Help Center")
    print("3. About")
    print("4. Press")
    print("5. Blog")
    print("6. Careers")
    print("7. Developers")
    print("8. Back")
    choice = input("Enter your choice: ")
    if choice == '1':
      chooseLogInSignUp()
    elif choice == '2':
      print("We're here to help!")
    elif choice == '3':
      print(
          "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
      )
    elif choice == '4':
      print(
          "In College Pressroom: Stay on top of the latest news, updates, and reports"
      )
    elif choice == '5' or choice == '6' or choice == '7':
      underConstruct()
    elif choice == '8':
      useful_links()
      break
    else:
      print("Invalid choice. Please try again.")


# menu for Useful Links (submenu for Main Menu)
def useful_links():
  while True:
    print("\nUseful Links:")
    print("1. General")
    print("2. Browse InCollege")
    print("3. Business Solutions")
    print("4. Directories")
    print("5. Back")
    choice = input("Enter your choice: ")
    if choice == '1':
      general_links()
    elif choice == '2' or choice == '3' or choice == '4':
      underConstruct()
    elif choice == '5':
      print("Back to Main Menu")
      break
    else:
      print("Invalid choice. Please try again.")


def copyright_notice():
  print("""
  @ 2024 InCollege USA, Inc. All rights reserved.
  """)


def about():
  print("""
  We are a group of dedicated college students aiming at making       
  networking more accessible for college students in hopes of making 
  the job search more simpler. The idea came to us as we knew how 
  difficult it is to find jobs through other apps that don't have as 
  many filters so we wanted to make one that specifically caters 
  towards students.
  """)


def accessibility():
  print("""
  SAMPLE:
  InCollege Accessibility Statement:
  InCollege is committed to ensuring digital accessibility for all 
  college students. We strive to continually improve the user 
  experience for everyone and apply the relevant accessibility 
  standards.

  **Accessibility Features:**
  - Our website is designed to be compatible with popular screen 
  readers.
  - Navigation is consistent and structured to facilitate easy access 
  to information.
  - Forms and controls are labeled for screen reader users.

  **Accessibility Feedback:**
  We welcome your feedback on the accessibility of InCollege. Please 
  let us know if you encounter accessibility barriers on our website 
  or if you have suggestions for improvement. You can reach us by:

  - Email: InCollege@gmail.com
  - Phone: 813-123-4567
  - Address: Tampa, FL

  **Date:**
  This statement was last updated on 2/17/24.

  InCollege is dedicated to providing an accessible and inclusive 
  online experience for all users. We appreciate your support as we 
  continue to enhance the accessibility features of our website.)
""")


def user_agree():
  print("""
  SAMPLE:
  InCollege User Agreement:

  Last Updated: 2/17/24

  Welcome to InCollege! By using our website or services, you agree to 
  comply with and be bound by the following terms and conditions. 
  Please read these terms carefully before accessing or using our 
  platform.

  1. Acceptance of Terms

  By accessing or using InCollege, you acknowledge that you have read, 
  understood, and agree to be bound by these terms of service. If you 
  do not agree to these terms, please do not use our services.

  2. User Eligibility

  You must be at least 18 years old to use our services. By using the 
  Platform, you represent and warrant that you meet the eligibility 
  criteria. If you are using the services on behalf of an organization, 
  you represent and warrant that you have the authority to bind the 
  organization to these terms.

  If you have any questions or concerns about these terms, please 
  contact us through email, phone, or mail.

  Thank you for using InCollege!""")


def update_gc(user_name, new_gc):
  user_ref = db.collection("users").document(user_name)
  user_ref.update({"guest_controls": new_gc})


def privacy_policy(user_name):
  while True:
    user_ref = db.collection("users").document(user_name)
    current_gc = user_ref.get().to_dict().get("guest_controls", {})

    print("""
    Below is a list of Guest Controls which InCollege may send updates and   
    information to you. By default, a user is opted into receiving these     
    notifications. If you would like to opt out of receiving these notifications, or 
    change your previous notification status, please select the corresponding 
    number from the list below. You may change your option at any time.
    1. InCollege Email
    2. SMS
    3. Targeted Advertising
    4. Back""")

    choice = input(
        """Please enter the option number for the Guest Control you'd
    like to change: """)

    if choice in ["1", "2", "3"]:
      control_name = "email" if choice == "1" else (
          "sms" if choice == "2" else "target_adv")
      current_ctrlname = current_gc.get(control_name, False)

      new_value = not current_ctrlname
      update_gc(user_name, {control_name: new_value})
      print("Guest Control updated successfully.")

    elif choice == "4":
      print("Exiting Guest Control Menu.")
      break
    else:
      print("Invalid option. Please try again.")


def cookie_policy():
  print("""
  SAMPLE:
  Cookie Policy:

  Effective Date: 2/17/24

  This Cookie Policy explains how InCollege uses cookies to provide and improve our 
  services. By using our website, you consent to the use of cookies as described in 
  this policy.

  What are Cookies?

  Cookies are small pieces of text sent to your web browser by a website you visit. 
  A cookie file is stored in your web browser and allows the service or a third- 
  party to recognize you and make your next visit easier and more useful to you.

  If you do not consent to the use of cookies, you should not use our website.

  For any inquiries about our Cookies Policy, please contact us through email, 
  phone, or mail. Thank you for using InCollege!
""")


def copyright_policy():
  print("""
  SAMPLE:
  Copyright Policy

  Effective Date: 2/17/24

  This Copyright Policy governs the use of the content on InCollege website and 
  outlines the terms and conditions under which users may use, share, and interact 
  with our content.

  1. Copyright Ownership

  All content on this website, including but not limited to text, graphics, logos, 
  images, videos, and other materials, is the property of InCollege and is 
  protected by applicable copyright laws.

  2. Permitted Use

  Users are granted a limited, revocable, non-exclusive license to access and use 
  the content for personal, non-commercial, and informational purposes only. This 
  license does not transfer ownership of any intellectual property rights.


  For any inquiries about our Copyright Policy, please contact us through email, 
  phone, or mail. Thank you for using InCollege!
  """)


def brand_policy():
  print("""
  SAMPLE:
  Brand Policy Statement:

  Effective Date: 2/17/24

  This Brand Policy governs the use of the brand elements of InCollege and 
  establishes guidelines for maintaining the integrity and consistency of our brand 
  identity.

  For any inquiries about our Copyright Policy, please contact us through email, 
  phone, or mail. Thank you for using InCollege!
  """)


# updates default language of English to English or Spanish
def update_language(user_name, updated_lang):
  if updated_lang in ["english", "English", "spanish", "Spanish"]:
    user_ref = db.collection("users").document(user_name)
    user_ref.update({"language": updated_lang})
    print("Language has been updated.")
  else:
    print("Invalid language. Please try again.")


# makes user login before accessing the Important Links menu
def enter_importantlinks():
  username = input("Please enter your username: ")
  password = input("Please enter your password: ")
  if check_user_credentials(username, password):
    important_links(username)
  else:
    again = input(
        "Invalid username or password. Would you like to try again?(y/n): ")
    if again == "y" or again == "Y":
      enter_importantlinks()
    elif again == "n" or again == "N":
      "Returning back to main menu..."
    else:
      print("Invalid Input. Please try again.")
      enter_importantlinks()


# menu for Important Links (submenu of Main Menu)
def important_links(user_name):
  while True:
    print("\nInCollege Important Links:")
    print("1. Copyright Notice")
    print("2. About")
    print("3. Accessibility")
    print("4. User Agreement")
    print("5. Privacy Policy")
    print("6. Cookie Policy")
    print("7. Copyright Policy")
    print("8. Brand Policy")
    print("9. Languages")
    print("10. Back")
    choice = input("Enter your choice: ")
    if choice == '1':
      copyright_notice()
    elif choice == '2':
      about()
    elif choice == '3':
      accessibility()
    elif choice == '4':
      user_agree()
    elif choice == '5':
      privacy_policy(user_name)
    elif choice == '6':
      cookie_policy()
    elif choice == '7':
      copyright_policy()
    elif choice == '8':
      brand_policy()
    elif choice == '9':
      lang = input("Enter the language you'd like to change to: ")
      update_language(user_name, lang)
    elif choice == '10':
      print('Exiting Important links Menu...')
      break
    else:
      print("Invalid choice. Please try again.")


"""
EPIC 4 included:
- editing the max number of users to 10
- editing sign_up_user, connect, and user_exist functions
- adding friends and pending list to database
"""


# updates list of pending friends requests of user w/ u_user_name
def update_pending_list(u_user_name, f_user_name, f_first_name, f_last_name):
  users_ref = db.collection("users").document(u_user_name)
  users_data = users_ref.get().to_dict()

  pending_list = users_data.get("pending_friends_list")    
  new_pending_list = {
      "pending_friends_list": pending_list,
      "user_name": f_user_name,
      "first_name": f_first_name,
      "last_name": f_last_name
  }
  
  users_ref.update({"pending_friends_list": new_pending_list})



# updates friends list of user w/ u_user_name
def update_friends_list(u_user_name, f_user_name, f_first_name, f_last_name):
  users_ref = db.collection("users").document(u_user_name)
  users_data = users_ref.get().to_dict()

  friends_list = users_data.get("friends_list")  
  new_friends_list = {
      "friends_list": friends_list,
      "user_name": f_user_name,
      "first_name": f_first_name,
      "last_name": f_last_name
  }
  #user_ref.update({"language": updated_lang})
  users_ref.update({"friends_list": new_friends_list})
  print(users_data.get("friends_list"))
  print("Friend added successfully!")


# Main Menu presented to user before and after logging in
def main_menu():
  while True:
    print("\nMain Menu:")
    print("1. Display College Student Success Story")
    print("2. Play a Video")
    print("3. Log in or Create Account")
    print("4. Connect with People")
    print("5. Post a Job")
    print("6. Useful Links")
    print("7. InCollege Important Links")
    print("8. Exit")

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
      create_job()
    elif choice == '6':
      useful_links()
    elif choice == '7':
      enter_importantlinks()
    elif choice == '8':
      print("Exiting program...")
      break
    else:
      print("Invalid choice. Please try again.")


if __name__ == "__main__":
  main_menu()
