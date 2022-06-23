import time

import streamlit as st
from utils import rdict

db = rdict.db

st.set_page_config(layout="wide")

markdown = """
Web App URL: <https://template.streamlitapp.com>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Split-panel Map")

with st.expander("See source code"):
	with st.echo():
		st.info("test")

data = st.text_area("data")
save = st.button("存入")
if save:
	db["data"] = {"data": data, "time": time.time()}
st.write(db["data"])
with st.echo():
	st.write(exec(data))


def xx(x):
	x * 2
	return x


st.write(xx("data"))
