from tkinter import*
import tkinter
from matplotlib import*
from PIL import*
CountBtn = 1
# функция съема значения с ползунка
def scaleget(newVal):
    currentValue['text'] = newVal
def BtnChangeState(text):
    global CountBtn
    if text == '1':
        CountBtn += 1
        if CountBtn % 2 == 0:
            btn1['state'] = 'disabled'
        else:
            btn1['state'] = 'normal'
    if text == '2':
        CountBtn += 1
        if CountBtn % 2 == 0:
            btn['state'] = 'disabled'
        else:
            btn['state'] = 'normal'

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
btn = Button(frame, text='Авт. вентилирование', width=21, height=2, state = None, command=lambda: BtnChangeState('1'))
btn1 = Button(frame, text='Вкл. вентилирование', width=21, height=2, state = None, command=lambda: BtnChangeState('2'))
btn.place(x=1011, y=619)
btn1.place(x=1010, y=662)
# ползунок
scale_tittle = Label(frame, text = 'Нагрев %', width=10, height=1, bg = 'grey80')
scale_tittle.place(x = 1057, y = 348)
scale = Scale(frame, orient='vertical', from_= 100, to=0, width=70, length=220, showvalue=0, sliderlength=20, sliderrelief='raised', command=scaleget)
scale.place(x=1057, y=368)
currentValue = Label(frame, width=6, height=14, bg = 'grey80', highlightbackground = 'black')
currentValue.place(x=1012, y=371)
main.mainloop()