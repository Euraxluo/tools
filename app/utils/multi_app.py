import traceback
from inspect import getmodule

import streamlit as st
import os

__all__ = ["multi_app"]


def multi_app() -> "MultiApp":
	key = traceback.extract_stack()[-2].filename
	
	if key not in st.session_state:
		st.session_state[key] = MultiApp(key)
	
	return st.session_state[key]


class MultiApp:
	"""Framework for combining multiple streamlit applications
	"""
	
	def __init__(self, applications_key) -> None:
		self.apps = []
		self.applications_key = applications_key
		
		self._param: str = applications_key
		self._default: str = None
		self._selected: str = None
	
	def add_app(self, title, func):
		app_key = f"{self.applications_key}::{title}_{getmodule(func).__name__}.{func.__name__}"
		app_item = {'title': title, 'function': func, 'applications_key': self.applications_key, 'app_key': app_key}
		if app_key not in st.session_state:
			st.session_state[app_key] = app_item
			self.apps.append(app_item)
	
	# st.checkbox(label, key=key, disabled=selected, on_change=self._on_change, args=(page,))
	
	def run(self):
		if self.selected is not None:
			self.selected()
		elif len(self.apps) > 1:
			app = st.sidebar.selectbox(
				'Tool Select',
				self.apps,
				format_func=lambda app: app['title'],  # Function to modify the display of the labels.
			)
			self._on_change(app)
			app['function']()
		elif len(self.apps) == 1:
			self.apps[0]['function']()
	
	@property
	def selected(self):
		params = st.experimental_get_query_params()
		st.write("selected")
		st.write(params)
		if self.applications_key in params:
			app_key = params[self.applications_key][0]
			for a in self.apps:
				if a['app_key'] == app_key:
					return a['function']
		else:
			return None
	
	def _on_change(self, app: dict) -> None:
		params = st.experimental_get_query_params()
		params[app['applications_key']] = [app['app_key']]
		st.write("_on_change")
		st.write(params)
		st.experimental_set_query_params(**params)
