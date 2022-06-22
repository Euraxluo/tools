import streamlit as st

# 导入多app 框架
from utils.multi_app import *

# 导入app列表
from apps import home

st.set_page_config(page_title="tool", page_icon="🍀", layout="wide")
application = multi_app()

# add applications
application.add_app('home', home.app)
# run applications
application.run()
