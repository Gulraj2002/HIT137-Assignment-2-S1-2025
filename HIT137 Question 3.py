#!/usr/bin/env python
# coding: utf-8

# In[3]:


import turtle  # Importing the necessary module for turtle graphics

def build_tree(painter, trunk_length, left_turn, right_turn, levels, shrink_factor):
    """
    Generates a fractal tree pattern using recursive drawing with the turtle.
    This function forms the core of the tree generation process.
    It draws branches and recursively calls itself for subsequent levels.

    Args:
        painter (Turtle): The turtle object responsible for drawing.
                          Think of this as our digital pen.
        trunk_length (float): The length of the current branch being drawn.
                              This length decreases with each level of recursion.
        left_turn (float): The angle in degrees to turn left for a new branch.
                           This angle influences the shape of the tree.
        right_turn (float): The angle in degrees to turn right for a new branch.
                            This angle also plays a crucial role in the tree's appearance.
        levels (int): The number of recursive branching levels remaining.
                      This determines the complexity and detail of the tree.
        shrink_factor (float): The factor by which subsequent branch lengths are reduced.
                               A value less than 1 ensures the tree gets smaller as it branches.
    """
    if levels == 0:
        # Base case for the recursion: when no more levels are left, draw a leaf.
        painter.color("forest green")  # Set the color to a lush green for the leaves.
        painter.dot(trunk_length * 0.6)  # Draw a small circle representing a leaf.
        return  # End the function call for this branch.

    branch_thickness = int(levels * 1.5)  # Determine the thickness of the current branch.
                                         # Thicker branches at the base for a more natural look.
    painter.pensize(branch_thickness)  # Set the thickness of the pen.
    branch_color = (0.4 + 0.6 * levels / 8, 0.2, 0.15)  # Define a brownish color for the branches.
                                                       # The color slightly lightens at higher levels.
    painter.color(branch_color)  # Set the color of the pen for drawing the branch.

    painter.forward(trunk_length)  # Draw the current branch forward.

    painter.left(left_turn)  # Turn the turtle to the left by the specified angle.
    build_tree(painter, trunk_length * shrink_factor, left_turn, right_turn, levels - 1, shrink_factor)
    # Recursively call the function to draw the left sub-branch.
    # The branch length is reduced, and the recursion level decreases.

    painter.right(left_turn + right_turn)  # Turn the turtle to the right to prepare for the right branch.
    build_tree(painter, trunk_length * shrink_factor, left_turn, right_turn, levels - 1, shrink_factor)
    # Recursively call the function to draw the right sub-branch.
    # Similar to the left branch, the length is reduced, and the level decreases.

    painter.left(right_turn)  # Turn the turtle back to the original orientation after drawing the right branch.
    painter.backward(trunk_length)  # Move the turtle back to the starting point of the current branch.
                                   # This is crucial for drawing the subsequent branches correctly.

def initiate_tree():
    """
    Sets up the turtle graphics environment and gets user input to draw a tree.
    This function handles the initial setup and user interaction.
    """
    try:
        angle_left = float(input("Specify the left branch angle (e.g., 20): "))  # Enter the angle (in degrees) for the left branches (e.g., 20).
        angle_right = float(input("Indicate the right branch angle (e.g.,25): "))  # Enter the angle (in degrees) for the right branches (e.g., 25).
        initial_length = float(input("Set the starting branch length (e.g.,100): "))  # Enter the length of the initial trunk (e.g., 100).
        depth_level = int(input("Determine the recursion depth (e.g.,5): "))  # Enter the number of branching levels (e.g., 5).
        reduction = float(input("Define the branch length reduction factor (e.g., 0.65): "))
        # Enter a value between 0 and 1 to reduce branch length at each level (e.g., 0.7).

        screen = turtle.Screen()  # Create the main window for the turtle graphics.
        screen.setup(width=700, height=550)  # Set the dimensions of the drawing window.
        screen.title("My Own Recursive Tree")  # Set the title of the turtle graphics window.
        artist = turtle.Turtle()  # Create a turtle object, which will do the drawing.
        artist.speed("fastest")  # Set the drawing speed to the fastest for quick rendering.
        artist.penup()  # Lift the pen so that the turtle doesn't draw while moving.
        artist.left(90)  # Turn the turtle upwards to start drawing the tree from the bottom.
        artist.goto(0, -200)  # Move the turtle to the starting position at the bottom center.
        artist.pendown()  # Put the pen down so that the turtle starts drawing.

        build_tree(artist, initial_length, angle_left, angle_right, depth_level, reduction)
        # Call the main recursive function to start drawing the tree.

        screen.mainloop()  # Keep the turtle graphics window open until it is manually closed.

    except turtle.Terminator:
        print("Drawing session ended.")  # Handle the event when the user closes the turtle window.
    finally:
        try:
            turtle.bye()  # Clean up the turtle graphics resources.
        except turtle.Terminator:
            pass  # Ignore if the screen is already closed.

if __name__ == "__main__":
    initiate_tree()  # Call the function to start the tree drawing process when the script is run.


# In[ ]:




