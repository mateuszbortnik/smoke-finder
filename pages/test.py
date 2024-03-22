import streamlit as st
import streamlit_authenticator as stauth


username = st.secrets['auth_username']
email = st.secrets['email']
name = st.secrets['auth_name']
password = st.secrets['auth_password']

# Creating the credentials dictionary
credentials = {
    'usernames': {
        username: {
            'email': email,
            'name': name,
            'password': password,
            # 'logged_in' is not included as it will be managed automatically
        }
    }
}

# Your configuration for cookie and preauthorized users (replace with your actual values)
cookie_config = {
    'expiry_days': 30,
    'key': 'some_signature_key',  # Replace with your actual key
    'name': 'some_cookie_name'  # Replace with your actual cookie name
}

# Instantiate the authenticator
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name=cookie_config['name'],
    key=cookie_config['key'],
    cookie_expiry_days=cookie_config['expiry_days'],
    # Include preauthorized or validator if necessary
)

name, authentication_status, username = authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')