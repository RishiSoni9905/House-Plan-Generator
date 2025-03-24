import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_floor_plan(plot_length, plot_breadth, num_rooms, num_bathrooms, num_kitchens, has_living_room=True):
    if not has_living_room:
        print("Living room is mandatory for this layout strategy.")
        return

    fig, ax = plt.subplots(figsize=(plot_length / 10, plot_breadth / 10))

    color_palette = {
        "Living": "lightcoral",
        "Room": "lightblue",
        "Kitchen": "khaki",
        "Bathroom": "lightgray",
        "Entrance": "salmon"
    }

    layout_grid = [[], [], []]  # Top, Middle, Bottom
    top_components = []
    middle_components = []
    bottom_components = []

    rooms = [f'Room {i+1}' for i in range(num_rooms)]
    kitchens = [f'Kitchen {i+1}' for i in range(num_kitchens)]
    bathrooms = [f'Bathroom {i+1}' for i in range(num_bathrooms)]

    components = rooms + kitchens + bathrooms

    def safe_pop(lst):
        return lst.pop(0) if lst else None

    # Fill top and bottom rows first
    for _ in range(2):
        if components:
            top_components.append(safe_pop(components))
        if components:
            bottom_components.append(safe_pop(components))

    # Add Living Room at center (index 1)
    middle_components = [None, "Living Room", None]

    # Fill remaining components to middle row (left/right of Living Room)
    if components:
        if middle_components[0] is None:
            middle_components[0] = safe_pop(components)
    if components:
        if middle_components[2] is None:
            middle_components[2] = safe_pop(components)

    # Fill rest of the components in round robin
    while components:
        if len(top_components) <= len(bottom_components):
            top_components.append(safe_pop(components))
        else:
            bottom_components.append(safe_pop(components))

    # Always add Entrance at the end of bottom row
    bottom_components.append("Entrance")

    # Filter out None from middle row if no components left for that side
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
    plt.show()

# Example usage
generate_floor_plan(plot_length=30, plot_breadth=40, num_rooms=4, num_bathrooms=2, num_kitchens=1)


