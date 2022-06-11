import geojson
from shapely.geometry import shape, Point, Polygon, MultiPolygon, LineString, MultiLineString, MultiPoint


def parse_data_to_shapely(data, cls):
	if isinstance(data, tuple):
		data = list(data)

	# 如果是string，那么解析为对应的结构
	if isinstance(data, str):
		features = []
		# 直接geojson转换为对象
		data = geojson.loads(data)
		if isinstance(data, list):
			return parse_data_to_shapely(data, cls)
		features.append(geojson.Feature(geometry=data))
		return geojson.FeatureCollection(features=features)

	# 如果 data = [x,y] 是列表，且长度为2，且 元素不是list，那么可以认为这个是一个point
	if isinstance(data, list) and len(data) == 2 and not isinstance(data[0], list) and cls == Point:
		return Point(*data)

	# 如果数据是 [[x,y],...],并且 cls为 point，那么转换为多个point
	if isinstance(data, list) and isinstance(data[0], list) and cls == Point:
		res = []
		for d in data:
			parse_res = parse_data_to_shapely(d, cls)
			if isinstance(parse_res, list):
				res.extend(parse_res)
			else:
				res.append(parse_res)
		return res

	# 如果数据是 [[x,y],...],并且 cls为 point，那么转换为多个 MultiPoint
	if isinstance(data, list) and isinstance(data[0], list) and cls == MultiPoint:
		ps = parse_data_to_shapely(data, Point)
		return MultiPoint(*ps)
	# 如果数据是 [[x,y],...],并且 cls为 point，那么转换为多个 Polygon
	if isinstance(data, list) and isinstance(data[0], list) and cls == Polygon:
		return Polygon(data)
	# 如果数据是 [[x,y],...],并且 cls为 point，那么转换为多个 LineString
	if isinstance(data, list) and isinstance(data[0], list) and cls == LineString:
		return LineString(data)


def transform_to_shapely(datas, data_type):
	geometry = None

	# 1. 先分割解析各种数据
	if data_type == "Point":
		points = []
		# 如果有n列，判断每一列是不是 list，如果是，那么每一列都转换为 点
		# 如果有两列，判断每一列 都不是list ，那么两列加起来是点
		if len(datas.keys()) == 2 and not isinstance(list(datas.values())[0][0], list):
			for i in zip(*(datas.values())):
				points.append(parse_data_to_shapely(i, Point))
		elif isinstance(list(datas.values())[0][0], list):
			for i in datas.values():
				p = parse_data_to_shapely(i, Point)
				if isinstance(p, list):
					points.extend(p)
				else:
					points.append(p)
		elif isinstance(list(datas.values())[0][0], str):
			for i in datas.values():
				for j in i:
					points.append(parse_data_to_shapely(j, Point))
		if isinstance(points[0], Point):
			geometry = MultiPoint(points)
		elif isinstance(points[0], list):
			geometry = MultiPoint([j for i in points for j in i])

	elif data_type == "Polygon":
		polygons = []
		# 每一列都是 list ，转换为面
		if isinstance(list(datas.values())[0][0], list):
			for i in datas.values():
				for j in i:
					polygons.append(parse_data_to_shapely(j, Polygon))
		elif isinstance(list(datas.values())[0][0], str):
			for i in datas.values():
				for j in i:
					polygons.append(parse_data_to_shapely(j, Polygon))
		geometry = MultiPolygon(polygons)
	elif data_type == "LineString":
		# 每一列都是list，转换为 线
		linestring = []
		# 每一列都是 list ，转换为面
		if isinstance(list(datas.values())[0][0], list):
			for i in datas.values():
				for j in i:
					linestring.append(parse_data_to_shapely(j, LineString))
		elif isinstance(list(datas.values())[0][0], str):
			for i in datas.values():
				for j in i:
					linestring.append(parse_data_to_shapely(j, LineString))
		geometry = MultiLineString(linestring)

	elif data_type == "MultiPoint":
		# 每一列都是 转换为一个  MultiPoint
		geometry = transform_to_shapely(datas, "Point")
	elif data_type == "MultiLineString":
		# 每一列都是 list 转换为一个  MultiLineString
		geometry = transform_to_shapely(datas, "LineString")
	elif data_type == "MultiPolygon":
		# 每一列都是 list 转换为一个  MultiPolygon
		geometry = transform_to_shapely(datas, "Polygon")

	return geometry
