import datetime
import PySimpleGUI as sg
def get_current_time():
    """
    Return the current time as a datetime object.

    Returns:
        datetime.datetime: The current date and time.
    """
    return datetime.datetime.now()
def make_window():
    """
    Create the main window of the Awesome Habbit Tracker.

    The window contains three rows: the first row contains an image, the second row contains a title, a text input, a button to choose an image, and the current time, the third row contains four empty columns.

    The window is finalized and margins are set to (0,0).

    Returns:
        sg.Window: The created window.
    """
    layout = make_layout()
    window = sg.Window("Awesome Habbit Tracker",layout,margins=(0,0),finalize=True)
    return window
def main_title():
    """
    Create a Text element with the current date and time, formatted as a string.

    The string is in the format "Weekday, DD.MM.YYYY, HH:MM:SS" and is centered horizontally and vertically.

    The Text element is given the key "-TIME-" and has the font "New Amsterdam" with size 24.

    Returns:
        sg.Text: The Text element with the current date and time.
    """
    current_time = get_current_time()
    text = sg.Text(f"{current_time.strftime("%A")}, {current_time.day}.{current_time.month}.{current_time.year}, {current_time.hour}:{current_time.minute}:{current_time.second}", 
                   justification="Center", expand_y=True, key="-TIME-",font=("New Amsterdam",24))
    return text
def make_four_column():
    """
    Create four empty columns and return them as a tuple of four elements.

    The columns are given the keys (-COLUMN-, 1), (-COLUMN-, 2), (-COLUMN-, 3), and (-COLUMN-, 4) and are 
    all set to expand in the x-direction.

    Returns:
        tuple: A tuple of four sg.Column elements.
    """
    global icon
    return sg.vtop(sg.Column([[]],key=("-COLUMN-", 1),expand_x=True)),sg.vtop(sg.Column([[]],key=("-COLUMN-", 2),expand_x=True)), sg.vtop(sg.Column([[]],key=("-COLUMN-", 3),expand_x=True)), sg.vtop(sg.Column([[]],key=("-COLUMN-", 4),expand_x=True))
def make_layout(*args):
    """
    Create a layout for the main window of the Awesome Habbit Tracker.

    The layout consists of three rows.

    The first row contains a single Image element with the key "-IMAGE-", which is centered horizontally and has no padding.

    The second row contains a Text element with the key "-TEXT-", a Push element, a Button element with the key "-CHOOSE-", and a Text element with the current date and time.

    The third row contains four empty columns, which are all set to expand in the x-direction.

    Returns:
        list: A list of lists, where each sublist is a row in the layout.
    """

    title = main_title()
    columns = make_four_column()
    layout = [[sg.Image(None,pad=(0,0),key="-IMAGE-")],
              [sg.Push(),title,sg.Text(key="-TEXT-"),sg.Button("Choose", key="-CHOOSE-")],
              [sg.Push(),columns[0], columns[1],columns[2],columns[3],sg.Push()]
              ]
    return layout
def update_time(window):
    """
    Update the Text element with the key "-TIME-" in the given window with the current date and time.

    The string is in the format "Weekday, DD.MM.YYYY, HH:MM:SS" and is centered horizontally and vertically.

    Args:
        window (sg.Window): The window containing the Text element to be updated.
    """
    current_time = get_current_time()
    window["-TIME-"].update(f"{current_time.strftime("%A")}, {current_time.day}.{current_time.month}.{current_time.year}, {current_time.hour}:{current_time.minute}:{current_time.second}")