import tkinter as tk

class LiveMainApp(tk.Frame):

    def __init__(self, parent, view):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        self.view = view


    def message_view(self, message, value):
        self.view.notify_observers(message, value)






class SceneSelectorPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent


        self.buttons = self.make_buttons


    def message_view(self, message, value):
        self.parent.message_view(message, value)


