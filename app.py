import streamlit as st
import pandas as pd
from utils import recommender, weather, reminder
from utils.recommender import sunscreen_recommend
from utils.authentication import authenticate_user, register_user

# Sets the page configuration to wide by default
st.set_page_config(
    layout="wide",
    page_title="Sun Shield Advisor",
    page_icon=":sun_with_face:")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

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


# login page (Temporarily Disabled)
if False: #"logged_in" not in st.session_state or not st.session_state["logged_in"]:
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
        " :house: Home ",
        " :wrench: UV Tools",
        " :book: UV Impacts Handbook",
    ]
    tab1, tab2, tab3 = st.tabs(tab_names)
    css = """
    <style>
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: flex-end;
        }

        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.5em;
        font-family:recoleta-web;
        }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    with tab1:
        padding = st.container(height=10, border=False)
        home_img, text_col = st.columns([3, 1.5],gap="medium")
        with home_img:
            st.image("./assets/home.png",use_column_width=True)
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
            <p style="font-family:recoleta-web; color: #FF4B4B; font-size: 4.2rem; font-weight: bold; text-align: center;font-style: italic">
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
        home_col1,home_col2 = st.columns([1.6,3], gap = "medium")
        with home_col1:
            body4 = """
            <p style="font-family:recoleta-web; color: #393939; font-size: 2.2rem;font-weight: bold;text-align: center">
                Stay Protected Anywhere
            </p>
            <p style="font-family:recoleta-web; color: gray; font-size: 1rem;font-weight: italic;text-align: center">
                with our features like:
            </p>
            """
            st.markdown(body4, unsafe_allow_html=True)
            st.divider()
            padding2 = st.container(height=3, border=False)
            col1, col2, col3 = st.columns(3)
            col1.markdown("""
            <p style="font-family:Helvetica; color: #393939; font-size: 1rem;text-align: center">
                Live UV & Weather Updates by Location
            </p>
            """, unsafe_allow_html=True)
            col2.markdown("""
            <p style="font-family:Helvetica; color: #393939; font-size: 1rem;text-align: center">
                Clothing & Sunscreen Recommenders
            </p>
            """, unsafe_allow_html=True)
            col3.markdown("""
            <p style="font-family:Helvetica; color: #393939; font-size: 1rem;text-align: center">
                Google Calendar Sunscreen Reminders
            </p>
            """, unsafe_allow_html=True)
            st.divider()
            col_text, col_searchabar = st.columns([1,2.5])
            with col_text:
                text = """
                    <p style="font-family:recoleta-web; color: gray; font-size: 0.8rem;text-align: center">
                        Search for a Location (Postcode/Surburb)
                    </p>
                     """
                st.markdown(text, unsafe_allow_html=True)
            with col_searchabar:
                text_search = st.text_input(
                    "Location", value="Clayton", label_visibility="collapsed", key = "demo"
                )
            weather.display_location_weather(text_search, True)
            
        with home_col2:
            st.image("./assets/home_2.png",use_column_width=True)
            body5 = """
            <p style="font-family:recoleta-web; color: gray; font-size: 0.8rem;text-align: center">
                By Andrea Piacquadio via https://www.pexels.com/photo/cheerful-young-woman-resting-in-colorful-hammock-3771818/
            </p>
            """
            st.markdown(body5, unsafe_allow_html=True)
            

    # tab1 is the main page w/ 2 colummns (UV Map, Recommenders)
    with tab2:
        padding = st.container(height=20, border=False)
        st.session_state.user_email = " "
        t1_col1, t1_col2 = st.columns(2)

        # UV Map
        with t1_col1:
            st.subheader("Search for a Location")
            text_search = st.text_input(
                "Location", value="Clayton", label_visibility="collapsed"
            )
            weather.display_location_weather(text_search)

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
                if activity_type not in [
                    "Swimming/Water Activity",
                    "High Intensity Sports",
                    "Low Intensity Sports",
                ]:
                    st.write("Please Select an Activity First")
                else:
                    if st.toggle("Get Reminders: Outdoor Session"):
                        st.session_state.user_email = reminder.start_outdoor_session(
                            activity_type
                        )

            with sub_col2:
                with st.popover(":clipboard: Reminder History"):
                    reminder.display_reminder_history(st.session_state.user_email)

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

        # Task 1.3 UV Impacts Handbook
        with tab3:
            padding = st.container(height=20, border=False)
            t3_col1, t3_col2, t3_col3 = st.columns(3)

            # Dangers of Sun Exposure
            with t3_col1:
                st.header("Dangers of Sun Exposure", divider="red")
                st.subheader("Skin cancer")
                skincancer_text1 = """
                #### About skin cancer

                Skin cancer can hide in plain sight and in places we might not expect.

                UV radiation causes damage to the skin cells DNA and can mutate into cancer that can spread to different parts of your body, such as the liver, lung and brain. In rare cases skin cancer can become deadly within six weeks.

                Although we can’t feel or see UV radiation, we can see UV damage to our skin as it changes colour –- which could be red from sunburn or what people often call a ‘tan’. At any time, skin cancer signs will also become visible, in the form of new spots, changes in colour or shape of existing spots.

                """
                st.markdown(skincancer_text1)

                st.image("./assets/skincancer.png")

                skincancer_text2 = """
                #### Know your skin

                More than 70% of skin cancers are diagnosed by people other than health professionals. As you can see and are familiar with your skin, you are more likely to detect skin cancer. That’s why it’s important to get to know your skin and check it regularly.

                If you detect or notice changes to your skin, and see your doctor at an earlier, more easily treatable stage, you can enjoy more of what life has the offer.
                
                #### What is skin cancer?

                Skin cancer is the uncontrolled growth of abnormal cells in the skin. 

                The three main types of skin cancer are basal cell carcinoma (BCC), squamous cell carcinoma (SCC) and melanoma. BCC and SCC are also called non-melanoma skin cancer or keratinocyte cancer, while they are more common than melanoma treatment for any type of skin cancer can be painful, leading to ongoing treatment requirements and life-long surveillance.
                """
                st.markdown(skincancer_text2)

                st.image("./assets/melanoma.png")

                skincancer_text3 = """
                #### What causes skin cancer?

                More than 95% of skin cancers are caused by exposure to UV radiation.

                UV radiation most often comes from the sun, but it can also come from artificial sources, such as arc welders, glue curing lights for artificial nails, and solariums.

                Solariums are now banned for commercial use in Australia as research shows that people who use solariums have a much greater risk of developing skin cancer.

                #### Skin cancer statistics

                - More than two in three Australians will be diagnosed with skin cancer in their lifetime.1
                - About 2,000 Australians die from skin cancer each year.2
                - Australia has one of the highest rates of skin cancer in the world.3
                - Medicare records show there were over a million treatments for squamous and basal cell carcinoma skin cancers in 2018 – that’s more than 100 skin cancer treatments every hour.
                - Basal and squamous cell carcinoma skin cancers accounted for one quarter of all cancer-related hospitalisations in 2014–15.4 The cost to the health system of these skin cancers alone is estimated to be more than $700 million annually. The costs to the Federal Government and the community from basal and squamous cell carcinomas are predicted to continue to increase in the future.5
                - In 2021, 2,824 Victorians were diagnosed with melanoma and 291 lost their lives.6
                - It is estimated that approximately 200 melanomas and 34,000 other skin cancer types per year are caused by occupational exposures in Australia.
                """
                st.markdown(skincancer_text3)

            # UV Index & SPF
            with t3_col2:
                st.header("UV Index & SPF", divider="orange")
                uv_index_text1 = """
                #### What is UV radiation?

                Ultraviolet (UV) radiation is the invisible killer that you can't see or feel. UV radiation can be high even on cool and overcast days. This means you can't rely on clear skies or high temperatures to determine when you need to protect yourself from the sun
                UV is a form of energy produced by the sun. The sun produces different types of energy:

                - Visible light – which we can see as sunlight.
                - Infrared radiation – which we feel as heat.
                - UV radiation – which we cannot see or feel.

                UV radiation is often confused with infrared radiation. The temperature, however, does not affect UV radiation levels. UV radiation can be just as high on a cool or even cold day as it is on a hot one, especially if skies are clear. Thick cloud provides a good filter, but UV radiation can penetrate thin cloud cover. And while UV radiation is higher in summer than in winter, it is still present every day of the year.
                
                There are three types of UV radiation, categorised by wavelength: UVA, UVB and UVC.

                - UVA can cause sunburn, DNA (cell) damage in the skin and skin cancer.
                - UVB causes skin damage and skin cancer. Ozone stops most UVB from reaching the earth’s surface, about 15% is transmitted.
                - UVC is the most dangerous type of UV. Ozone in the atmosphere absorbs all UVC and it does not reach the earth’s surface.
                
                UV levels are affected by a number of factors including geographic location, altitude, time of day, time of year and cloud cover. This means that UV levels are higher in some parts of Australia than others even on the same day.
                """

                st.markdown(uv_index_text1)

                uv_index_text2 = """
                #### What is the UV Index?

                The UV Index is a tool you can use to protect yourself from UV radiation. It tells you the times during the day that you need to be SunSmart.

                The UV Index divides UV radiation levels into:

                - low (1-2)
                - moderate (3-5)
                - high (6-7)
                - very high (8-10)
                - extreme (11 and above).
                
                Sun protection times are issued by the Bureau of Meteorology when the UV Index is forecast to reach 3 or above. At that level, it can damage your skin and lead to skin cancer. Sunscreen should be incorporated into your daily routine on these days.
                """

                st.markdown(uv_index_text2)

                uv_index_text3 = """
                #### When should I use the UV Index?

                Look or listen for the UV Index when you are:

                - planning or participating in an outdoor activity or event
                - undertaking recreational activities such as running, swimming, cycling or team sports
                - watching a spectator sport, such as tennis or cricket
                - working outdoors, or have responsibility for outdoor workers, or
                - responsible for young children and their outdoor activities.

                If sun protection times have been issued, you need to protect yourself during the times indicated.
                """

                st.markdown(uv_index_text3)

                st.image("./assets/spf.png")

                spf_text1 = """
                #### What is SPF?

                Sun Protection Factor(SPF) is a measure of how well a sunscreen will protect skin from UVB rays, the kind of radiation that causes sunburn, damages skin, and can contribute to skin cancer.

                The SPF (Sun Protection Factor) scale is not linear:

                - SPF 15 blocks 93% of UVB rays
                - SPF 30 blocks 97% of UVB rays
                - SPF 50 blocks 98% of UVB rays
                
                So, one way of looking at this is that SPF 30 sunscreen only gives you 4% more protection than SPF 15 sunscreen. Or:

                - SPF 15 (93% protection) allows 7 out of 100 photons through
                - SPF 30 (97% protection) allows 3 out of 100 photons through.

                So, while you may not be doubling your level of protection, an SPF 30 will block half the radiation that an SPF 15 would let through to your skin. It’s complicated, but to keep it simple, most dermatologists recommend using a SPF 30 or higher.
                """
                st.markdown(spf_text1)

            # Sun Safety for Kids
            with t3_col3:
                st.header("Sun Safety for Kids", divider="rainbow")
                sp_kids_text1 = """
                Babies and children are at particular risk of sunburn and skin damage because of their delicate skin. Exposure to UV radiation during the first 15 years of life greatly increases the risk of developing skin cancer later in life.

                Your child's sensitive skin is especially vulnerable to UV radiation. Cancer Council NSW recommends that children under the age of 12 months are not exposed to direct sunlight when UV levels are 3 and above. You can check your local UV levels and the recommended sun protection times (when UV levels are 3 and above) using the free SunSmart app or weather section of most newspapers.

                """

                st.markdown(sp_kids_text1)

                st.image("./assets/kids.png")

                sp_kids_text2 = """
                #### Protect your child’s skin by:

                - Cover as much of your children’s skin as possible with loose-fitting clothes made from tightly-woven fabrics.
                - Slap on a broad brim, bucket or legionnaire style hat that protects the face, ears and back of the neck. Hats are available for babies that crumple easily when they put their head down.
                - Provide shade for prams and strollers.
                - Plan the day’s activities to reduce your children’s exposure to the sun, especially between 10am and 2pm (11am and 3pm in daylight saving time).
                - Stay in the shade as much as possible. Even in the shade, use other forms of sun protection to reduce exposure from reflected UV radiation from surfaces such as sand or concrete.
                - Apply SPF30+ or higher, broad-spectrum and water-resistant sunscreen on any exposed areas of skin.
                
                #### Using sunscreen on babies and children

                Cancer Council recommends protecting babies and children’s skin with physical barriers such as wraps, clothing, hats and using shade as much as possible. If your baby or child is going to be exposed to the sun, apply sunscreen to those small areas of skin not covered by wraps, clothing and a hat.
                
                Babies aged under 6 months have highly absorptive skin and the Australasian College of Dermatologist recommends minimising use of sunscreen. Always usage test any product first on a small area of your baby or child’s skin for any negative reactions and apply sunscreen to those areas of exposed skin that can’t be covered with hats and clothing. If your baby or child reacts to sunscreen, seek advice from your doctor or chemist.

                #### When you’re out and about:

                - Check your children often to ensure they are well protected. Adjust covers on prams and strollers to make sure babies remain shaded.
                - Encourage your children to play in the shade. Remember even in shade, scattered or reflected UV radiation can cause skin damage.
                - Keep children’s hats on.
                - Reapply sunscreen every two hours or more often if wiped or washed off.
                - Be a role model for your child and practice good sun protection behaviors yourself.
                """

                st.markdown(sp_kids_text2)
                st.image("./assets/sun safety for kids 3.png")
