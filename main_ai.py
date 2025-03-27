import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import json
import os

FEEDBACK_FILE = "feedback.json"

if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w") as file:
        json.dump({"good": {}, "bad": []}, file)

def load_feedback():
    with open(FEEDBACK_FILE, "r") as file:
        return json.load(file)

def save_feedback(layout, rating, length, breadth):
    data = load_feedback()
    key = f"{length}-{breadth}"
    if rating >= 4:
        if key not in data["good"]:
            data["good"][key] = []
        if layout not in data["good"][key]:
            data["good"][key].append(layout)
    else:
        if layout not in data["bad"]:
            data["bad"].append(layout)
    with open(FEEDBACK_FILE, "w") as file:
        json.dump(data, file, indent=4)

def generate_layout(plot_length, plot_breadth, num_rooms, num_bathrooms, num_kitchens):
    components = ["Room"] * num_rooms + ["Kitchen"] * num_kitchens + ["Bathroom"] * num_bathrooms
    random.shuffle(components)
    
    top_row, middle_row, bottom_row = [], ["Living Room"], []
    
    while components:
        if components:
            top_row.append(components.pop())
        if components:
            bottom_row.append(components.pop())
        if components:
            middle_row.insert(0, components.pop()) if len(middle_row) % 2 == 0 else middle_row.append(components.pop())
    
    if bottom_row:
        if random.choice([True, False]):
            bottom_row.insert(0, "Entrance")
        else:
            bottom_row.append("Entrance")
    else:
        bottom_row.append("Entrance")
    
    return [top_row, middle_row, bottom_row]

def draw_floor_plan(layout, plot_length, plot_breadth):
    fig, ax = plt.subplots()
    row_heights = plot_breadth / 3
    y_positions = [2 * row_heights, row_heights, 0]
    color_palette = {"Living Room": "lightcoral", "Room": "lightblue", "Kitchen": "khaki", "Bathroom": "lightgray", "Entrance": "salmon"}
    
    for i, row in enumerate(layout):
        x_pos = 0
        total_components = len(row)
        widths = []
        
        if total_components > 0:
            base_width = plot_length / total_components
            for comp in row:
                if comp == "Bathroom":
                    widths.append(base_width * random.uniform(0.6, 0.8))
                elif comp == "Kitchen":
                    widths.append(base_width * random.uniform(0.8, 1.0))
                elif comp == "Room":
                    widths.append(base_width * random.uniform(1.0, 1.2))
                elif comp == "Living Room":
                    widths.append(base_width * random.uniform(1.5, 2.0))
                else:
                    widths.append(base_width)
            widths = [w * (plot_length / sum(widths)) for w in widths]
        
        for comp, width in zip(row, widths):
            ax.add_patch(patches.Rectangle((x_pos, y_positions[i]), width, row_heights, edgecolor='black', facecolor=color_palette.get(comp, 'white')))
            ax.text(x_pos + width/2, y_positions[i] + row_heights/2, f"{comp}\n{int(width)}x{int(row_heights)}", ha='center', va='center')
            x_pos += width
    
    ax.set_xlim(0, plot_length)
    ax.set_ylim(0, plot_breadth)
    ax.set_aspect('equal')
    plt.title("Floor Plan")
    return fig

def on_generate(mode):
    length, breadth = int(entry_length.get()), int(entry_breadth.get())
    rooms, bathrooms, kitchens = int(entry_rooms.get()), int(entry_bathrooms.get()), int(entry_kitchens.get())
    global current_layout
    
    if mode == "demo":
        feedback = load_feedback()
        key = f"{length}-{breadth}"
        layouts = feedback["good"].get(key, [])
        current_layout = random.choice(layouts) if layouts else generate_layout(length, breadth, rooms, bathrooms, kitchens)
    else:
        current_layout = generate_layout(length, breadth, rooms, bathrooms, kitchens)
    
    fig = draw_floor_plan(current_layout, length, breadth)
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame_output)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def on_feedback(rating):
    length, breadth = int(entry_length.get()), int(entry_breadth.get())
    save_feedback(current_layout, rating, length, breadth)
    on_generate("train")

def ui_setup(mode="train"):
    global root, frame_input, frame_output, canvas, entry_length, entry_breadth, entry_rooms, entry_bathrooms, entry_kitchens
    root = tk.Tk()
    root.title("AI Floor Plan Generator")
    
    frame_input = tk.Frame(root)
    frame_input.pack()
    
    tk.Label(frame_input, text="Plot Length:").grid(row=0, column=0)
    entry_length = tk.Entry(frame_input)
    entry_length.grid(row=0, column=1)
    
    tk.Label(frame_input, text="Plot Breadth:").grid(row=1, column=0)
    entry_breadth = tk.Entry(frame_input)
    entry_breadth.grid(row=1, column=1)
    
    tk.Label(frame_input, text="Rooms:").grid(row=2, column=0)
    entry_rooms = tk.Entry(frame_input)
    entry_rooms.grid(row=2, column=1)
    
    tk.Label(frame_input, text="Bathrooms:").grid(row=3, column=0)
    entry_bathrooms = tk.Entry(frame_input)
    entry_bathrooms.grid(row=3, column=1)
    
    tk.Label(frame_input, text="Kitchens:").grid(row=4, column=0)
    entry_kitchens = tk.Entry(frame_input)
    entry_kitchens.grid(row=4, column=1)
    
    tk.Button(frame_input, text="Generate", command=lambda: on_generate(mode)).grid(row=5, column=0, columnspan=2)
    frame_output = tk.Frame(root)
    frame_output.pack()
    
    if mode == "train":
        tk.Button(root, text="Like", command=lambda: on_feedback(5)).pack(side='left')
        tk.Button(root, text="Dislike", command=lambda: on_feedback(2)).pack(side='right')
    
    global canvas
    canvas = None
    root.mainloop()

ui_setup("demo")
