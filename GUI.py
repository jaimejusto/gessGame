from tkinter import *

# window
window = Tk()

# window title
window.title("Gess Board Game")

# window dimensions
window.configure(width=800, height=450)

# window background color
window.configure(bg="tan4")

# center the window
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
positionLeft = int(window.winfo_screenheight() / 2 - windowHeight / 2)
window.geometry("+{}+{}".format(positionRight, positionLeft))

window.mainloop()
