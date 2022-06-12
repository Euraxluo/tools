import streamlit as st


def app():
	# Customize the sidebar
	st.sidebar.title("About")
	about = """
	Web App URL: <https://share.streamlit.io/euraxluo/tools>
	GitHub Repository: <https://github.com/Euraxluo/tools>
	"""
	st.sidebar.info(about)
	my_logo = "https://avatars.githubusercontent.com/u/34028978?v=4/"
	st.sidebar.image(my_logo)
	
	# Customize page title
	
	st.title("Home")
	st.markdown(
		"""

		This app is my tool list

		The project itself is a multi-page, multi-app application
		"""
	)
	
	# Instructions
	st.header("Instructions")
	instructions = """
	1. Web App URL: <https://share.streamlit.io/euraxluo/tools>
	2. GitHub Repository: <https://github.com/Euraxluo/tools>
	3. Add a new pages to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.
	"""
	st.markdown(instructions)
	
	# Github
	st.header("My Github")
	github = """
	My github Home page: <https://github.com/Euraxluo>
	"""
	st.markdown(github)
