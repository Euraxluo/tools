import streamlit as st
from multipage import MultiPage
from pages import home, machine_learning, coordinates2kml

st.set_page_config(page_title="tool", page_icon="random", layout="wide")

app = MultiPage()

# add applications
# app.add_page('主页', home.app)
app.add_page('机器学习', machine_learning.app)
app.add_page('coordinates2kml', coordinates2kml.app)

# Run application
if __name__ == '__main__':
	app.run()
