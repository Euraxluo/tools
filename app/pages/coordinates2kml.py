import geojson
import pandas as pd
import shapely
import streamlit as st
from io import StringIO
from shapely import wkt
from shapely.geometry import shape, Point, Polygon, MultiPolygon, LineString, MultiLineString, MultiPoint


def get_data(way, isheader=True, sep=','):
	"""
	读取数据
	:param way:
	:param isheader:
	:param sep:
	:return:
	"""
	dataframe = None
	sep = sep if sep else ','
	st.write(f"读取数据如下. sep:`{sep}` isheader:`{isheader}`, way:`{way}`")
	match way:
		case "直接粘贴":
			uploaded_file = st.text_area('请输入多行经纬度列表')
			if uploaded_file:
				dataframe = pd.read_csv(StringIO(uploaded_file), header="infer" if isheader else None, sep=sep)

		case "文件上传":
			uploaded_file = st.file_uploader("选择文件并上传")
			if uploaded_file:
				dataframe = pd.read_csv(uploaded_file, header="infer" if isheader else None, sep=sep)

	with st.expander("上传结果如下."):
		st.write(dataframe)

	return dataframe


def choose_columns(dataframe):
	"""
	选择列
	:param dataframe:
	:return:
	"""
	if dataframe is not None:
		way = st.sidebar.multiselect(
			'选择列',
			dataframe.columns.tolist()
		)
		st.write(f"选的的列: {way}")
		return way
	return []


def get_columns(dataframe, columns):
	"""
	聚合列数据
	:param dataframe:
	:param columns:
	:return:
	"""
	result = {}
	if dataframe is not None and columns:
		for _, row in dataframe.iterrows():
			for c in columns:
				if c not in result:
					result[c] = []
				result[c].append(row[c])
	with st.expander("解析结果如下."):
		st.write(result)

	return result


@st.cache(suppress_st_warning=True)
def transform(datas, data_type, wkt_type):
	"""
	数据转换
	:param datas:
	:param data_type:
	:param wkt_type:
	:return:
	"""
	if not datas:
		return None

	geometry = None
	# 1. 先分割解析各种数据
	match data_type:
		case "Point":
			points = []
			# 如果有n列，判断每一列是不是 list，如果是，那么每一列都转换为 点
			# 如果有两列，判断每一列 都不是list ，那么两列加起来是点
			if len(datas.keys()) == 2 and not isinstance(list(datas.values())[0][0], list):
				for i in zip(*(datas.values())):
					points.append(Point(*i))
			elif isinstance(list(datas.values())[0][0], list):
				for i in datas.values():
					points.append(Point(*i))
			geometry = MultiPoint(points)

		case "LineString":
			# 每一列都是list，转换为 线
			...
		case "Polygon":
			# 每一列都是 list ，转换为面
			...
		case "MultiPoint":
			# 每一列都是 转换为一个  MultiPoint
			...
		case "MultiLineString":
			# 每一列都是 list 转换为一个  MultiLineString
			...
		case "MultiPolygon":
			# 每一列都是 list 转换为一个  MultiPolygon
			...
	if not geometry:
		return geometry

	result = None
	filename = 'data'
	match wkt_type:
		case "KML":
			result = geometry.wkt
			filename += '.kml'
		case "WKT":
			result = geometry.wkt
			filename += '.wkt'
		case "GEOJSON":
			result = geojson.dumps(shapely.geometry.mapping(geometry))
			filename += '.json'
		case _:
			filename += '.text'
	st.code(result)
	return result, filename


def app():
	st.write("""## 经纬度列表转KML""")
	way = st.sidebar.selectbox(
		'经纬度数据上传途径',
		("文件上传", "直接粘贴")
	)
	isheader = st.sidebar.radio(
		'是否忽略header解析',
		(False, True)
	)

	sep = st.sidebar.text_input('输入你的分隔符')

	# 读取并显示数据
	dataframe = get_data(way, isheader, sep)
	# 根据数据的列，来选择哪一列是我们需要的数据
	columns = choose_columns(dataframe)

	# 获取并显示这些数据
	datas = get_columns(dataframe, columns)

	# 选择将这些列构建为什么数据
	data_type = st.sidebar.selectbox(
		'请选择转换数据类型',
		("Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"),
	)
	wkt_type = st.sidebar.selectbox(
		'请选择转换格式',
		("KML", "WKT", "GEOJSON")
	)
	# 将上面解析的到的数据，每一种数据都
	clicked = st.sidebar.button(f"点击转换生成{wkt_type}")
	if clicked:
		data, file_name = transform(datas, data_type, wkt_type)
		if data is not None:
			st.download_button(
				label="下载数据",
				data=data,
				file_name=file_name,
				mime='text/plain',
			)
