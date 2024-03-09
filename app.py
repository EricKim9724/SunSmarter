import streamlit as st
import pandas as pd
from utils import recommender
from utils.recommender import sunscreen_recommend

# from utils.authorisation import Authenticator
# from utils.authorisation import authenticate
from utils.authentication import authenticate_user, register_user

# Sets the page configuration to wide by default
st.set_page_config(layout="wide")

# Logo, Title
col1, col2 = st.columns([1.5, 10])

with col1:
    st.image("./assets/logo.png", width=128)

with col2:
    title = """
            <p style="font-family:Helvetica; color:orange; font-size: 66px;">
                <b>SunSmarter</b>
                <span style= "font-family:Calibri; color:gray; font-size: 18px;">
                    Your Shield From UV Harm
                </span>
            </p>
            """
    st.markdown(title, unsafe_allow_html=True)
# login page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.title("Login to SunSmarter")
    with st.form("Login Form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            if authenticate_user(email, password):
                st.session_state["logged_in"] = True
                st.experimental_rerun()

        register_button = st.form_submit_button("Register")
        if register_button:
            if register_user(email, password):
                st.experimental_rerun()
else:
    # Currently 3 "Pages" but we can just use tabs
    tab_names = [
        ":world_map: UV Map",
        ":clipboard: Reminder History",
        ":orange_book: UV Impacts Handbook",
    ]
    tab1, tab2, tab3 = st.tabs(tab_names)
    css = """
    <style>
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: flex-end;
        }

        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:18px;
        font-weight: bold;
        }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    # tab1 is the main page w/ 2 colummns (UV Map, Recommenders)
    with tab1:
        padding = st.container(height=20, border=False)
        t1_col1, t1_col2 = st.columns(2)

        # UV Map
        with t1_col1:
            st.subheader("Search for a Location")
            default_location = None
            df = pd.DataFrame({"lat": [-37.91667], "lon": [145.11667]})
            text_search = st.text_input(
                "Location", value="", label_visibility="collapsed"
            )
            st.map(df, zoom=11, use_container_width=False)

        # Recommenders
        with t1_col2:

            # Start Outdoor Session Functionality
            st.subheader("Staying Sunsafe Outdoors")
            activity_type = st.selectbox(
                "Activity Type",
                (
                    "Swimming/Water Activity",
                    "High Intensity Sports",
                    "Low Intensity Sports",
                ),
                index=None,
                placeholder="Select Activity Type",
                label_visibility="collapsed",
            )
            sub_col1, sub_col2 = st.columns([3, 1])
            with sub_col1:
                st.button(
                    "Start Outdoor Session", type="primary", use_container_width=True
                )
            with sub_col2:
                st.toggle("Get Reminders", value=True)

            # Adjustable Slider for Recommendations
            st.subheader("UV Index")
            current_location_uv = 10
            uv_index = st.slider(
                "UV", 0, 12, value=current_location_uv, label_visibility="collapsed"
            )

        # Task 1.2 Clothing Recommender
        st.subheader("Clothing Recommender", divider="orange")
        clothing_advice, image_filenames = recommender.cloth_recommend(uv_index)
        st.write(clothing_advice)

        # Display the images if available
        if image_filenames:
            for filename in image_filenames.split(","):
                image_path = f"./assets/{filename}.png"  # Assuming images are stored in the assets folder with .jpg extension
                st.image(
                    image_path,
                    caption=f"{filename.capitalize()}",
                    use_column_width=True,
                    width=30,
                )
        else:
            st.write("No images available for this recommendation.")

        # Task 1.4 Sunscreen Recommender
        st.subheader("Sunscreen Recommender", divider="orange")
        st.markdown("**Please enter your height and weight below:**")
        user_height = st.slider("**Height (cm)**", 100, 250, 170)
        user_weight = st.slider("**Weight (kg)**", 30, 200, 70)

        # When calling the sunscreen_recommend function, pass the selected activity type to it
        sunscreen_usage_df = sunscreen_recommend(
            uv_index, user_height, user_weight, activity_type
        )
        # Display instructions for sunscreen application
        st.markdown(
            "**Apply before going outdoors:** Ensure skin is clean and dry before use and apply 20 minutes before going outdoors."
        )
        st.markdown(
            "**Reapply regularly:** Every two hours and immediately after swimming, sweating or toweling off."
        )
        st.markdown(
            "**Sunscreen does not provide 100% protection:** Wear a wide-brimmed hat, sunglasses, cover-ups and seek shade."
        )
        # Round the values in the sunscreen usage DataFrame to one decimal place
        sunscreen_usage_df = sunscreen_usage_df.round(1)
        # Display sunscreen usage information in tabular form
        st.write(sunscreen_usage_df)

    # Reminder History
    with tab2:
        padding = st.container(height=20, border=False)
        t2_col1, t2_col2 = st.columns(2)

        # Log of all reminders
        with t2_col1:
            st.subheader("UV Index")
            reminder_log = pd.DataFrame(
                {
                    "date_time": [
                        "2024-03-06 11:00:00",
                        "2024-03-06 13:00:00",
                        "2024-03-06 15:00:00",
                    ],
                    "received": ["Yes", "Ignored", "Yes"],
                }
            )
            st.dataframe(reminder_log, hide_index=True, use_container_width=True)

        # Visualisation of reminder history?
        with t2_col2:
            st.subheader("Summary: You had XX hours of sun exposure in the last week")
            st.subheader("Placeholder for Some data viz")

    # Reminder History
    with tab3:
        padding = st.container(height=20, border=False)
        t3_col1, t3_col2, t3_col3 = st.columns(3)

        # Cancer Risk Info
        with t3_col1:
            st.subheader("Dangers of Sun Exposure", divider="red")
            st.write("Placeholder")

        # Sun Safety Practices
        with t3_col2:
            st.subheader("Staying Sun Safe", divider="orange")
            st.write("Placeholder")

        # Sun Protection for Kids
        with t3_col3:
            st.subheader("Sun Safety for Kids", divider="rainbow")
            st.write("Placeholder")
