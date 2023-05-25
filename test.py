from tkinter import*
x = 0.0
def update_x():
    global x
    x += 20
    main.after(500, update_x)
    label.configure(text=f'Температура\n{x}°C')
    if x > 100:
        label['bg'] = 'red'
        return 
 
main = Tk()
label = Label(main, text=f'Температура\n{x}°C', bg = 'green', width= 50, height=50, font=("Arial", 12))
label.pack()
button = Button(main, text='Обновить x', width=10, height=2, command=update_x)
button.pack()
main.mainloop()