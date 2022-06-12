import streamlit as st
from inspect import *
import os


# Use local CSS
def local_css(file_name):
	file_path = os.path.join(os.path.dirname(getfile(app)), file_name)
	with open(file_path) as f:
		st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def app():
	local_css("style/style.css")
	
	# ---- basic introduction ----
	with st.container():
		st.subheader("Hi, I am Euraxluo :wave:")
		st.title("An algorithm engineer")
		st.write("""
		I'm apply algorithms to the logistics industry
		
		My research interests are mainly in distributed systems
		"""
		         )
		st.write("[My Homepage >](https://github.com/Euraxluo)")
	
	# ---- My recent job ----
	with st.container():
		st.write("---")
		
		st.header("Recent Job")
		st.write("##")
		st.write(
			"""
			On my Github, as you can see, I've been doing this mostly lately:
			- study Dragonfly, the new Redis replacement
			- study Storage engine Bitcask, LSM
			- Develop distributed applications with Golang
			"""
		)
		st.write("[BreezeTeam wheel factory for learning purposes >](https://github.com/BreezeTeam)")
	
	# ---- Projects ----
	with st.container():
		st.write("---")
		
		st.header("Projects")
		st.write("##")
		# ------ Sub Projects ------
		
		# 分布式任务调度组件
		st.subheader("distributed task scheduler")
		st.write(
			"""
			distributed task scheduling Writing in go
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/BreezeTeam/scheduler)")
		
		# 分布式缓存
		st.subheader("distributed KV cache")
		st.write(
			"""
			Learn the distributed KV cache implemented by GroupCache
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/BreezeTeam/cache)")
		
		# bitcask 存储存储模型
		st.subheader("Bitcask")
		st.write(
			"""
			a log-structured hash table for fast key/value data with golang
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/BreezeTeam/bitcask)")
		
		# monkey scripting language
		st.subheader("A scripting language")
		st.write(
			"""
			A language implemented using GO and Rust
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/BreezeTeam/lang)")
		
		# monkey scripting language
		st.subheader("Simple RPC framework")
		st.write(
			"""
			Simple RPC framework Writing in Go
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/BreezeTeam/rpc)")
		
		# python 虚拟机
		st.subheader("Simple Python VM")
		st.write(
			"""
			Simple Python virtual machine Writing in C++
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/Euraxluo/simple_pyvm)")
		
		# TEXT-AM-GCN
		st.subheader("TEXT AM-GCN")
		st.write(
			"""
			A Text cluster base on AM-GCN
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/Euraxluo/TEXT-AM-GCN)")
		
		# 任务调度组件
		st.subheader("Job scheduling with fastapi")
		st.write(
			"""
			Provides scheduling apis and scheduling and task-related services Writing in Python
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/Euraxluo/fast_job)")
		
		# 简单的梯度下降和反向求导模块
		st.subheader("Gradient descent and reverse derivation libraries")
		st.write(
			"""
			Learning neural networks, writing gradient descent and reverse derivation libraries Writing in Numpy
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/Euraxluo/simplegrad)")
		
		# typing_environs
		st.subheader("Typing environs config sup module")
		st.write(
			"""
			typing_environs add type hints support for environs
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/Euraxluo/typing_environs)")
		
		# typing_environs
		st.subheader("Verb")
		st.write(
			"""
			A simple PHP web framework
			"""
		)
		st.markdown("[Goto Source Code...](https://github.com/Euraxluo/verb)")
	
	# ---- Contact Me ----
	with st.container():
		st.write("---")
		
		st.header("Contact Me!")
		st.write("##")
		contact_form = """
        <form action="https://formsubmit.co/euraxluo@outlook.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
		left_column, right_column = st.columns(2)
		with left_column:
			st.markdown(contact_form, unsafe_allow_html=True)
		with right_column:
			st.empty()
