import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_floor_plan(plot_length, plot_breadth, num_rooms, num_bathrooms, num_kitchens, has_living_room=True):
    if not has_living_room:
        messagebox.showerror("Error", "Living room is mandatory.")
        return None

    fig, ax = plt.subplots(figsize=(plot_length / 10, plot_breadth / 10))

    color_palette = {
        "Living": "lightcoral",
        "Room": "lightblue",
        "Kitchen": "khaki",
        "Bathroom": "lightgray",
        "Entrance": "salmon"
    }

    layout_grid = [[], [], []]
    top_components = []
    middle_components = []
    bottom_components = []

    rooms = [f'Room {i+1}' for i in range(num_rooms)]
    kitchens = [f'Kitchen {i+1}' for i in range(num_kitchens)]
    bathrooms = [f'Bathroom {i+1}' for i in range(num_bathrooms)]

    components = rooms + kitchens + bathrooms

    def safe_pop(lst):
        return lst.pop(0) if lst else None

    for _ in range(2):
        if components:
            top_components.append(safe_pop(components))
        if components:
            bottom_components.append(safe_pop(components))

    middle_components = [None, "Living Room", None]
    if components and middle_components[0] is None:
        middle_components[0] = safe_pop(components)
    if components and middle_components[2] is None:
        middle_components[2] = safe_pop(components)

    while components:
        if len(top_components) <= len(bottom_components):
            top_components.append(safe_pop(components))
        else:
            bottom_components.append(safe_pop(components))

    bottom_components.append("Entrance")
    middle_components = [comp for comp in middle_components if comp is not None]

    layout_grid[0] = top_components
    layout_grid[1] = middle_components
    layout_grid[2] = bottom_components

    row_heights = plot_breadth / 3
    y_positions = [2 * row_heights, row_heights, 0]

    def draw_row(row, y, total_width):
        widths = []
        if "Living Room" in row:
            idx = row.index("Living Room")
            side_count = len(row) - 1
            max_living_width = total_width * 0.45
            side_width = (total_width - max_living_width) / side_count if side_count > 0 else 0
            if side_width < total_width * 0.1:
                side_width = total_width * 0.1
                max_living_width = total_width - side_width * side_count
            for i in range(len(row)):
                widths.append(max_living_width if i == idx else side_width)
        else:
            count = len(row)
            widths = [total_width / count] * count if count else []

        positions = [sum(widths[:i]) for i in range(len(widths))]
        for i, comp in enumerate(row):
            x = positions[i]
            color = color_palette.get(comp.split()[0], 'white')
            rect = patches.Rectangle((x, y), widths[i], row_heights, edgecolor='black', facecolor=color)
            ax.add_patch(rect)
            ax.text(x + widths[i]/2, y + row_heights/2, comp, ha='center', va='center', fontsize=8)

    for row_idx, row in enumerate(layout_grid):
        if row:
            draw_row(row, y_positions[row_idx], plot_length)

    ax.set_xlim(0, plot_length)
    ax.set_ylim(0, plot_breadth)
    ax.set_aspect('equal')
    plt.title("Generated Floor Plan")
    plt.tight_layout()

    return fig


# ---------------------- TKINTER UI ----------------------

def on_generate():
    try:
        length = int(entry_length.get())
        breadth = int(entry_breadth.get())
        rooms = int(entry_rooms.get())
        bathrooms = int(entry_bathrooms.get())
        kitchens = int(entry_kitchens.get())

        # Validation
        if length <= 0 or breadth <= 0:
            raise ValueError("Plot size must be positive.")
        if not (1 <= rooms <= 6):
            raise ValueError("Rooms must be between 1 and 6.")
        if not (1 <= kitchens <= 2):
            raise ValueError("Kitchens must be between 1 and 2.")
        if not (1 <= bathrooms <= 3):
            raise ValueError("Bathrooms must be between 1 and 3.")

        fig = generate_floor_plan(length, breadth, rooms, bathrooms, kitchens)
        if fig:
            global canvas
            if canvas:
                canvas.get_tk_widget().destroy()
            canvas = FigureCanvasTkAgg(fig, master=frame_output)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("🏠 House Floor Plan Generator")
root.geometry("1000x750")
root.configure(bg="#f0f4f7")

frame_input = tk.Frame(root, bg="#e2ecf3", padx=20, pady=20, bd=2, relief='groove')
frame_input.pack(side='top', fill='x', padx=20, pady=10)

tk.Label(frame_input, text="Plot Length:", bg="#e2ecf3").grid(row=0, column=0, sticky='e', padx=10, pady=5)
entry_length = tk.Entry(frame_input)
entry_length.grid(row=0, column=1, pady=5)

tk.Label(frame_input, text="Plot Breadth:", bg="#e2ecf3").grid(row=1, column=0, sticky='e', padx=10, pady=5)
entry_breadth = tk.Entry(frame_input)
entry_breadth.grid(row=1, column=1, pady=5)

tk.Label(frame_input, text="Number of Rooms (1-6):", bg="#e2ecf3").grid(row=2, column=0, sticky='e', padx=10, pady=5)
entry_rooms = tk.Entry(frame_input)
entry_rooms.grid(row=2, column=1, pady=5)

tk.Label(frame_input, text="Number of Bathrooms (1-3):", bg="#e2ecf3").grid(row=3, column=0, sticky='e', padx=10, pady=5)
entry_bathrooms = tk.Entry(frame_input)
entry_bathrooms.grid(row=3, column=1, pady=5)

tk.Label(frame_input, text="Number of Kitchens (1-2):", bg="#e2ecf3").grid(row=4, column=0, sticky='e', padx=10, pady=5)
entry_kitchens = tk.Entry(frame_input)
entry_kitchens.grid(row=4, column=1, pady=5)

btn_generate = tk.Button(frame_input, text="Generate Floor Plan", command=on_generate, bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'))
btn_generate.grid(row=5, column=0, columnspan=2, pady=15)

frame_output = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
frame_output.pack(fill='both', expand=True, padx=20, pady=10)

canvas = None

root.mainloop()