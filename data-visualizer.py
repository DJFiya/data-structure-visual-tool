import tkinter as tk
import tkinter.ttk as ttk
import ast

from tree import TreeNode, build_binary_tree

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Data Visualizer")
        self.root.configure(bg="#1e1e2f")

        # Input Frame
        self.input_frame = tk.Frame(root, bg="#2c2c3e", bd=0)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        self._add_label_entry("Value (Python syntax):", 0)
        self.value_entry = self._add_entry(0)

        self._add_label_entry("Type:", 1)
        self.type_var = tk.StringVar(value="str")

        allowed_types = ["int", "float", "str", "list", "tuple", "set", "dict", "bool", "linkedlist", "stack", "queue", "binarytree", "2dlist", "range"]

        self.type_combobox = ttk.Combobox(
            self.input_frame, textvariable=self.type_var,
            values=allowed_types, state="readonly",
            font=("Segoe UI", 10), width=15
        )
        self.type_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.submit_btn = tk.Button(
            self.input_frame, text="Visualize", command=self.visualize,
            bg="#3b82f6", fg="white", activebackground="#2563eb", activeforeground="white",
            font=("Segoe UI", 11, "bold"), relief="flat", bd=0, padx=10, pady=6, cursor="hand2"
        )
        self.submit_btn.grid(row=2, columnspan=2, pady=14)

        # Canvas
        self.canvas_frame = tk.Frame(root, bg="#1e1e2f")
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas_width = 1440
        self.canvas_height = 640
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2

        self.canvas = tk.Canvas(
            self.canvas_frame, width=1440, height=self.canvas_height,
            bg="#ffffff", bd=0, highlightthickness=0, relief="flat"
        )
        self.canvas.pack()

    def _add_label_entry(self, text, row):
        label = tk.Label(
            self.input_frame, text=text, bg="#2c2c3e", fg="#f1f1f1", font=("Segoe UI", 10)
        )
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

    def _add_entry(self, row):
        entry = tk.Entry(
            self.input_frame, width=40, font=("Segoe UI", 10),
            bg="#ffffff", fg="#000000", relief="flat", bd=3, highlightthickness=1,
            highlightbackground="#cccccc", highlightcolor="#3b82f6"
        )
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        return entry

    def visualize(self):
        self.canvas.delete("all")

        raw_value = self.value_entry.get().strip()
        type_hint = self.type_var.get().strip().lower()

        def_types = {
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "tuple": tuple,
            "set": set,
            "dict": dict,
            "bool": bool,
            "range": range,
        }
        if type_hint in def_types:
            converter = def_types[type_hint]
        try:
            if type_hint == "bool":
                raw = raw_value.lower().strip()
                if raw in ("", "false", "none"):
                    value = False
                else:
                    try:
                        numeric = float(raw)
                        value = numeric != 0
                    except ValueError:
                        value = True
            elif type_hint in ("list", "tuple", "set"):
                stripped = raw_value.strip("[](){}")
                parts = [part.strip() for part in stripped.split(",") if part.strip()]
                if type_hint == "list":
                    value = parts
                elif type_hint == "tuple":
                    value = tuple(parts)
                else: 
                    value = set(parts)
            elif type_hint == "dict":
                stripped = raw_value.strip("{}")
                pairs = [pair.strip() for pair in stripped.split(",") if pair.strip()]
                d = {}
                for pair in pairs:
                    if ":" in pair:
                        k, v = pair.split(":", 1)
                        d[k.strip()] = v.strip()
                value = d
            elif type_hint == "int":
                try:
                    value = int(raw_value)
                except ValueError:
                    f = float(raw_value)
                    value = int(f)
                except ValueError as e:
                    raise e
            elif type_hint in ("linkedlist", "stack", "queue", "binarytree"):
                stripped = raw_value.strip("[](){}")
                parts = [part.strip() for part in stripped.split(",") if part.strip()]
                value = parts
            elif type_hint == "2dlist":
                try:
                    parsed = ast.literal_eval(raw_value)
                    if not (isinstance(parsed, list) and all(isinstance(row, list) for row in parsed)):
                        raise ValueError("Invalid 2D list format")
                    value = parsed
                except Exception:
                    raise ValueError("Invalid input for list2d")
            elif type_hint == "range":
                stripped = raw_value.strip("[](){}")
                parts = [part.strip() for part in stripped.split(",") if part.strip()]
                print(parts)
                if len(parts) == 1:
                    value = range(int(parts[0]))
                elif len(parts) == 2:
                    value = range(int(parts[0]), int(parts[1]))
                elif len(parts) == 3:
                    value = range(int(parts[0]), int(parts[1]), int(parts[2]))
                else:
                    raise ValueError("Invalid input for range. Use start, stop[, step]")
            else:
                value = converter(raw_value)
        except Exception as e:
            self._show_error(f"Cannot typecast entered value. Please enter a valid {type_hint} value.")
            return
        value_type = type_hint

        draw_fn = getattr(self, f"draw_{value_type}", self.draw_default)
        draw_fn(value, value_type)

    def _show_error(self, msg):
        self.canvas.create_text(
            self.center_x, 230, text=msg, fill="#ef4444", font=("Segoe UI", 20, "bold"), justify="center"
        )

    def draw_default(self, value, value_type):
        self.canvas.create_rectangle(self.center_x - 140, 180, self.center_x + 140, 270, fill="#f3f4f6", outline="#d1d5db", width=2)
        self.canvas.create_text(self.center_x, 205, text=f"Type: {value_type}", font=("Segoe UI", 13, "bold"))
        self.canvas.create_text(self.center_x, 240, text=f"Value: {str(value)}", font=("Segoe UI", 11))

    def draw_list(self, value, value_type):
        self.canvas.create_text(self.center_x, 40, text=f"Type: {value_type}", font=("Segoe UI", 20, "bold"))

        if isinstance(value, list) and all(isinstance(row, list) for row in value):
            box_size = 50
            spacing = 10
            num_rows = len(value)
            num_cols = max(len(row) for row in value) if num_rows > 0 else 0

            total_width = num_cols * (box_size + spacing) - spacing
            total_height = num_rows * (box_size + spacing) - spacing

            start_x = self.center_x - total_width // 2
            start_y = self.center_y - total_height // 2

            for row_idx, row in enumerate(value):
                for col_idx, item in enumerate(row):
                    x0 = start_x + col_idx * (box_size + spacing)
                    y0 = start_y + row_idx * (box_size + spacing)
                    x1 = x0 + box_size
                    y1 = y0 + box_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#bfdbfe", outline="#1d4ed8", width=2)
                    self.canvas.create_text((x0 + x1)//2, (y0 + y1)//2, text=str(item), font=("Segoe UI", 11))
            return

        box_width = 60
        y = self.center_y - box_width // 2
        max_boxes = min(len(value), 12)
        total_width = max_boxes * (box_width + 10) - 10
        start_x = self.center_x - total_width // 2

        for i, item in enumerate(value[:max_boxes]):
            x0 = start_x + i * (box_width + 10)
            x1 = x0 + box_width
            self.canvas.create_rectangle(x0, y, x1, y + 60, fill="#bfdbfe", outline="#1d4ed8", width=2)
            self.canvas.create_text((x0 + x1)//2, y + 30, text=str(item), font=("Segoe UI", 11))
        
        if len(value) > max_boxes:
            self.canvas.create_text(x1 + 40, y + 30, text="...", font=("Segoe UI", 16))


    def draw_tuple(self, value, value_type):
        self.draw_list(value, "tuple")

    def draw_set(self, value, value_type):
        self.draw_list(list(value), "set")
    
    def draw_2dlist(self, value, value_type):
        self.draw_list(value, "2dlist")

    def draw_dict(self, value, value_type):
        self.canvas.create_text(self.center_x, 40, text="Type: dict", font=("Segoe UI", 20, "bold"))
        y = 80
        for i, (k, v) in enumerate(value.items()):
            self.canvas.create_rectangle(self.center_x-250, y + i * 50, self.center_x+250, y + 40 + i * 50, fill="#fef9c3", outline="#ca8a04", width=2)
            self.canvas.create_text(self.center_x, y + 20 + i * 50, text=f"{k} : {v}", font=("Segoe UI", 11))
    
    def draw_linkedlist(self, value, value_type):
        self.canvas.create_text(self.center_x, 40, text="Type: Linked List", font=("Segoe UI", 20, "bold"))
        
        node_width = 80
        node_height = 60
        spacing = 20
        arrow_length = 30
        
        total_width = len(value) * node_width + (len(value) - 1) * (arrow_length + spacing)
        start_x = self.center_x - total_width // 2
        y = self.center_y - node_height // 2  # Center vertically based on node height
        
        if value:
            self.canvas.create_text(start_x + node_width // 2, y - 20, text="Head", font=("Segoe UI", 10, "italic"), fill="#6b7280")
        
        for i, item in enumerate(value):
            x0 = start_x + i * (node_width + arrow_length + spacing)
            x1 = x0 + node_width
            
            # Draw node
            self.canvas.create_rectangle(x0, y, x1, y + node_height, fill="#bbf7d0", outline="#16a34a", width=2)
            self.canvas.create_text((x0 + x1) // 2, y + node_height // 2, text=str(item), font=("Segoe UI", 11))
            
            # Draw arrow to next node (if not last)
            if i < len(value) - 1:
                arrow_start = x1
                arrow_end = x1 + arrow_length
                self.canvas.create_line(arrow_start, y + node_height // 2, arrow_end, y + node_height // 2, arrow=tk.LAST, fill="#16a34a", width=2)
        
        if value:
            # Draw "None" after the last node
            self.canvas.create_text(x1 + 40, y + node_height // 2, text="None", font=("Segoe UI", 10, "italic"), fill="#6b7280")

    
    def draw_stack(self, value, value_type):
        self.canvas.create_text(self.center_x, 40, text="Type: Stack (Top → Bottom)", font=("Segoe UI", 20, "bold"))

        box_width = 140
        box_height = 40
        start_x = self.center_x - box_width // 2
        start_y = 100

        for i, item in enumerate(reversed(value)): 
            y0 = start_y + i * (box_height + 10)
            y1 = y0 + box_height
            w_plus = i*10
            self.canvas.create_rectangle(start_x - w_plus, y0, start_x + box_width + w_plus, y1, fill="#fca5a5", outline="#b91c1c", width=2)
            self.canvas.create_text(start_x + box_width // 2, y0 + box_height // 2, text=str(item), font=("Segoe UI", 11))

        top_label_x = start_x + box_width + 40
        top_label_y = start_y + 20
        self.canvas.create_text(top_label_x, top_label_y, text="Top", font=("Segoe UI", 10, "bold"), fill="#ef4444")

        self.canvas.create_line(top_label_x - 10, top_label_y, start_x + box_width, top_label_y, arrow=tk.LAST, fill="#ef4444", width=2)
    
    def draw_queue(self, value, value_type):
        self.canvas.create_text(self.center_x, 40, text="Type: Queue (Front → Rear)", font=("Segoe UI", 20, "bold"))

        box_width = 80
        box_height = 60
        y = self.center_y - box_height // 2
        total_width = len(value) * (box_width + 10) - 10
        start_x = self.center_x - total_width // 2

        for i, item in enumerate(value):
            x0 = start_x + i * (box_width + 10)
            x1 = x0 + box_width
            self.canvas.create_rectangle(x0, y, x1, y + box_height, fill="#ddd6fe", outline="#7c3aed", width=2)
            self.canvas.create_text((x0 + x1) // 2, y + box_height//2, text=str(item), font=("Segoe UI", 11))
            
            if i < len(value) - 1:
                arrow_start = x1
                arrow_end = x1 + 10
                self.canvas.create_line(arrow_start, y + box_height//2, arrow_end + 10, y + 30, arrow=tk.LAST, fill="#7c3aed", width=2)

        if value:
            self.canvas.create_text(start_x - 10, y + 80, text="Front", font=("Segoe UI", 10), fill="#7c3aed")
            self.canvas.create_text(x1 + 30, y + 80, text="Rear", font=("Segoe UI", 10), fill="#7c3aed")
            front_arrow_x = start_x - 30
            rear_arrow_x = x1 + 30

            self.canvas.create_line(front_arrow_x, y + box_height//2, start_x, y + 30, arrow=tk.FIRST, fill="#7c3aed", width=2)

            self.canvas.create_line(rear_arrow_x + 20, y + 30, x1, y + 30, arrow=tk.LAST, fill="#7c3aed", width=2)

    def draw_binarytree(self, value, value_type):
        self.canvas.create_text(self.center_x, 40, text="Type: Binary Tree", font=("Segoe UI", 20, "bold"))

        values = [None if val.lower() == "none" else val for val in value]
        root = build_binary_tree(values)
        if not root:
            return

        level_height = 80
        node_radius = 25

        positions = {}

        def assign_positions(node, depth, x_min, x_max):
            if not node:
                return
            x = (x_min + x_max) // 2
            y = 100 + depth * level_height
            positions[node] = (x, y)
            assign_positions(node.left, depth + 1, x_min, x)
            assign_positions(node.right, depth + 1, x, x_max)

        assign_positions(root, 0, self.center_x - 600, self.center_x + 600)

        def draw_edges(node):
            if not node:
                return
            x, y = positions[node]
            for child in [node.left, node.right]:
                if child:
                    cx, cy = positions[child]
                    self.canvas.create_line(x, y + node_radius, cx, cy - node_radius, fill="#7c3aed", width=2)
                    draw_edges(child)

        def draw_nodes():
            for node, (x, y) in positions.items():
                self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="#ddd6fe", outline="#7c3aed", width=2)
                self.canvas.create_text(x, y, text=str(node.val), font=("Segoe UI", 11))

        draw_edges(root)
        draw_nodes()
    
    def draw_range(self, value, value_type):
        self.canvas.create_text(self.center_x, 40, text="Type: range", font=("Segoe UI", 20, "bold"))
        items = list(value)
        if not items:
            self.canvas.create_text(self.center_x, self.center_y, text="Empty range", font=("Segoe UI", 14, "italic"))
            return
        box_width = 60
        y = self.center_y - box_width // 2
        max_boxes = min(len(items), 12)
        total_width = max_boxes * (box_width + 10) - 10
        start_x = self.center_x - total_width // 2

        for i, item in enumerate(items[:max_boxes]):
            x0 = start_x + i * (box_width + 10)
            x1 = x0 + box_width
            self.canvas.create_rectangle(x0, y, x1, y + 60, fill="#fde68a", outline="#b45309", width=2)
            self.canvas.create_text((x0 + x1)//2, y + 30, text=str(item), font=("Segoe UI", 11))
        if len(items) > max_boxes:
            self.canvas.create_text(x1 + 40, y + 30, text="...", font=("Segoe UI", 16))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()
