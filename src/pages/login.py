from src.utils.dependancies import *
from src.utils.database_operations import Database
from src.utils.util import send_email

db = Database()
db.connect()
db.create_table()

def get_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    user_input = st.radio('Please select an option:', options=['Sign In', 'Sign Up'], horizontal=True)
    
    if user_input == 'Sign In':
        sign_in()
        if get_session_state().user:
            user_dashboard()
    
    elif user_input == 'Sign Up':
        sign_up()

def generate_reset_token():
    return secrets.token_urlsafe(32)

def send_reset_email(email, token):
    if(send_email(email, token)):
        st.success("Password reset link sent to your email. Check your inbox or spam.")
    else:
        st.error(f"Error sending email")


def user_dashboard():
    st.title("User Dashboard")
    st.subheader("User Details")

    user = st.session_state.user
    st.write(f"First Name: {user[1]}")
    st.write(f"Last Name: {user[2]}")
    st.write(f"Email: {user[4]}")
    st.write(f"Date of Birth: {user[3]}")

    st.subheader("Update User Details")

    change_first_name = st.checkbox("Want to change your First Name?")

    if change_first_name:
        changefname = st.text_input("Enter your new First Name")
        
        changeb = st.button("Change First Name")
        if changeb:
            db.update_first_name(changefname, st.session_state.user[0])
            st.success("Updated Successfully")

    change_last_name = st.checkbox("Want to change your Last Name?")

    if change_last_name:
        changelname = st.text_input("Enter your new Last Name")
        changel = st.button("Change Last Name")
        if changel:
            db.update_last_name(changelname, st.session_state.user[0])
            st.success("Updated Successfully")

    change_first_name = st.checkbox("Want to change your DOB?")

    if change_first_name:
        changedob = st.text_input("Enter your new Date of Birth (YYYY-MM-DD)")
        
        changed = st.button("Change DOB")
        if changed:
            db.update_dob(changedob, st.session_state.user[0])
            st.success("Updated Successfully")


    st.subheader("Actions")
    passbutton = st.checkbox("Change Password")

    if passbutton:
        oldpass = st.text_input("Enter your old password", type="password")
        newpass = st.text_input("Enter your new password", type="password")
        connpass = st.text_input("Confirm your new password", type="password")
        changep = st.button("Change")
        if changep:
            if hash_password(oldpass) != st.session_state.user[5]:
                st.error("Old password doesn't match")
            else:
                if newpass != connpass:
                    st.error("New and Confirm password don't match")
                else:
                    hashpass = hash_password(newpass)
                    db.update_password(hashpass, st.session_state.user[0])
                    st.success("Password Updated Successfully")


def sign_in():
    st.header('User Login')
    email_login = st.text_input('Enter your email:', placeholder="abc123@email.com")
    password_login = st.text_input('Enter your Password:', placeholder="Password", type="password")

    forgot_password = st.checkbox("Forgot Password")

    if forgot_password:
        email_forgot = st.text_input("Enter your registered Gmail account:")
        if st.button("Reset Password"):
            
            user = db.select_user(email_forgot)

            if user:
                
                reset_token = generate_reset_token()
                reset_expiration = datetime.now() + timedelta(hours=1)

                db.update_reset_token(reset_token, reset_expiration, email_forgot)

                
                send_reset_email(email_forgot, reset_token)

                st.session_state.user = user

            else:
                st.error("Email not found. Please enter a registered Gmail account.")
    else:
        if st.button("Login"):
        
            hashed_login_password = hash_password(password_login)

            user = db.login(email_login, hashed_login_password)

            if user:
                st.session_state.user = user
                st.success("Login successful.")
                return user
            else:
                st.error("Invalid email or password.")
                return None
            
def sign_up():
    st.header('Create a new Account')
    first_name = st.text_input('Enter your First Name:')
    last_name = st.text_input("Enter your Last Name:")
    dob = st.text_input('Enter your DOB(YYYY-MM-DD):', placeholder="01/01/1980")
    email_reg = st.text_input('Enter your email account:', placeholder="abc123@gmail.com")
    password_reg = st.text_input('Enter your password:', type="password")
    confirm_password = st.text_input('Confirm your password:', type="password")
    register=st.button('Register')

    if register == True:
        if password_reg != confirm_password:
            st.error('Passwords do not match. Please try again.')
        
        elif not email_reg.endswith('@gmail.com'):
            st.error('Please register with a Gmail account.')
        else:
            hashed_password = hash_password(password_reg)

            try:
                db.insert_user(first_name, last_name, dob, email_reg, hashed_password)

                st.success(f"Registration successful for {email_reg}!")
            
            except IntegrityError:
                    st.error(f"Email {email_reg} is already registered. Please use a different email.")