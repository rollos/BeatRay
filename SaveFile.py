import tkinter as tk
import tkinter.filedialog

class TkFileDialog(tk.Frame):

    def __init__(self, root):

        tk.Frame.__init__(self, root)

        self.file_opt = options = {}
        options['filetypes'] = [('all files', '*'), ('text files', '*.txt')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root

    def asksaveasfilename(self):
        filename = tk.filedialog.asksaveasfilename(**self.file_opt)

        if filename:
            return filename + ".txt"

    def askloadasfilename(self):
        filename = tk.filedialog.askopenfilename(**self.file_opt)

        if filename:
            return filename

if __name__=='__main__':
    root = tk.Tk()
    TkFileDialog(root).pack()
    root.mainloop()