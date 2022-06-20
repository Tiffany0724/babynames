"""
File: babygraphics.py
Name: Tiffany
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import tkinter as tk # from campy.private.backends import tk
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    return ((width - 2 * GRAPH_MARGIN_SIZE) / len (YEARS)) * year_index + GRAPH_MARGIN_SIZE


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # To cleaning the space first, deleted all existed  lines on the canvas

    # To build horizontal lines on canvas
    canvas.create_line (GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                        width = LINE_WIDTH, fill = "black")
    canvas.create_line (GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
                        CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, width = LINE_WIDTH, fill = "black")

    # To build straight lines and year  text labels on canvas
    for index in range (len (YEARS)):
        canvas.create_line (get_x_coordinate (CANVAS_WIDTH, index), 0, get_x_coordinate (CANVAS_WIDTH, index),CANVAS_HEIGHT, width = LINE_WIDTH, fill = 'black')
        canvas.create_text (get_x_coordinate (CANVAS_WIDTH, index) + TEXT_DX, CANVAS_HEIGHT,text = str (YEARS [ index ]), anchor = tk.SW, fill = 'black')


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """

    draw_fixed_lines (canvas)  # draw the fixed background grid

    coloured_id = 0 # start in 0
    for name in lookup_names: # wrap coloured_id in four
        coloured_id %= len (COLORS) # For each year, total position list to store all of the ranking position
        pos_list = [ ]
        for yr_id in range (len (YEARS)): # The yearly position[x,y]
            year_pos = [ get_x_coordinate (CANVAS_WIDTH, yr_id) ]  # To get the x position
            """
            1. To get y position by searching year data from name_data    
            2. If rank existed, transfer these data to valid y position
            3. y position: start point + (rank * valid canvas height // max range)
            """
            if str (YEARS [ yr_id ]) in name_data [ name ]:
                year_pos.append (int (name_data [ name ] [ str (YEARS [ yr_id ]) ]) * (
                            CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) // MAX_RANK + GRAPH_MARGIN_SIZE)
            else:
                # To add the yearly position into total position list
                year_pos.append (CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)
            pos_list.append (year_pos)
            rank = str (name_data [ name ].get (str (YEARS [ yr_id ]))) if str (YEARS [ yr_id ]) in name_data [
                name ] else "*"   # To get rank in string format
            canvas.create_text (year_pos [ 0 ] + TEXT_DX, year_pos [ 1 ], text = str (name) + " " + rank, anchor = tk.SW, fill = COLORS [ coloured_id ])
        # To create text and lining amount would be (points number  - 1)
        for i in range (len (YEARS) - 1):
            # To create lines between every year's position
            canvas.create_line (pos_list [ i ] [ 0 ], pos_list [ i ] [ 1 ], pos_list [ i + 1 ] [ 0 ],
                                pos_list [ i + 1 ] [ 1 ], width = LINE_WIDTH, fill = COLORS [ coloured_id ])
        # To switch to next colour
        coloured_id += 1


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
