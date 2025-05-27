import tkinter as tk
import ast

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Structure Visual Tool")

        # Input Frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Value (Python syntax):").grid(row=0, column=0)
        self.value_entry = tk.Entry(self.input_frame, width=40)
        self.value_entry.grid(row=0, column=1)

        tk.Label(self.input_frame, text="Type (optional):").grid(row=1, column=0)
        self.type_entry = tk.Entry(self.input_frame, width=40)
        self.type_entry.grid(row=1, column=1)

        self.submit_btn = tk.Button(self.input_frame, text="Visualize", command=self.visualize)
        self.submit_btn.grid(row=2, columnspan=2, pady=5)

        # Canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

    def visualize(self):
        self.canvas.delete("all")

        value_text = self.value_entry.get()
        type_hint = self.type_entry.get().strip().lower()

        try:
            value = ast.literal_eval(value_text)
        except Exception as e:
            self.canvas.create_text(300, 200, text=f"Error parsing value: {e}", fill="red", font=("Arial", 14))
            return

        # Determine type if not explicitly given
        value_type = type_hint if type_hint else type(value).__name__

        # Dispatch drawing based on inferred type
        draw_fn = getattr(self, f"draw_{value_type}", self.draw_default)
        draw_fn(value, value_type)

    # Primitive and fallback drawer
    def draw_default(self, value, value_type):
        self.canvas.create_rectangle(150, 150, 450, 250, fill="lightgray", outline="black")
        self.canvas.create_text(300, 180, text=f"Type: {value_type}", font=("Arial", 14, "bold"))
        self.canvas.create_text(300, 220, text=f"Value: {str(value)}", font=("Arial", 12))

    # Specialized drawer for list
    def draw_list(self, value, value_type):
        self.canvas.create_text(300, 50, text=f"Type: {value_type}", font=("Arial", 14, "bold"))
        start_x = 50
        y = 150
        box_width = 60

        for i, item in enumerate(value):
            x0 = start_x + i * (box_width + 10)
            x1 = x0 + box_width
            self.canvas.create_rectangle(x0, y, x1, y + 60, fill="lightblue")
            self.canvas.create_text((x0 + x1)//2, y + 30, text=str(item), font=("Arial", 12))

    def draw_tuple(self, value, value_type):
        self.draw_list(value, "tuple")

    def draw_set(self, value, value_type):
        self.draw_list(list(value), "set")

    def draw_dict(self, value, value_type):
        self.canvas.create_text(300, 50, text="Type: dict", font=("Arial", 14, "bold"))
        y = 100
        for i, (k, v) in enumerate(value.items()):
            self.canvas.create_rectangle(100, y + i * 50, 500, y + 40 + i * 50, fill="lightyellow")
            self.canvas.create_text(300, y + 20 + i * 50, text=f"{k} : {v}", font=("Arial", 12))

# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()