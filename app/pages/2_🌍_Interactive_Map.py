import streamlit as st

# 导入多app 框架
from utils.multi_app import *

# 导入app列表
from apps.map import (
	basemaps,
	census,
	cesium,
	deck,
	device_loc,
	gee,
	gee_datasets,
	heatmap,
	home,
	# housing,
	# hurricane,
	plotly_maps,
	# raster,
	# timelapse,
	# vector,
	wms,
	xy,
)

st.set_page_config(layout="wide")
application = multi_app()

# add applications
application.add_app("Home", home.app)
# application.add_app("Create Timelapse", timelapse.app)
# application.add_app("Hurricane Mapping", hurricane.app)
# application.add_app("U.S. Real Estate Data", housing.app)
application.add_app("U.S. Census Data", census.app)
# application.add_app("Visualize Raster Data", raster.app)
# application.add_app("Visualize Vector Data", vector.app)
application.add_app("Search Basemaps", basemaps.app)
application.add_app("Pydeck Gallery", deck.app)
application.add_app("Heatmaps", heatmap.app)
application.add_app("Add Points from XY", xy.app)
application.add_app("Add Web Map Service (WMS)", wms.app)
application.add_app("Google Earth Engine (GEE)", gee.app)
application.add_app("Awesome GEE Community Datasets", gee_datasets.app)
application.add_app("Geolocation", device_loc.app)
application.add_app("Cesium 3D Map", cesium.app)
application.add_app("Plotly", plotly_maps.app)
# run applications
application.run()
