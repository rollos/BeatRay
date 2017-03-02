from TkGUI import MainApp
import SceneModel as m
import SceneController as c
import SceneView as v
import tkinter as tk



if __name__ == "__main__":
    root = tk.Tk()

    app = MainApp.MainApplication(root)

    app.pack(expand=tk.YES, fill="both")

  #  app.title("MainGUI")





    model = m.SceneModel()
    view = v.SceneView(gui=app)

    app.set_view(view)

    controller = c.SceneController(model, view)

    root.mainloop()
