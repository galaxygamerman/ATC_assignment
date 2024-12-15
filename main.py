import tkinter as tk
from tkinter import messagebox
from graphviz import Digraph
from PIL import Image, ImageTk

class FiniteStateMachineApp:
	#The Window
	root: tk

	# Frames
	num_states_frame: tk.Frame
	state_names_frame: tk.Frame
	transitions_frame: tk.Frame

	#Entries
	num_states_entry: tk.Entry
	state_names_entries: list[tk.Entry]
	transitions_entries: dict[str,tk.Entry]

	#Saved Values
	num_states: int
	state_names: list[str]
	transitions: dict[str,list[set[str]]]

	def __init__(self, root):
		self.root = root
		self.root.title("Finite State Machine App")
		self.state_names_entries = []
		self.transitions_entries = {}

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
			self.state_names_entries.append(entry)

		# Create button to submit state names
		tk.Button(self.state_names_frame, text="Submit", command=self.get_state_names).pack(side=tk.LEFT)

	def get_state_names(self):
		self.state_names = [state.get() for state in self.state_names_entries]
		if len(set(self.state_names)) != len(self.state_names):
			messagebox.showerror("Error", "State names must be unique.")
			return

		# Create input fields for transitions
		self.transitions_frame.pack_forget()
		self.transitions_frame = tk.Frame(self.root)
		self.transitions_frame.pack()
		for state in self.state_names:
			tk.Label(self.transitions_frame, text=f"Transitions for {state}:").pack(side=tk.LEFT)
			entry = tk.Entry(self.transitions_frame)
			entry.pack(side=tk.LEFT)
			self.transitions_entries[state] = entry

		# Create button to submit transitions
		tk.Button(self.transitions_frame, text="Submit", command=self.get_transitions).pack(side=tk.LEFT)

	def get_transitions(self):
		self.transitions = {}
		for current_state, entry in self.transitions_entries.items():
			transitions_for_current_state = entry.get().split(",")
			self.transitions[current_state] = []
			for t in transitions_for_current_state:
				# Split each transition string into state and input symbol
				input_symbol, next_state = t.split("->")
				self.transitions[current_state].append((input_symbol.strip(), next_state.strip()))

		# Print the finite state machine
		print("Finite State Machine:")
		print("States:", list(self.transitions_entries.keys()))
		print("Transitions:", self.transitions)

		# Create DFA graph using graphviz
		dot = Digraph(comment='Finite State Machine')
		for current_state, transitions_for_current_list in self.transitions.items():
			dot.node(current_state)  # Add state node
			for input_symbol, next_state in transitions_for_current_list:
				dot.edge(current_state, next_state, label=input_symbol)  # Add transition edge

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