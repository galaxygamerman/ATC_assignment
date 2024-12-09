import tkinter as tk
from tkinter import messagebox
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
import networkx as nx
import matplotlib.pyplot as plt

def nfa_to_dfa(nfa):
	"""Convert NFA to DFA."""
	dfa_states = {}
	dfa_transitions = {}
	queue = []

	# Start with the epsilon closure of the NFA's initial state
	initial_state = frozenset({nfa.initial_state})
	queue.append(initial_state)
	dfa_states[initial_state] = True

	visited = set()

	while queue:
		current_set = queue.pop(0)
		current_name = "-".join(sorted(map(str, current_set)))

		if current_name not in dfa_transitions:
			dfa_transitions[current_name] = {}

		for symbol in nfa.input_symbols:
			# Compute the next state for this symbol
			next_set = set()
			for state in current_set:
				next_set.update(nfa.transitions.get(state, {}).get(symbol, set()))

			if next_set:
				next_name = "-".join(sorted(map(str, next_set)))
				dfa_transitions[current_name][symbol] = next_name

				if frozenset(next_set) not in visited:
					visited.add(frozenset(next_set))
					queue.append(frozenset(next_set))

		for symbol in nfa.input_symbols:
			if symbol not in dfa_transitions[current_name]:
				dfa_transitions[current_name][symbol] = "dead_state"

	dfa_final_states = {
		"-".join(sorted(map(str, state)))
		for state in dfa_states
		if any(nfa_final in state for nfa_final in nfa.final_states)
	}

	dfa_initial_state = "-".join(sorted(map(str, initial_state)))

	return DFA(
		states=set(dfa_transitions.keys()),
		input_symbols=nfa.input_symbols,
		transitions=normalize_transitions(dfa_transitions),
		initial_state=dfa_initial_state,
		final_states=dfa_final_states
	)

def normalize_transitions(transitions):
	"""Normalize DFA transitions to the format required by automata-lib."""
	normalized = {}
	for state, transitions_dict in transitions.items():
		for symbol, next_state in transitions_dict.items():
			normalized[(state, symbol)] = next_state
	return normalized

def draw_dfa(dfa):
	"""Draw the DFA using NetworkX and Matplotlib."""
	graph = nx.DiGraph()

	for state in dfa.states:
		graph.add_node(state, shape="doublecircle" if state in dfa.final_states else "circle")
	for (state, symbol), next_state in dfa.transitions.items():
		graph.add_edge(state, next_state, label=symbol)

	pos = nx.spring_layout(graph)
	nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10)
	edge_labels = nx.get_edge_attributes(graph, 'label')
	nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

	plt.title("DFA Diagram")
	plt.show()

def convert_and_draw():
	"""Convert regex to DFA and draw the diagram."""
	regex = entry.get()
	if not regex:
		messagebox.showerror("Error", "Please enter a regular expression.")
		return

	try:
		# Convert regex to NFA
		nfa = NFA.from_regex(regex)

		# Convert NFA to DFA
		dfa = nfa_to_dfa(nfa)

		# Draw DFA using NetworkX
		draw_dfa(dfa)

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

root.mainloop()
