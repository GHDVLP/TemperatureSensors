from tkinter import*
from PIL import*
class Cnopka(Button):
    def __init__(self, master, text, width, height, bg = 'grey', **kw):
        super().__init__(master = master, text = text, width = width, height = height, bg = bg, **kw)
# главное окно
main = Tk()
main.state('zoomed')
main.title("SCADA система температурных датчиков")
window_width = 800
window_height = 600
main.geometry('%dx%d' % (window_width, window_height))
# контейнер с мнемосхемой
photo = PhotoImage(file='1.png')
frame = Frame(main, width=1920, height=1080, bg='MistyRose1')
label = Label(frame, image=photo)
label.place(x=0, y=0)
frame.pack()
# кнопки
btn = Cnopka(frame, 'Авт. вентилирование', 21, 2)
btn1 = Cnopka(frame, 'Вкл. вентилирование', 21, 2)
btn.place(x=1011, y=619)
btn1.place(x=1010, y=662)
# ползунок
scale = Scale(frame, bg='grey', activebackground='white', highlightbackground='MistyRose1', from_= 100, to=0, width=50, length=220)
scale.place(x=1057, y=368)

main.mainloop()