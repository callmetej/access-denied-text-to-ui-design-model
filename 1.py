import streamlit as st
from ui_generation_logic import generate_ui_from_description  # Import the backend logic

# Page Configuration
st.set_page_config(
    page_title="AI Product Idea Generator",
    page_icon="✨",
    layout="wide"
)

# Initialize session state for user authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Authentication Functions
def show_sign_in_page():
    st.title("Sign In")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Sign In"):
        if username == "admin" and password == "password123":
            st.session_state["authenticated"] = True
            st.success("Sign In Successful!")
            st.rerun()  # Corrected from st.experimental_rerun() to st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")

def show_sign_up_page():
    st.title("Sign Up")
    username = st.text_input("Choose a Username", placeholder="Enter a username")
    password = st.text_input("Choose a Password", type="password", placeholder="Enter a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

    if st.button("Sign Up"):
        if password == confirm_password:
            st.success("Sign Up Successful! Please Sign In to continue.")
            st.session_state["authenticated"] = False
            st.rerun()  # Corrected from st.experimental_rerun() to st.rerun()
        else:
            st.error("Passwords do not match. Please try again.")

# Main App Content
def show_main_app():
    # Main App Container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Title and Subtitle
    st.markdown('<div class="title">AI Product Idea Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Transform your product ideas into stunning visual concepts with the power of AI.</div>', unsafe_allow_html=True)

    # User Input and Generate Button
    user_input = st.text_input("Enter your product idea", placeholder="Enter your product idea (e.g., A personal finance tracker for students)")
    if st.button("✨ Generate ✨"):
        if user_input.strip():
            with st.spinner("Creating your concept..."):
                result = generate_ui_from_description(user_input)
                screenshot = result.get("screenshot")
                if screenshot:
                    st.image(screenshot, caption="Generated Concept", use_column_width=True)
                else:
                    st.error("Oops! Something went wrong. Please try again.")
        else:
            st.error("Please provide a valid product idea.")

    # Footer
    st.markdown('<div class="footer">Crafted with ❤️ | Powered by <a href="#">Streamlit</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Authentication Navigation
if not st.session_state["authenticated"]:
    option = st.sidebar.radio("Navigation", ["Sign In", "Sign Up"])
    if option == "Sign In":
        show_sign_in_page()
    else:
        show_sign_up_page()
else:
    # Show the main app if authenticated
    show_main_app()
