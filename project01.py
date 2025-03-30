from tkinter import * 
from time import * 
def update(): 
    time_String = strftime("%I:%M:%S: %p")
    time_label.config(text=time_String)

    day_String = strftime("%A")
    day_label.config(text=day_String)

    date_String = strftime("%d %B %Y")  
    date_label.config(text=date_String)

    time_label.after(1000, update)

window = Tk() 

time_label = Label(window, font=("Arial", 50), fg="white", bg="black") 
time_label.pack()

day_label = Label(window, font=("Arial", 20))
day_label.pack()

date_label = Label(window, font=("Arial", 30))
date_label.pack()

update()

window.mainloop()
