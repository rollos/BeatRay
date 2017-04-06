from TkGUI import MainApp
import SceneModel as m
import SceneController as c
import SceneView as v
import tkinter as tk
from Utils import _create_circle




if __name__ == "__main__":
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()-100
    root.geometry("%dx%d+0+0" % (w, h))

    app = MainApp.MainApplication(root)

    app.pack(expand=tk.YES, fill="both")

  #  app.title("MainGUI")

    tk.Canvas.create_circle = _create_circle




    model = m.SceneModel()
    view = v.SceneView(gui=app)

    app.set_view(view)

    controller = c.SceneController(model, view, root)

