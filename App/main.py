import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# Import page modules
from home import show_home_page
from visualizations import show_visualizations_page
from predictions import show_predictions_page
from explainable_ai import show_explainable_ai_page
import gdown

# Set page configuration to wide mode
st.set_page_config(
    layout="wide", 
    page_title="Health Commodity Dashboard",
    page_icon="💊"
)

# Apply custom CSS styling
def load_css():
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Try to load CSS, create default if file doesn't exist
# try:
#     load_css()
# except FileNotFoundError:
#     st.warning("styles.css not found. Default styling will be applied.")

# Add background color to the main content
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Customize sidebar styling */
    .css-1d391kg, .css-1lsmgbg {
        background-color: #2c3e50;
    }
    
    /* Customize sidebar text */
    .css-1d391kg p, .css-1lsmgbg p {
        color: white !important;
    }
    
    /* Customize option menu */
    .nav-link {
        font-weight: 500 !important;
        border-radius: 5px !important;
        margin-bottom: 5px !important;
    }
    
    .nav-link.active {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    
    /* Fix for navigation title and icon */
    .nav-menu-title, .nav-menu-icon {
        color: white !important;
    }
    
    /* Additional styling */
    .stSelectbox label, .stNumberInput label {
        font-weight: 500;
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    file_id = "1Oj2n3_DcJVk7q6Cn0v2TNamgP9unnUpi"
    url = f"https://drive.google.com/uc?id={file_id}"


    output = "downloaded_file.csv"
    gdown.download(url, output, quiet=False)

    # Read the CSV file
    df = pd.read_csv(output)
    # Drop 'Unnamed: 0' column if it exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    df["period"] = pd.to_datetime(df["period"], errors="coerce")
    df["year"] = df["period"].dt.year
    df["month"] = df["period"].dt.month
    df["quarter"] = df["period"].dt.to_period("Q").astype(str)
    return df

# Load the data once for all pages
df = load_data()

# Sidebar Navigation with custom styling
with st.sidebar:
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #2c3e50;
        }
        
        div[data-testid=stSidebarUserContent] {
            padding-top: 1rem;
        }
        
        .sidebar-title {
            color: white;
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    selected_page = option_menu(
        "Navigation", ["Home", "Visualizations", "Predictions", "Explainable AI"],
        icons=["house-fill", "bar-chart-fill", "lightbulb-fill", "info-circle-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#2c3e50"},
            "icon": {"color": "orange", "font-size": "18px"}, 
            "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "#4CAF50"},
            "menu-title": {"color": "white"},  # Make menu title text white
            "menu-icon": {"color": "white"},   # Make menu icon white
        }
    )
    
    # Add dashboard info
    st.markdown("---")
    st.markdown('<p style="color: white; opacity: 0.7; font-size: 0.9em;">Health Commodity Dashboard v1.0</p>', unsafe_allow_html=True)

# Route to the selected page
if selected_page == "Home":
    show_home_page(df)
elif selected_page == "Visualizations":
    show_visualizations_page(df)
elif selected_page == "Predictions":
    show_predictions_page(df)
elif selected_page == "Explainable AI":
    show_explainable_ai_page(df)