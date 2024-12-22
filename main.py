import PySimpleGUI as sg
import datetime
from PIL import Image, ImageOps
from cropping_functions import *
from window_functions import *
icon = r"D:\habit_tracker\dashed-line-8200898_1280_100x25.png"
def main():
    sg.theme("Light Gray 1")
    global icon
    window = make_window()
    row = 5
    column = 1
    button = 1
    window.finalize()
    check = False
    window.extend_layout(window[("-COLUMN-",column)],[[(sg.pin(sg.Column([[(sg.Button("+",image_filename=icon, key=("-ADD-",button)))]],key=("-COLUMN-", row))))]])
    while True:
        event, value = window.read(timeout=1000)
        if event == sg.WIN_CLOSED:
            break
        print(event[0],event[1])
        if event[0] == "-ADD-":
            text = sg.popup_get_text("Please enter your habit!")
            window[("-COLUMN-",row)].update(visible=False)
            window.refresh()
            window.extend_layout(window[("-COLUMN-",column)],[[(sg.pin(sg.Column([[(sg.Button(text, key=("-HABIT-",button)))]],key=("-COLUMN-", row))))]])
            window.refresh()
            window.refresh()
            button+=1
            row+=1
            column+=1
            if column > 4:
                column = 1
            window.extend_layout(window[("-COLUMN-",column)],[[sg.pin(sg.Column([[(sg.Button("+",image_filename=icon, key=("-ADD-",button)))]],key=("-COLUMN-", row)))]])
            window.refresh()
            print(window[("-ADD-",button)].get_size())
            print(window[("-HABIT-",1)].get_size())
            print(window[("-COLUMN-",6)].get_size())
        if event == "-CHOOSE-":
                while True:
                    x = sg.popup_get_file('Please enter a filename')
                    path = get_image_path(x)
                    if not path==None:
                        break
                window.hide()
                path = crop_image(path)
                window.un_hide()
                window["-IMAGE-"].update(filename=path)
        update_time(window)
        
    window.Close()
if __name__ == "__main__":
    main()