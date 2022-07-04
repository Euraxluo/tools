import streamlit as st

# 导入多app 框架
from utils.multi_app import *

# 导入app列表
from apps import table2kml, csv, json2kml, json2geojson,log_treatment

st.set_page_config(layout="wide")
application = multi_app()

# add applications
application.add_app('coordinates2kml', table2kml.app)
application.add_app('json2kml', json2kml.app)
application.add_app('json2geojson', json2geojson.app)
application.add_app('csv', csv.app)
application.add_app('log_treatment', log_treatment.app)
# run applications
application.run()
