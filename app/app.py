import streamlit as st
from utils.app_group import page_group
# 导入app列表
from apps import home


# def main():
# 	page = page_group("p")
#
# 	with st.sidebar:
# 		st.title("🎈 Okld's Gallery")
#
# 		with st.expander("✨ APPS", True):
# 			page.item("Streamlit gallery", home.app, default=True)
#
# 		with st.expander("🧩 COMPONENTS", True):
# 			page.item("Ace editor", home.app)
#
# 	page.show()
#
#
# if __name__ == "__main__":
# 	st.set_page_config(page_title="Streamlit Gallery by Okld", page_icon="🎈", layout="wide")
# 	main()
