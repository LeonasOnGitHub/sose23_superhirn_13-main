import tkinter as tk

root = tk.Tk()
root.title("MasterMind")
root.geometry("500x500")
root.resizable(height=False, width=False)

label1 = tk.Label(root, text="Hello World!", bg="green")
label1.pack()

root.mainloop()
