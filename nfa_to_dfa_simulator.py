import tkinter as tk
from tkinter import messagebox
from graphviz import Digraph
import os

def generate_fsm_diagram(states, transitions, start_state, accept_states, filename):
    try:
        dot = Digraph()

        # Add nodes for all states
        for state in states:
            if state in accept_states:
                dot.node(state, shape='doublecircle')  # Accept states have double circles
            else:
                dot.node(state)

        # Add an invisible start node pointing to the start state
        dot.node('start', shape='none')
        dot.edge('start', start_state)

        # Add edges for transitions
        for transition in transitions:
            src, sym, dest = transition.split(',')
            dot.edge(src, dest, label=sym)

        # Render the diagram
        dot.render(filename, format='png', cleanup=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate FSM diagram: {e}")

def simulate_nfa_to_dfa():
    try:
        # Parse input
        nfa_states = state_entry.get().split(',')
        alphabet = alphabet_entry.get().split(',')
        start_state = start_state_entry.get()
        accept_states = accept_state_entry.get().split(',')
        nfa_transitions = transition_entry.get().split(';')
        input_string = input_string_entry.get()

        # Parse NFA transitions
        nfa_transition_dict = {}
        for trans in nfa_transitions:
            src, sym, dest = trans.split(',')
            if (src, sym) not in nfa_transition_dict:
                nfa_transition_dict[(src, sym)] = set()
            nfa_transition_dict[(src, sym)].add(dest)

        # Subset construction for NFA to DFA conversion
        dfa_states = []
        dfa_transitions = []
        dfa_accept_states = []
        state_map = {}

        queue = [frozenset([start_state])]
        state_map[frozenset([start_state])] = '{' + ','.join(sorted([start_state])) + '}'
        dfa_states.append(state_map[frozenset([start_state])])

        while queue:
            current_set = queue.pop(0)
            current_name = state_map[current_set]

            for sym in alphabet:
                next_set = set()
                for state in current_set:
                    if (state, sym) in nfa_transition_dict:
                        next_set.update(nfa_transition_dict[(state, sym)])

                if next_set:
                    next_set_frozen = frozenset(next_set)
                    if next_set_frozen not in state_map:
                        state_map[next_set_frozen] = '{' + ','.join(sorted(next_set)) + '}'
                        dfa_states.append(state_map[next_set_frozen])
                        queue.append(next_set_frozen)

                    dfa_transitions.append(f'{current_name},{sym},{state_map[next_set_frozen]}')

                    # Check if the new DFA state is an accept state
                    if any(state in accept_states for state in next_set):
                        dfa_accept_states.append(state_map[next_set_frozen])

        # Generate DFA diagram
        generate_fsm_diagram(dfa_states, dfa_transitions, '{' + start_state + '}', dfa_accept_states, 'dfa_diagram')

        # Display DFA diagram in the GUI
        if os.path.exists('dfa_diagram.png'):
            img = tk.PhotoImage(file='dfa_diagram.png')
            fsm_diagram_label.config(image=img)
            fsm_diagram_label.image = img

        result_label.config(text="NFA successfully converted to DFA", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"NFA to DFA conversion failed: {e}")

# GUI Setup
root = tk.Tk()
root.title("NFA to DFA Conversion and Simulation")
root.geometry("1200x600")

# Frames for Input and Output
input_frame = tk.Frame(root, padx=10, pady=10, bg="lightblue", relief="groove", bd=2)
input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

output_frame = tk.Frame(root, padx=10, pady=10, bg="lightgrey", relief="groove", bd=2)
output_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Input Fields
input_title = tk.Label(input_frame, text="Input Section", font=("Arial", 14, "bold"), bg="lightblue")
input_title.grid(row=0, column=0, columnspan=2, pady=10)

state_label = tk.Label(input_frame, text="Enter States (comma-separated):", bg="lightblue")
state_label.grid(row=1, column=0, sticky="w", pady=5)
state_entry = tk.Entry(input_frame, width=30)
state_entry.grid(row=1, column=1, pady=5)

alphabet_label = tk.Label(input_frame, text="Enter Alphabet (comma-separated):", bg="lightblue")
alphabet_label.grid(row=2, column=0, sticky="w", pady=5)
alphabet_entry = tk.Entry(input_frame, width=30)
alphabet_entry.grid(row=2, column=1, pady=5)

start_state_label = tk.Label(input_frame, text="Enter Start State:", bg="lightblue")
start_state_label.grid(row=3, column=0, sticky="w", pady=5)
start_state_entry = tk.Entry(input_frame, width=30)
start_state_entry.grid(row=3, column=1, pady=5)

accept_state_label = tk.Label(input_frame, text="Enter Accepting States (comma-separated):", bg="lightblue")
accept_state_label.grid(row=4, column=0, sticky="w", pady=5)
accept_state_entry = tk.Entry(input_frame, width=30)
accept_state_entry.grid(row=4, column=1, pady=5)

transition_label = tk.Label(input_frame, text="Enter Transitions (state,symbol,next_state;...):", bg="lightblue")
transition_label.grid(row=5, column=0, sticky="w", pady=5)
transition_entry = tk.Entry(input_frame, width=30)
transition_entry.grid(row=5, column=1, pady=5)

input_string_label = tk.Label(input_frame, text="Enter String to Verify:", bg="lightblue")
input_string_label.grid(row=6, column=0, sticky="w", pady=5)
input_string_entry = tk.Entry(input_frame, width=30)
input_string_entry.grid(row=6, column=1, pady=5)

simulate_button = tk.Button(input_frame, text="Convert NFA to DFA", command=simulate_nfa_to_dfa, bg="white", fg="black")
simulate_button.grid(row=7, column=0, columnspan=2, pady=10)

# Output Section
output_title = tk.Label(output_frame, text="Output Section", font=("Arial", 14, "bold"), bg="lightgrey")
output_title.grid(row=0, column=0, pady=10)

fsm_diagram_label = tk.Label(output_frame, bg="lightgrey")
fsm_diagram_label.grid(row=1, column=0, pady=10)

result_label = tk.Label(output_frame, text="Result:", font=("Arial", 12), bg="lightgrey")
result_label.grid(row=2, column=0, pady=10)

root.mainloop()