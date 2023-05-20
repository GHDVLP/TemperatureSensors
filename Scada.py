from tkinter import*
from matplotlib import*
from PIL import*
class Cnopka(Button):
    def __init__(self, master, text, width, height, bg = 'grey', **kw):
        super().__init__(master = master, text = text, width = width, height = height, bg = bg, **kw)

# функция съема значения с ползунка
def scaleget(newVal):
    label['text'] = float(newVal)

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
scale = Scale(frame, orient='vertical', from_= 100, to=0, width=53, length=240, showvalue=0, sliderlength=10, sliderrelief='raised', tickinterval = 25, command=scaleget)
scale.place(x=1057, y=368)
label = Label(frame, width=11, height=1)
label.place(x=1057, y=348)

main.mainloop()