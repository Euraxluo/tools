import json

import geojson
import pandas as pd
import shapely
import streamlit as st
from io import StringIO
from shapely.geometry import shape
from streamlit_ace import st_ace
from utils.coordinates import transform_to_shapely
from utils.geo_to_kml import to_kml


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
	if way == "直接粘贴":
		uploaded_file = st_ace('请输入多行日志列表', theme="github", language="python", height=100)
		if uploaded_file:
			dataframe = pd.read_csv(StringIO(uploaded_file), header="infer" if isheader else None, sep=sep)
		else:
			st.stop()
	
	elif way == "文件上传":
		uploaded_file = st.file_uploader("选择文件并上传")
		if uploaded_file:
			dataframe = pd.read_csv(uploaded_file, header="infer" if isheader else None, sep=sep)
		else:
			st.stop()
	
	with st.expander("上传结果如下."):
		st.write(dataframe)
	
	return dataframe


def choose_columns(dataframe, prompt="选择列"):
	"""
	选择列
	:param dataframe:
	:return:
	"""
	if dataframe is not None:
		way = st.sidebar.multiselect(
			prompt,
			dataframe.columns.tolist()
		)
		st.write(f"{prompt}结果: {way}")
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
def transform(datas, match, out_put):
	"""
	数据转换
	:param datas:
	:param match:
	:param out_put:
	:return:
	"""
	if not datas:
		return None
	result = {}
	filename = 'log.txt'
	for k, v in datas.items():
		result[k] = []
		for vd in v:
			if match in vd and out_put:
				result[k].append(vd)
			elif not out_put:
				result[k].append(vd)
	result = pd.read_json(json.dumps(result))
	with st.expander("转换结果如下."):
		st.table(result)
	return result, filename


def app():
	st.write("""## 日志数据处理""")
	way = st.sidebar.selectbox(
		'日志数据上传途径',
		("文件上传", "直接粘贴")
	)
	isheader = st.sidebar.radio(
		'是否忽略header解析',
		(False, True)
	)
	
	sep = st.sidebar.text_input('输入你的分隔符')
	match = st.sidebar.text_input('输入匹配数据')
	
	out_put = st.sidebar.radio(
		'是否保留匹配的行',
		(False, True)
	)
	
	# 读取并显示数据
	dataframe = get_data(way, isheader, sep)
	# 根据数据的列，来选择哪一列是我们需要的数据
	columns = choose_columns(dataframe)
	
	# 获取并显示这些数据
	datas = get_columns(dataframe, columns)
	# 输出以下数据
	# 将上面解析的到的数据，每一种数据都
	clicked = st.sidebar.button(f"点击转换生成")
	if clicked:
		data, file_name = transform(datas, match, out_put)
		if data is not None:
			st.download_button(
				label="下载日志数据",
				data=data.to_csv().encode('utf8'),
				file_name=file_name,
				mime='text/plain',
			)
