import streamlit as st

# 导入多app 框架
from utils.multi_app import MultiApp

# 导入app列表
from apps import about_me

st.set_page_config(layout="wide")
application = MultiApp()

# add applications
application.add_app('coordinates2kml', about_me.app)

application.run()
