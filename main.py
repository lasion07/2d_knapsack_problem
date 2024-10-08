"""
    2D Knapsack
"""
import os
import time
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyomo.environ as pyo

from matplotlib.patches import Rectangle


COLORS = {
    "Aqua": "#00FFFF",
    "Azure": "#F0FFFF",
    "Beige": "#F5F5DC",
    "Blue": "#0000FF",
    "Brown": "#A52A2A",
    "Chocolate": "#D2691E",
    "Coral": "#FF7F50",
    "Crimson": "#DC143C",
    "Cyan": "#00FFFF",
    "DarkBlue": "#00008B",
    "DarkCyan": "#008B8B",
    # "DarkGray": "#A9A9A9",
    "DarkGreen": "#006400",
    "DarkKhaki": "#BDB76B",
    "DarkMagenta": "#8B008B",
    "DarkOliveGreen": "#556B2F",
    "DarkOrange": "#FF8C00",
    "DarkOrchid": "#9932CC",
    "DarkRed": "#8B0000",
    "DarkSalmon": "#E9967A",
    "DarkSeaGreen": "#8FBC8F",
    "DarkSlateBlue": "#483D8B",
    # "DarkSlateGray": "#2F4F4F",
    "DarkTurquoise": "#00CED1",
    "DarkViolet": "#9400D3",
    "DeepPink": "#FF1493",
    "DeepSkyBlue": "#00BFFF",
    # "DimGray": "#696969",
    "DodgerBlue": "#1E90FF",
    "FireBrick": "#B22222",
    "FloralWhite": "#FFFAF0",
    "ForestGreen": "#228B22",
    "Fuchsia": "#FF00FF",
    "Gainsboro": "#DCDCDC",
    "GhostWhite": "#F8F8FF",
    "Gold": "#FFD700",
    "GoldenRod": "#DAA520",
    # "Gray": "#808080",
    "Green": "#008000",
    "GreenYellow": "#ADFF2F",
    "HoneyDew": "#F0FFF0",
    "HotPink": "#FF69B4",
    "IndianRed": "#CD5C5C",
    "Indigo": "#4B0082",
    "Ivory": "#FFFFF0",
    "Khaki": "#F0E68C",
    "Lavender": "#E6E6FA",
    "LavenderBlush": "#FFF0F5",
    "LawnGreen": "#7CFC00",
    "LemonChiffon": "#FFFACD",
    "LightBlue": "#ADD8E6",
    "LightCoral": "#F08080",
    "LightCyan": "#E0FFFF",
    "LightGoldenRodYellow": "#FAFAD2",
    # "LightGray": "#D3D3D3",
    "LightGreen": "#90EE90",
    "LightPink": "#FFB6C1",
    "LightSalmon": "#FFA07A",
    "LightSeaGreen": "#20B2AA",
    "LightSkyBlue": "#87CEFA",
    # "LightSlateGray": "#778899",
    "LightSteelBlue": "#B0C4DE",
    "LightYellow": "#FFFFE0",
    "Lime": "#00FF00",
    "LimeGreen": "#32CD32",
    "Linen": "#FAF0E6",
    "Magenta": "#FF00FF",
    "Maroon": "#800000",
    "MediumAquaMarine": "#66CDAA",
    "MediumBlue": "#0000CD",
    "MediumOrchid": "#BA55D3",
    "MediumPurple": "#9370DB",
    "MediumSeaGreen": "#3CB371",
    "MediumSlateBlue": "#7B68EE",
    "MediumSpringGreen": "#00FA9A",
    "MediumTurquoise": "#48D1CC",
    "MediumVioletRed": "#C71585",
    "MidnightBlue": "#191970",
    "MintCream": "#F5FFFA",
    "MistyRose": "#FFE4E1",
    "Moccasin": "#FFE4B5",
    "NavajoWhite": "#FFDEAD",
    "Navy": "#000080",
    "OldLace": "#FDF5E6",
    "Olive": "#808000",
    "OliveDrab": "#6B8E23",
    "Orange": "#FFA500",
    "OrangeRed": "#FF4500",
    "Orchid": "#DA70D6",
    "PaleGoldenRod": "#EEE8AA",
    "PaleGreen": "#98FB98",
    "PaleTurquoise": "#AFEEEE",
    "PaleVioletRed": "#DB7093",
    "PapayaWhip": "#FFEFD5",
    "PeachPuff": "#FFDAB9",
    "Peru": "#CD853F",
    "Pink": "#FFC0CB",
    "Plum": "#DDA0DD",
    "PowderBlue": "#B0E0E6",
    "Purple": "#800080",
    "RebeccaPurple": "#663399",
    "Red": "#FF0000",
    "RosyBrown": "#BC8F8F",
    "RoyalBlue": "#4169E1",
    "SaddleBrown": "#8B4513",
    "Salmon": "#FA8072",
    "SandyBrown": "#F4A460",
    "SeaGreen": "#2E8B57",
    "SeaShell": "#FFF5EE",
    "Sienna": "#A0522D",
    "Silver": "#C0C0C0",
    "SkyBlue": "#87CEEB",
    "SlateBlue": "#6A5ACD",
    # "SlateGray": "#708090",
    "Snow": "#FFFAFA",
    "SpringGreen": "#00FF7F",
    "SteelBlue": "#4682B4",
    "Tan": "#D2B48C",
    "Teal": "#008080",
    "Thistle": "#D8BFD8",
    "Tomato": "#FF6347",
    "Turquoise": "#40E0D0",
    "Violet": "#EE82EE",
    "Wheat": "#F5DEB3",
    "White": "#FFFFFF",
    "WhiteSmoke": "#F5F5F5",
    "Yellow": "#FFFF00",
    "YellowGreen": "#9ACD32"
}


