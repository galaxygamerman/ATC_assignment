import tkinter as tk
from tkinter import messagebox
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.conversions import nfa_to_dfa
import pygraphviz as pgv
from PIL import Image, ImageTk
import os

def convert_and_draw():
	regex = entry.get()
	if not regex:
		messagebox.showerror("Error", "Please enter a regular expression.")
		return
	
	try:
		# Convert regex to NFA
		nfa = NFA.from_regex(regex)
		# Convert NFA to DFA
		dfa = nfa_to_dfa(nfa)
		
		# Visualize DFA using Graphviz
		dfa_graph = dfa.to_graphviz()
		dfa_graph.render("dfa", format="png", cleanup=True)
		
		# Display DFA
		img = Image.open("dfa.png")
		img = img.resize((400, 400), Image.ANTIALIAS)
		img_tk = ImageTk.PhotoImage(img)
		canvas.create_image(200, 200, image=img_tk)
		canvas.image = img_tk
		
	except Exception as e:
		messagebox.showerror("Error", f"Invalid regex or conversion failed: {e}")

# Create GUI
root = tk.Tk()
root.title("Regex to DFA Converter")

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Enter Regular Expression:")
label.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(frame, width=30)
entry.pack(side=tk.LEFT, padx=5)

button = tk.Button(frame, text="Convert", command=convert_and_draw)
button.pack(side=tk.LEFT, padx=5)

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(pady=10)

root.mainloop()
