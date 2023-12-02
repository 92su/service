import streamlit as st
from multiapp import MultiApp
from apps import first,second

st.set_page_config(layout='wide',initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

app = MultiApp()

st.markdown("""
# IT Service Center """)

# Add all your application here
app.add_app("End User Support Team Page",first.app)
app.add_app("Network Team Page",second.app)

app.run()