if __name__ == '__main__':
    # INPUT
    container_width = 11
    container_height = 11
    item_num = 20

    # Map color
    color_dict = {'container': 'lightgrey'}

    ## List of items, each represented as (width, height, value)
    items = []
    for i in range(item_num):
        iw, ih = random.randint(1, 4), random.randint(1, 4)
        items.append((iw, ih))

    for i, color in enumerate(COLORS.values()):
        if i > len(items):
            break

        color_dict[i] = color

    print(f"Container Dimensions: {container_width} x {container_height}")

    variables = [] # List of variables
    item_placement_map = {}
    overlap_map = {}
    start_time = time.time()

    # Intialize map to place items
    for i, item in enumerate(items):
        item_placement_map[f'{i}'] = []

    # Intialize overlapping map
    for row in range(container_height):
        for column in range(container_width):
            overlap_map[f'{row},{column}'] = []

    # Try to place items
    for row in range(container_height): # row to place items
        for column in range(container_width): # column to place items
            
            for i, item in enumerate(items): # Select item
                iw, ih = item # width and height of the item

                if row + ih > container_height or column + iw > container_width:
                    continue

                var_name = f'z_{i}_{row}_{column}'
                variables.append(var_name)
                item_placement_map[f'{i}'].append(var_name)
                
                # Update overlap map
                for irow in range(ih):
                    for icolumn in range(iw):
                        overlap_map[f'{row+irow},{column+icolumn}'].append(var_name)
    

    # Define optimization model
    model = pyo.ConcreteModel()

    # Define model's variables with binary types
    model.x = pyo.Var(variables, within=pyo.Binary)

    # Objective: Maximize sum of variables
    expr = 0
    for variable in model.x:
        expr += model.x[variable]
    model.obj = pyo.Objective(expr=expr, sense=pyo.maximize)

    # Constraints
    model.cons = pyo.ConstraintList()
    ## A item type only be placed once
    for item_type in item_placement_map:
        expr = 0
        for variable in item_placement_map[item_type]:
            expr += model.x[variable]
        model.cons.add(expr <= 1)
    # Item cannot overlap
    for pos in overlap_map:
        expr = 0
        for variable in overlap_map[pos]:
            expr += model.x[variable]
        model.cons.add(expr <= 1)

    # Select solver and solve model
    opt = pyo.SolverFactory('glpk')
    opt.solve(model)

    print('Execution time:', time.time() - start_time)

    # Display result
    # model.display()
    
    # Visualize
    plt.figure(figsize=(6, 6))

    fig = plt.gcf()
    ax = fig.gca()

    ax.add_patch(Rectangle(xy=(0, 0), width=container_width, height=container_height, edgecolor='white', facecolor=color_dict['container'], alpha=1, linewidth=2))

    # unfitted_items = []
    fitted_items = []
    fitted_items_count = 0
    for var_name in model.x:
        value = pyo.value(model.x[var_name])

        if value == 0:
            continue

        fitted_items_count += 1
        splitted_var_name = var_name.split('_')
        item_type = int(splitted_var_name[1])
        position = int(splitted_var_name[3]), int(splitted_var_name[2])
        width, height = items[item_type]
        fitted_items.append((item_type, position))
        ax.add_patch(Rectangle(xy=position, width=width, height=height, edgecolor='white', facecolor=color_dict[item_type], alpha=0.7, linewidth=2))

    print('FITTED ITEMS:')
    for item_type, position in sorted(fitted_items, key=lambda x: x[0]):
        print(f'Item {item_type} at position {position}')

    print(f'Fitted {fitted_items_count}/{item_num}')

    plt.xlim([0, container_width])
    plt.ylim([0, container_height])

    plt.show()

    print('Process successfully')
