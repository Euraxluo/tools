import json
import streamlit as st
from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from .dashboard import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player


def app():
	if "w" not in state:
		board = Dashboard()
		w = SimpleNamespace(
			dashboard=board,
			editor=Editor(board, 0, 0, 6, 11, minW=3, minH=3),
			player=Player(board, 0, 12, 6, 10, minH=5),
			pie=Pie(board, 6, 0, 6, 7, minW=3, minH=4),
			radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
			card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
			data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
		)
		state.w = w
		
		w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
		w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
		w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
		w.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")
	else:
		w = state.w
	
	with elements("demo"):
		event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
		
		with w.dashboard(rowHeight=57):
			w.editor()
			w.player()
			w.pie(w.editor.get_content("Pie chart"))
			w.radar(w.editor.get_content("Radar chart"))
			w.card(w.editor.get_content("Card content"))
			w.data_grid(w.editor.get_content("Data grid"))
