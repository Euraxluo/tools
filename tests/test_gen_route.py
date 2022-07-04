import geojson
import pandas as pd
import shapely
import streamlit as st
from shapely.geometry import shape
from utils.coordinates import transform_to_shapely
from utils.geo_to_kml import to_kml


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
	return result


def transform(datas, properties, data_type, wkt_type):
	"""
	数据转换
	:param datas:
	:param data_type:
	:param wkt_type:
	:return:
	"""
	if not datas:
		return None
	geometrys = []
	for v in zip(*datas.values()):
		geometry = transform_to_shapely(dict(zip(datas.keys(), [v])), data_type)
		geometrys.append(geometry)
	features = []
	for idx, ps in enumerate(zip(*properties.values())):
		feature = geojson.Feature(geometry=geometrys[idx], properties=dict(zip(properties.keys(), ps)))
		features.append(feature)
	
	return features


if __name__ == '__main__':
	total_features = []
	with open("./log.txt") as f:
		for idx, line in enumerate(f.readlines()):
			if idx % 2 == 0:
				continue
			data = pd.read_json(line)
			features = transform(get_columns(data, ["route"]), get_columns(data, ["taskCode"]), "LineString", "GEOJSON")
			total_features.extend(features)
	
	geometry = geojson.FeatureCollection(features=total_features, **{"name": "fence", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}})
	result = geojson.dumps(shapely.geometry.mapping(geometry))
	print(result)
