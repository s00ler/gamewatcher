import tkinter as tk


win = tk.Tk()
win.title('Hello, Tkinter!')
win.geometry('1000x800')  # Size 200, 200
win.configure(background='red')
label = tk.Label(win, text='ALERT!!', relief=tk.RAISED, justify=tk.CENTER, bg='white', font=("Courier", 160))
label.pack()
win.bell()
win.focus_set()
win.attributes("-topmost", True)
tk.mainloop()
