import os
from inspect import getfile

import leafmap
import streamlit as st


def app():
    st.title("Cesium 3D Map")
    html = "data/html/sfo_buildings.html"
    html = os.path.join(os.path.dirname(getfile(app)), html)
    leafmap.cesium_to_streamlit(html, height=800)
