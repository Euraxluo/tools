from io import StringIO

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


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
		uploaded_file = st.text_area('请输入多行经纬度列表')
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


def gridoptions_builder_from_dataframe(gb: GridOptionsBuilder, dataframe, **default_column_parameters):
	type_mapper = {
		"b": ["textColumn"],
		"i": ["numericColumn", "numberColumnFilter"],
		"u": ["numericColumn", "numberColumnFilter"],
		"f": ["numericColumn", "numberColumnFilter"],
		"c": [],
		"m": ['timedeltaFormat'],
		"M": ["dateColumnFilter", "shortDateTimeFormat"],
		"O": [],
		"S": [],
		"U": [],
		"V": [],
	}
	if gb is None:
		gb = GridOptionsBuilder()
	
	if any((isinstance(col, list) or isinstance(col, str)) and ('.' in col) for col in dataframe.columns):
		gb.configure_grid_options(suppressFieldDotNotation=True)
	
	for col_name, col_type in zip(dataframe.columns, dataframe.dtypes):
		gb.configure_column(field=col_name,header_name=col_name, type=type_mapper.get(col_type.kind, []))
	
	return gb


def app():
	st.title("CSV Wrangler")
	way = st.sidebar.selectbox(
		'经纬度数据上传途径',
		("文件上传", "直接粘贴")
	)
	isheader = st.sidebar.radio(
		'是否忽略header解析',
		(False, True)
	)
	
	sep = st.sidebar.text_input('输入你的分隔符')
	
	dataframes = get_data(way, isheader, sep)
	if dataframes is not None:
		file_container = st.expander("Check your uploaded .csv")
		file_container.write(dataframes)
	else:
		st.info(
			f"""
                👆 Upload a .csv file first. Sample to try: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
                """
		)
		
		st.stop()
	gb = GridOptionsBuilder()
	gridoptions_builder_from_dataframe(gb, dataframes)
	gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
	# gb.configure_selection(selection_mode="multiple", use_checkbox=True)
	gb.configure_side_bar()
	
	st.success(
		f"""
	        💡 Tip! Hold the shift key when selecting rows to select multiple rows at once!
	        """
	)
	
	response = AgGrid(
		dataframes,
		gridOptions=gb.build(),
		enable_enterprise_modules=True,
		update_mode=GridUpdateMode.MODEL_CHANGED,
		data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
		fit_columns_on_grid_load=False,
	)
	df = pd.DataFrame(response["selected_rows"])
	
	st.subheader("Filtered data will appear below 👇 ")
	st.table(df)
