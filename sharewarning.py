from tkinter import Tk, CENTER, Label

TITLE = 'Control Docente'
MESSAGE = "Comenzo el control de su clase\nSi no desea que el control interrumpa la vista de los estudiantes\nSe recomienda compartir una sola aplicacion y no toda su pantalla."
DURATION = 20000

class WarningAlert(Tk):

    def __init__(self):

        super().__init__()

        width = 570
        height = 100
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.title(TITLE)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.iconbitmap("umss.ico")
        self.resizable(0, 0)
        self.wm_attributes("-topmost", True)
        self.after(DURATION, self.destroy)
        message_label = Label(self, text=MESSAGE, justify=CENTER, font = "Helvetica 14")
        message_label.pack()

testUI = WarningAlert()
testUI.mainloop()
