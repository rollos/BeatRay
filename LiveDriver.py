from Views import LiveView as LV
from Controllers import LiveController as LC
from Models import LiveModel as LM
from TkGUI.LiveGUI.LiveMainGUI import LiveMainApp
import tkinter as tk


if __name__ == '__main__':


    root = tk.Tk()


    controller = LC.LiveController(root)


    root.mainloop()



