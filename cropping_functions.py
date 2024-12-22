import PySimpleGUI as sg
from PIL import Image, ImageOps
import os

def set_image(path):
    """
    Given a path to an image file, open it using PIL and return its size as a tuple of two integers (width, height).
    """
    with Image.open(path) as im:
        return im.size
def crop(path, x1, y1, x2, y2):
    """
    Given a path to an image file and two sets of coordinates (x1,y1) and (x2,y2), open the image using PIL and return a cropped version of it.
    The coordinates are in the coordinates of the opened image, with the top-left corner being (0,0) and the y-axis pointing downwards.
    """
    with Image.open(path) as im:
        sg.Print(x1,y1,x2,y2)
        return im.crop((x1, y1, x2, y2))

def get_image_path(path):
    """Given a path to an image file, open it using PIL and check if image width is larger than 700.
    If it is not, show a popup and return None. If image is not in PNG format, save it as PNG in the current directory and return the path.
    If an OSError occurs, pass and return the path as is"""
    try:
        with Image.open(path) as im:
            if im.size[0]<700:
                sg.popup("Image width must be widen!")
                return None 
            if im.format != "png" or im.format != "PNG":
                im.save(f"{os.getcwd()}\\image.png")
                return f"{os.getcwd()}\\image.png"
    except OSError:
        pass
    return path
def crop_image(path):
    """
    Opens a new window with a graph element to crop an image.
    
    The window displays the image given by the path parameter, and has a button to crop the image.
    
    The user can drag the red rectangle to select the part of the image to crop.
    
    When the user clicks the "Crop" button or closes the window, the function returns the cropped image as a PIL Image object, or None if the window was closed.
    
    Parameters:
        path (str): The path to the image to crop.
    
    Returns:
        PIL.Image or None: The cropped image as a PIL Image object, or None if the window was closed.
    """
    global dragging, delta_x, delta_y, start_point, end_point, prior_rect
    with Image.open(path) as im:
        layout = [
             [sg.Graph((im.size[0], im.size[1]), (0,-im.size[1]), (im.size[0], 0), background_color='white', key='-GRAPH-',enable_events=True,drag_submits=True,pad=0)],
             [sg.Button("Crop", key="-CROP-",pad=0)]
         ]
        window2 = sg.Window("Crop Image",layout,finalize=True,margins=(0,0))
        window2["-GRAPH-"].draw_image(filename=path, location=(0,0))
        window2["-GRAPH-"].draw_rectangle((0,0),(700,-300),line_color="red",line_width=20)
        window2["-GRAPH-"].Widget.config(cursor='fleur')
        window2.refresh()
        graph = window2["-GRAPH-"]
        x0, y0 = 0, 0
        x1, y1 = 700, -300
        dragging = False
        delta_x, delta_y =0, 0
        start_point = end_point = prior_rect = None
        while True:
            event, values = window2.read()
            if event == sg.WIN_CLOSED:
                window2.close()
                return None
            if event == "-GRAPH-":
                x, y = values["-GRAPH-"]
                if not dragging:
                    start_point = (x, y)
                    dragging = True
                    drag_figures = graph.get_figures_at_location((x, y))
                    print(drag_figures)
                    lastxy = x, y
                else:
                    end_point = (x, y)
                    delta_x, delta_y = x - lastxy[0], y - lastxy[1]
                    lastxy = x, y
                    if start_point and end_point:
                        move_figure(drag_figures, delta_x, delta_y,graph,window2,im.size)
            elif event.endswith('+UP'):
                if drag_figures:
                    x0,x1,y0,y1 = update_figure_position(drag_figures, lastxy, start_point,im.size,x0,x1,y0,y1)
                dragging = False
            elif event == "-CROP-":
                window2.close()
                return create_crop_image(lastxy, start_point,path,x0,x1,y0,y1)
def move_figure(drag_figures, delta_x, delta_y,graph,window,size):
    if len(drag_figures) > 1:
        graph.move_figure(drag_figures[1], delta_x, delta_y)
        graph.update()
        widget = window["-GRAPH-"].widget
        x = widget.coords(drag_figures[1])
        # Keep the figure within the graph boundaries
        if x[0] < 0:
            graph.move_figure(drag_figures[1], -x[0], 0)
            graph.update()
        if x[3] > size[1]:
            graph.move_figure(drag_figures[1], 0, -delta_y)
            graph.update()
        if x[2] > size[0]:
            graph.move_figure(drag_figures[1], -delta_x, 0)
            graph.update()
        if x[1] < 0:
            graph.move_figure(drag_figures[1], 0, -delta_y)
            graph.update()
def update_figure_position(drag_figures, lastxy, start_point,size,x0,x1,y0,y1):
    if len(drag_figures) > 1:
        if lastxy[0]< 0:
            x0 = 0
            x1 = 700
        elif lastxy[0]>700:
            x0 = size[0] - 700
            x1 = size[0]
        else:
            x0 += lastxy[0]-start_point[0]
            x1 += lastxy[0]-start_point[0]
        if lastxy[1] < -size[1]:
            y0 = -size[1] + 300
            y1 = -size[1]
        elif lastxy[1] > 0 :
            y0 = 0
            y1 = -300
        else: 
            y0 += lastxy[1]-start_point[1]
            y1 += lastxy[1]-start_point[1]
    return x0,x1,y0,y1
def create_crop_image(lastxy, start_point,path,x0,x1,y0,y1):
    im = crop(path, abs(x0), abs(y0), abs(x1), abs(y1))
    im.save("cropped1.png")
    return "cropped1.png"