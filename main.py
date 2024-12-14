import tkinter as tk
from tkinter import messagebox
from graphviz import Digraph
from PIL import Image, ImageTk

class FiniteStateMachineApp:
	root : tk
	states : list
	transitions : dict
	num_states_frame : tk.Frame
	num_states_entry : tk.Entry
	num_states : int
	state_names_frame : tk.Frame
	transitions_frame : tk.Frame

	def __init__(self, root):
		self.root = root
		self.root.title("Finite State Machine App")
		self.states = []
		self.transitions = {}

		# Create input frame for number of states
		self.num_states_frame = tk.Frame(self.root)
		self.num_states_frame.pack()
		tk.Label(self.num_states_frame, text="Enter number of states (dead states can be excluded from this number):").pack(side=tk.LEFT)
		self.num_states_entry = tk.Entry(self.num_states_frame)
		self.num_states_entry.pack(side=tk.LEFT)
		tk.Button(self.num_states_frame, text="Submit", command=self.get_num_states).pack(side=tk.LEFT)

		# Create input frame for state names
		self.state_names_frame = tk.Frame(self.root)
		self.state_names_frame.pack()

		# Create input frame for transitions
		self.transitions_frame = tk.Frame(self.root)
		self.transitions_frame.pack()

	def get_num_states(self):
		try:
			self.num_states = int(self.num_states_entry.get())
			if self.num_states <= 0:
				raise ValueError
		except ValueError:
			messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")
			return

		# Create input fields for state names
		self.state_names_frame.pack_forget()
		self.state_names_frame = tk.Frame(self.root)
		self.state_names_frame.pack()
		for i in range(self.num_states):
			tk.Label(self.state_names_frame, text=f"State {i + 1} name:").pack(side=tk.LEFT)
			entry = tk.Entry(self.state_names_frame)
			entry.pack(side=tk.LEFT)
			self.states.append(entry)

		# Create button to submit state names
		tk.Button(self.state_names_frame, text="Submit", command=self.get_state_names).pack(side=tk.LEFT)

	def get_state_names(self):
		state_names = [state.get() for state in self.states]
		if len(set(state_names)) != len(state_names):
			messagebox.showerror("Error", "State names must be unique.")
			return

		# Create input fields for transitions
		self.transitions_frame.pack_forget()
		self.transitions_frame = tk.Frame(self.root)
		self.transitions_frame.pack()
		for i, state in enumerate(state_names):
			tk.Label(self.transitions_frame, text=f"Transitions for {state}:").pack(side=tk.LEFT)
			entry = tk.Entry(self.transitions_frame)
			entry.pack(side=tk.LEFT)
			self.transitions[state] = entry

		# Create button to submit transitions
		tk.Button(self.transitions_frame, text="Submit", command=self.get_transitions).pack(side=tk.LEFT)

	def get_transitions(self):
		transitions = {}
		for state, entry in self.transitions.items():
			transition_list = entry.get().split(",")
			transitions[state] = []
			for t in transition_list:
				# Split each transition string into state and input symbol
				input_symbol, next_state = t.split("->")
				transitions[state].append((next_state.strip(), input_symbol.strip()))

		# Print the finite state machine
		print("Finite State Machine:")
		print("States:", list(self.transitions.keys()))
		print("Transitions:")
		for state, transition in transitions.items():
			for next_state, input_symbol in transition:
				print(f"{state} on {input_symbol} -> {next_state}")

		# Create DFA graph using graphviz
		dot = Digraph(comment='Finite State Machine')
		for state, transition in transitions.items():
			dot.node(state)  # Add state node
			for next_state, input_symbol in transition:
				dot.edge(state, next_state, label=input_symbol)  # Add transition edge

		# Render the graph to a file
		dot.render('fsm','generatedImages', format='png', cleanup=True)  # Save as PNG and cleanup

		# Load the image using PIL and display in the window
		self.display_image('generatedImages/fsm.png')

	def display_image(self, image_path):
		# Create a new top-level window to display the image
		image_window = tk.Toplevel(self.root)
		image_window.title("Generated Diagram")

		# Load the image using PIL
		img = Image.open(image_path)
		img = img.resize((img.width*2, img.height*2), Image.LANCZOS)  # Resize image if necessary
		photo = ImageTk.PhotoImage(img)

		# Create a label to display the image
		label = tk.Label(image_window, image=photo)
		label.image = photo  # Keep a reference to avoid garbage collection
		label.pack()

		# Add a button to close the image window
		tk.Button(image_window, text="Close", command=image_window.destroy).pack()

if __name__ == "__main__":
	root = tk.Tk()
	app = FiniteStateMachineApp(root)
	root.mainloop()