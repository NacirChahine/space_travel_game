import os
import sys
import pygame

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    # Adjust path if running from src directory
    if base_path.endswith('src'):
        base_path = os.path.dirname(base_path)
        
    return os.path.join(base_path, 'assets', relative_path)

def split_text(text, font, max_width):
    """
    Splits the text into multiple lines based on the max width of the screen.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:  # Check if the line is within the screen width
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)  # Add the last line
    return lines
