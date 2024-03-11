import streamlit as st
import pandas as pd
from utils import recommender, weather
from utils.recommender import sunscreen_recommend
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
                <b>SunShieldAdvisor</b>
                <span style= "font-family:Calibri; color:gray; font-size: 18px;">
                    Your Shield From UV Harm
                </span>
            </p>
            """
    st.markdown(title, unsafe_allow_html=True)


# login page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.title("Login to SunShieldAdvisor")
    with st.form("Login Form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            if authenticate_user(email, password):
                st.session_state["logged_in"] = True
                st.write(st.session_state["logged_in"])
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
            text_search = st.text_input(
                "Location", value="Clayton", label_visibility="collapsed"
            )
            weather.display_location_weather(text_search)
            # location_weather = weather.get_weather_data(-37.91667,145.11667)
            # weather.weather_display_ui("Clayton",location_weather)

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
            st.button("Start Outdoor Session", type="primary", use_container_width=True)

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
            with st.expander("See Visual Recommendations"):
                if image_filenames:
                    for filename in image_filenames.split(","):
                        image_path = f"./assets/{filename}.png"  # Assuming images are stored in the assets folder with .jpg extension
                        st.markdown(
                            """
                            <style>
                                button[title^=Exit]+div [data-testid=stImage]{
                                    text-align: center;
                                    display: block;
                                    margin-left: auto;
                                    margin-right: auto;
                                    width: 100%;
                                }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.image(
                            image_path,
                            caption=f"{filename.capitalize()}",
                            use_column_width=False,
                            width=300,
                        )
                else:
                    st.write("No images available for this recommendation.")

            # Task 1.4 Sunscreen Recommender
            st.subheader("Sunscreen Recommender", divider="orange")
            st.markdown("**Please enter your height and weight below:**")
            sub_col3, sub_col4 = st.columns([3, 1])
            with sub_col3:
                user_height = st.slider("**Height (cm)**", 100, 250, 170)
            with sub_col4:
                user_weight = st.slider("**Weight (kg)**", 30, 200, 70)

            # When calling the sunscreen_recommend function, pass the selected activity type to it
            sunscreen_usage_df = sunscreen_recommend(
                uv_index, user_height, user_weight, activity_type
            ).round(1)
            # Display instructions for sunscreen application
            total_sunscreen = sunscreen_usage_df["Sunscreen Usage (ml)"].sum()
            st.markdown(
                f"**Recommendation: Apply {total_sunscreen:.1f}ml of Sunscreen**"
            )
            with st.expander("See more details"):
                st.markdown(
                    "**Apply before going outdoors:** Ensure skin is clean and dry before use and apply 20 minutes before going outdoors."
                )
                st.markdown(
                    "**Reapply regularly:** Every two hours  and immediately after swimming, sweating or toweling off."
                )
                st.markdown(
                    "**Sunscreen does not provide 100% protection:** Wear a wide-brimmed hat, sunglasses, cover-ups and seek shade."
                )
                # Add SPF Recommendation
                if uv_index >= 0 and uv_index <= 2:
                    st.markdown(
                        "**SPF Recommendation:** SPF 5-8 sunscreen is recommended."
                    )
                elif uv_index >= 3 and uv_index <= 5:
                    st.markdown(
                        "**SPF Recommendation:** SPF 15-30 sunscreen is recommended."
                    )
                elif uv_index >= 6 and uv_index <= 7:
                    st.markdown(
                        "**SPF Recommendation:** SPF 30-50 sunscreen is recommended."
                    )
                elif uv_index >= 8 and uv_index <= 10:
                    st.markdown(
                        "**SPF Recommendation:** SPF 50+ sunscreen is recommended."
                    )
                else:
                    st.markdown(
                        "**SPF Recommendation:** SPF 50+ sunscreen is strongly recommended, along with additional protective measures."
                    )
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
                st.subheader(
                    "Summary: You had XX hours of sun exposure in the last week"
                )
                st.subheader("Placeholder for Some data viz")

        # Task 1.3 UV Impacts Handbook
        with tab3:
            padding = st.container(height=20, border=False)
            t3_col1, t3_col2, t3_col3 = st.columns(3)

            # Cancer Risk Info
            with t3_col1:
                st.subheader("Dangers of Sun Exposure", divider="red")
                st.write(
                    "There is well established evidence that exposure to ultraviolet radiation (UVR) from the sun can lead to skin cancer and eye damage. For best protection use a combination of sun protection measures."
                )
                st.write(
                    "Australia has one of the highest rates of skin cancer in the world. At least two in three Australians will be diagnosed with skin cancer by the age of 70. The major cause of skin cancer is exposure to ultraviolet (UV) radiation from the sun."
                )
                st.write(
                    "Fortunately, UV induced skin cancer is almost entirely preventable and high profile awareness and information campaigns telling Australians how to save their skin have been in place for several decades."
                )
                st.markdown(
                    """[Prevention policy](https://www.cancer.org.au/about-us/policy-and-advocacy/prevention-policy).""",
                    unsafe_allow_html=False,
                )
                st.markdown(
                    """[National Cancer Care Policy](https://www.cancer.org.au/about-us/policy-and-advocacy/national-cancer-care-policy).""",
                    unsafe_allow_html=False,
                )
                st.markdown(
                    """[Early detection policy](https://www.cancer.org.au/about-us/policy-and-advocacy/early-detection-policy).""",
                    unsafe_allow_html=False,
                )
                st.markdown(
                    """[Private ownership and use of solariums in Australia](https://www.cancer.org.au/about-us/policy-and-advocacy/position-statements/uv/private-solariums).""",
                    unsafe_allow_html=False,
                )

            # Sun Safety Practices
            with t3_col2:
                st.subheader("Staying Sun Safe", divider="orange")
                st.write(
                    "Overexposure to ultraviolet (UV) light causes 95% of melanomas. The best way to prevent melanoma is to protect your skin from the sun by following the 5 Sun Safe Rules:"
                )
                st.image("./assets/5 Sun Safe Rules.png")

            # Sun Protection for Kids
            with t3_col3:
                st.subheader("Sun Safety for Kids", divider="rainbow")
                st.write(
                    "Babies and children are at particular risk of sunburn and skin damage because of their delicate skin. Exposure to UV radiation during the first 15 years of life greatly increases the risk of developing skin cancer later in life."
                )
                st.write(
                    "Your child's sensitive skin is especially vulnerable to UV radiation. Cancer Council NSW recommends that children under the age of 12 months are not exposed to direct sunlight when UV levels are 3 and above. You can check your local UV levels and the recommended sun protection times (when UV levels are 3 and above) using the free SunSmart app or weather section of most newspapers."
                )
                st.image("./assets/sun safety for kids 1.png")
                st.image("./assets/sun safety for kids 2.png")
                st.image("./assets/sun safety for kids 3.png")
