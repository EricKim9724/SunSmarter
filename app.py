import streamlit as st
import pandas as pd
from utils import recommender, weather, reminder
from utils.recommender import sunscreen_recommend
from utils.authentication import authenticate_user, register_user

# Sets the page configuration to wide by default
st.set_page_config(
    layout="wide", page_title="Sun Shield Advisor", page_icon=":sun_with_face:"
)

# Logo, Title
col1, col2 = st.columns([0.1, 10])

with col1:
    st.image("./assets/logo.png", width=96)

with col2:
    title = """
            <p style="font-family:recoleta-web; color: black; font-size: 4.5em;text-align: center;">
                SunShield Advisor
            </p>
            <p style="font-family:recoleta-web; color: gray; font-size: 1.2em;text-align: center;">
                Your shield from UV Harm
            </p>
            """
    st.markdown(title, unsafe_allow_html=True)


# login page
if False:
    pass

else:
    # Currently 3 "Pages" but we can just use tabs
    tab_names = [
        " :house: Home ",
        " :wrench: UV Tools",
        " :book: UV Impacts Handbook",
    ]
    home, tab2, tab3 = st.tabs(tab_names)
    css = """
    <style>
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: flex-end;
        }

        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.3em;
        font-family:recoleta-web;
        }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    with home:
        padding = st.container(height=10, border=False)
        home_img, text_col = st.columns([3, 1.5], gap="medium")
        with home_img:
            st.image("./assets/home.png", use_column_width=True)
            credit = """
            <p style="font-family:recoleta-web; color: gray; font-size: 0.8em;text-align: center">
                By Anna Tarazevich via https://www.pexels.com/photo/shirtless-man-with-sunscreen-7466770/
            </p>
            """
            st.markdown(credit, unsafe_allow_html=True)
        with text_col:
            padding2 = st.container(height=15, border=False)
            body1 = """
            <p style="font-family:recoleta-web; color: #393939; font-size: 2em;font-style: italic;text-align: center;font-weight: bold">
                Did you know?
            </p>
            """
            st.markdown(body1, unsafe_allow_html=True)
            padding2 = st.container(height=5, border=False)
            body2 = """
            <style>
                span{
                    font-weight: bold;
                    font-size: 1.2em;
                }
            </style>
            <p style="font-family:recoleta-web; color: #525252; font-size: 1.4rem;text-align: center;">
                Just <span>ONE</span> severe sunburn in childhood
            </p>
            <p style="font-family:recoleta-web; color: #FF4B4B; font-size: 4.2rem; font-weight: bold; text-align: center">
                DOUBLES
            </p>
            <p style="font-family:recoleta-web; color: #393939; font-size: 1.4rem; text-align: center;">
                likelihood of getting  <span>Skin Cancer</span>
            </p>
            """
            st.markdown(body2, unsafe_allow_html=True)
            padding2 = st.container(height=5, border=False)
            st.divider()
            body3 = """
            <p style="font-family:recoleta-web; color: #EA8C00; font-size: 2.2rem;text-align: center">
                Stay Sun-Safe
            </p>
            <p style="font-family:recoleta-web; color: #393939; font-size: 1.5rem;text-align: center">
                with Sun Shield Advisor
            </p>
            <p style="font-family:recoleta-web; color: gray; font-size: 1rem;text-align: center">
                Scroll down to find out more
            </p>
            """
            st.markdown(body3, unsafe_allow_html=True)
            st.divider()
            padding2 = st.container(height=10, border=False)

        padding2 = st.container(height=25, border=False)
        home_col1, home_col2 = st.columns([1.6, 3], gap="medium")
        with home_col1:
            body4 = """
            <p style="font-family:recoleta-web; color: #EA8C00; font-size: 2rem;font-weight: bold;text-align: center">
                Stay Protected Anywhere
            </p>
            <p style="font-family:recoleta-web; color: gray; font-size: 0.9rem;font-weight: italic;text-align: center">
                with our features like:
            </p>
            """
            st.markdown(body4, unsafe_allow_html=True)
            st.divider()
            padding2 = st.container(height=3, border=False)
            col1, col2, col3 = st.columns(3)
            col1.markdown(
                """
            <p style="font-family:Helvetica; color: #393939; font-size: 1rem;text-align: center">
                Live UV & Weather Updates by Location
            </p>

            """,
                unsafe_allow_html=True,
            )
            col2.markdown(
                """
            <p style="font-family:Helvetica; color: #393939; font-size: 1rem;text-align: center">
                Clothing & Sunscreen Recommenders
            </p style=text-align: center>
            """,
                unsafe_allow_html=True,
            )
            col3.markdown(
                """
            <p style="font-family:Helvetica; color: #393939; font-size: 1rem;text-align: center">
                Google Calendar Sunscreen Reminders*
            </p>
            """,
                unsafe_allow_html=True,
            )
            st.divider()
            html = """
            <p style="font-family:recoleta-web; color: #393939; font-size: 1.3rem;text-align: center">
                Try our Live UV Advice:
            </p>
            """
            st.markdown(html, unsafe_allow_html=True)
            col_text, col_searchabar = st.columns([1, 2.5])
            with col_text:
                text = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 0.8rem;text-align: center">
                        Search for a Location (Postcode/Surburb)
                    </p>
                     """
                st.markdown(text, unsafe_allow_html=True)
            with col_searchabar:
                text_search_1 = st.text_input(
                    "Location", value="Clayton", label_visibility="collapsed", key="xdd"
                )
            weather.display_location_weather(text_search_1, demo=True)

        with home_col2:
            padding2 = st.container(height=20, border=False)
            st.image("./assets/home_2.png", use_column_width=True)
            body5 = """
            <p style="font-family:recoleta-web; color: gray; font-size: 0.8rem;text-align: center">
                By Andrea Piacquadio via https://www.pexels.com/photo/cheerful-young-woman-resting-in-colorful-hammock-3771818/
            </p>
            """
            st.markdown(body5, unsafe_allow_html=True)

    padding = st.container(height=120, border=False)
    st.markdown(
        "<center>Copyright © 2024 SunShield Advisor. All rights reserved.</center>",
        unsafe_allow_html=True,
    )

    # tab2 is the main page w/ 2 colummns (UV Map, Recommenders)
    with tab2:
        col1, col2, col3 = st.columns([0.5, 1, 0.5])
        with col2:
            padding = st.container(height=20, border=False)
            st.session_state.user_email = " "

            padding = st.container(height=20, border=False)
            inter0 = """
                <p style="font-family:recoleta-web; color: #EA8C00; font-size: 2rem;text-align: center">
                    Ready to explore your sun-safe journey? Enter your location above and unlock a world of tailored advice to keep you protected from UV rays, all day long!
                </p>
                """
            st.markdown(inter0, unsafe_allow_html=True)
            padding = st.container(height=20, border=False)
            # UV Map
            st.subheader("Search for a Location")
            location_search = """
                <p style="font-family:recoleta-web; color: gray; font-size: 1rem;text-align: left">
                    Search for a Location (Postcode/Surburb) to get the latest UV Index and Weather Updates.
                </p>
                 """
            st.markdown(location_search, unsafe_allow_html=True)

            text_search = st.text_input(
                "Location", value="Clayton", label_visibility="collapsed"
            )
            weather.display_location_weather(text_search)
            # location_weather = weather.get_weather_data(-37.91667,145.11667)
            # weather.weather_display_ui("Clayton",location_weather)

            # Recommenders
            # Start Outdoor Session Functionality
            padding = st.container(height=150, border=False)
            inter1 = """
                <p style="font-family:recoleta-web; color: #EA8C00; font-size: 2rem;text-align: center">
                    Whether it's a day at the beach or a hike in the mountains, SunShield Advisor has you covered. Select your activity and let us remind you when it's time to reapply sunscreen.
                </p>
                """
            st.markdown(inter1, unsafe_allow_html=True)
            padding = st.container(height=40, border=False)
            with st.container(border=True):
                st.session_state.user_email = ""
                st.subheader("Staying Sunsafe Outdoors")
                choose_activity = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 1rem;text-align: left">
                        Choose your activity and get started with sunscreen reminders.
                    </p>
                     """
                st.markdown(choose_activity, unsafe_allow_html=True)
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

                if st.button(
                    "Start Outdoor Session: Get Sunscreen Reminders",
                    type="primary",
                    use_container_width=True,
                ):
                    st.caption("Unfortunately this feature is still under development")

            # Adjustable Slider for Recommendations
            padding = st.container(height=150, border=False)
            inter2 = """
                <p style="font-family:recoleta-web; color: #EA8C00; font-size: 2rem;text-align: center">
                    Discover the ideal clothing and sunscreen amount for your outdoor adventures. From hats to long sleeves, we'll help you stay sun safety!
                </p>
                """
            st.markdown(inter2, unsafe_allow_html=True)
            padding = st.container(height=40, border=False)
            with st.container(border=True):
                st.subheader("UV Index")
                slide_UV = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 1rem;text-align: left">
                        Slide to adjust the UV index to discover suitable clothing.
                    </p>
                     """
                st.markdown(slide_UV, unsafe_allow_html=True)
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
                sunscreen_amount = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 1rem;text-align: left">
                        Please enter your height and weight below:
                    </p>
                     """
                st.markdown(sunscreen_amount, unsafe_allow_html=True)
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
                with st.expander("Click for more details"):
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

        # Task 1.3 UV Impacts Handbook
        with tab3:
            padding = st.container(height=20, border=False)
            t3_col1, t3_col2, t3_col3 = st.columns(3)

            # Dangers of Sun Exposure
            with t3_col1:
                st.header("Skin cancer", divider="red")
                st.subheader("Dangers of Sun Exposure")

                st.image("./assets/skincancer.png")
                image1 = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 0.8em;text-align: center">
                        By cottonbro studio via https://www.pexels.com/zh-cn/photo/4974360/
                    </p>
                    """
                
                st.markdown(image1, unsafe_allow_html=True)
                skincancer_text3 = """

                More than 95% of skin cancers are caused by exposure to UV radiation.

                UV radiation most often comes from the sun. 

                - More than two in three Australians will be diagnosed with skin cancer in their lifetime.1
                - About 2,000 Australians die from skin cancer each year.
                - Australia has one of the highest rates of skin cancer in the world.
                - Medicare records show there were over a million treatments for squamous and basal cell carcinoma skin cancers in 2018 – that’s more than 100 skin cancer treatments every hour.
                """
                
                st.markdown(skincancer_text3)


            # UV Index & SPF
            with t3_col2:
                st.header("UV Index & SPF", divider="orange")

                uv_index_text2 = """
                #### What is the UV Index?

                The UV Index is a tool you can use to protect yourself from UV radiation. It tells you the times during the day that you need to be SunSmart.

                <b> The UV Index divides UV radiation levels into: </b>

                <div>
                    <p>- <b style='color: #A5DF00;'>low (1-2)</b></p
                    <p>- <b style='color: #D7DF01;'>moderate (3-5)</b></p
                    <p>- <b style='color: #DBA901;'>high (6-7)</b></p
                    <p>- <b style='color: #DF7401;'>very high (8-10)</b></p
                    <p>- <b style='color: #DF3A01;'>extreme (11 and above)</b></p.
                """

                st.markdown(uv_index_text2, unsafe_allow_html=True)

                st.image("./assets/spf.png")
                image2 = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 0.8em;text-align: center">
                        By RF._.studio via https://www.pexels.com/zh-cn/photo/suncsreen-3618606/
                    </p>
                    """
                st.markdown(image2, unsafe_allow_html=True)

                spf_text1 = """
                #### What is SPF?

                Sun Protection Factor(SPF) is a measure of how well a sunscreen will protect skin from UVB rays, the kind of radiation that causes sunburn, damages skin, and can contribute to skin cancer.

                <b>The SPF (Sun Protection Factor) scale is not linear:</b>

                - <b>SPF 15 blocks 93% of UVB rays</b>
                - <b>SPF 30 blocks 97% of UVB rays</b>
                - <b>SPF 50 blocks 98% of UVB rays</b>
                
                So, while you may not be doubling your level of protection, an SPF 30 will block half the radiation that an SPF 15 would let through to your skin. It’s complicated, but to keep it simple, most dermatologists recommend using a SPF 30 or higher.
                """
                st.markdown(spf_text1, unsafe_allow_html=True)

            # Sun Safety for Kids
            with t3_col3:
                st.header("Sun Safety for Kids", divider="rainbow")
                
                sp_kids_text2 = """
                #### Protect your child’s skin by:

                - Cover as much of your children’s skin as possible with loose-fitting clothes made from tightly-woven fabrics.
                - Slap on a broad brim, bucket or legionnaire style hat that protects the face, ears and back of the neck. Hats are available for babies that crumple easily when they put their head down.
                - Provide shade for prams and strollers.
                - Plan the day’s activities to reduce your children’s exposure to the sun, especially between 10am and 2pm (11am and 3pm in daylight saving time).
                - Stay in the shade as much as possible. Even in the shade, use other forms of sun protection to reduce exposure from reflected UV radiation from surfaces such as sand or concrete.
                - Apply SPF30+ or higher, broad-spectrum and water-resistant sunscreen on any exposed areas of skin.
                """
                st.markdown(sp_kids_text2, unsafe_allow_html=True)

                st.image("./assets/kids.png")
                image2 = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 0.8em;text-align: center">
                        By Kindel Media via https://www.pexels.com/zh-cn/photo/8215112/
                    </p>
                    """
                st.markdown(image2, unsafe_allow_html=True)
