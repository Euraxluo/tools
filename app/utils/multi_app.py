import streamlit as st


class MultiApp:
	"""Framework for combining multiple streamlit applications
	"""
	
	def __init__(self) -> None:
		self.apps = []
	
	def add_app(self, title, func):
		self.apps.append(
			{
				'title': title,
				'function': func
			}
		)
	
	def run(self):
		if len(self.apps) > 1:
			app = st.sidebar.selectbox(
				'Tool Select',
				self.apps,
				format_func=lambda app: app['title']  # Function to modify the display of the labels.
			
			)
			app['function']()
		elif len(self.apps) == 1:
			self.apps[0]['function']()
