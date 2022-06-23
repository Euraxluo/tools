from rocksdict import Rdict
import streamlit as st


def db_factory():
	db = Rdict("./dict")
	return db


db = db_factory()
