import streamlit as st
import pandas as pd

#Sets the page configuration to wide by default
st.set_page_config(layout  = "wide")

col1,col2 = st.columns([1.5,10])

with col1:
    st.image("logo.png",width = 128)
with col2:
    st.header ("SunSmarter: Your Shield Against UV Harm") 

tab_names = ["UV Map", "Reminder History", "UV Impacts Handbook"]
tab1, tab2, tab3 = st.tabs(tab_names)

with tab1:
    t1_col1, t1_col2 = st.columns([1,1])

    with t1_col1:
        default_location = None
        df = pd.DataFrame({'lat': [-37.91667], 'lon': [145.11667]})
        text_search = st.text_input("Search for a location", value="")
        st.map(df, zoom = 11)

    with t1_col2:
        st.subheader("Clothing Recommender") 
        st.selectbox("Activity Type",
        ("Swimming/Water Activity", "High Intensity Sports", "Low Intensity Sports"),
        index=None, placeholder="Select Activity Type")

with tab2:
    t2_col1, t2_col2 = st.columns(2)


css = '''
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
'''

st.markdown(css, unsafe_allow_html=True)
