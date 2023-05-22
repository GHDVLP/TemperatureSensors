# необходимые библиотеки

from tkinter import *
import random
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

# начальные значения по умолчанию
ArrX = [0.0]
SensorTemp_RTD_array = [20.0]
SensorTemp_Cuprum_array = [20.0]
SensorTemp_TPL_array = [20.0]
SensorTemp_TPK_array = [20.0]
SensorTemp_RT100_array = [20.0]

start_time = datetime.now(tz=None)
CountBtnClck = 1
CountBtnClck1 = 1
CountBtnClck2 = 1
CountBtnClck3 = 1

# функция съема значения с ползунка
def scaleget(newVal):
    currentValue['text'] = newVal+'%'
# текущее состояние кнопок
def BtnChangeState(text):
    global CountBtnClck
    if text == '1':
        CountBtnClck += 1
        if CountBtnClck % 2 == 0:
            AutoRegulation['bg'] = 'green'
            ManualRegulation['state'] = 'disabled'
        else:
            ManualRegulation['state'] = 'normal'
            AutoRegulation['bg'] = 'grey'
    if text == '2':
        global CountBtnClck1
        CountBtnClck1 += 1
        if CountBtnClck1 % 2 == 0:
            AutoRegulation['state'] = 'disabled'
            ManualRegulation['bg'] = 'green'
        else:
            AutoRegulation['state'] = 'normal'
            ManualRegulation['bg'] = 'grey'
    if text == '3':
        global CountBtnClck2
        CountBtnClck2 += 1
        if CountBtnClck2 % 2 == 0:
            btn['bg'] = 'green'
            create_plot()
            update_plot()
        else:
            btn['bg'] = 'grey'
            destroy_plot()
    if text == '4':
        global CountBtnClck3
        CountBtnClck3 += 1
        if CountBtnClck3 % 2 == 0:
            RedrawBtn['bg'] = 'green'
        else:
            RedrawBtn['bg'] = 'grey'

# создание графика
def create_plot():
    global fig, plot, canvas
    fig = Figure(figsize=(7,4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().place(x=150, y=150)
# обновление графика
def update_plot():
    global ArrX, SensorTemp_RTD_array, SensorTemp_Cuprum_array, SensorTemp_TPL_array, SensorTemp_TPK_array, SensorTemp_RT100_array, CountBtnClck2
    elapsed_time = datetime.now() - start_time
    x = elapsed_time.total_seconds()
    if CountBtnClck % 2 == 1:
        SensorTemp_RTD_array.append(scale.get()*0.01+SensorTemp_RTD_array[-1])
        SensorTemp_Cuprum_array.append(scale.get()*0.02+SensorTemp_Cuprum_array[-1])
        SensorTemp_TPL_array.append(scale.get()*0.03+SensorTemp_TPL_array[-1])
        SensorTemp_TPK_array.append(scale.get()*0.04+SensorTemp_TPK_array[-1])
        SensorTemp_RT100_array.append(scale.get()*0.05+SensorTemp_RT100_array[-1])
    if CountBtnClck % 2 == 0:
        if SensorTemp_RTD_array[-1] <= 0:
            SensorTemp_RTD_array.append(0)
        else:
            SensorTemp_RTD_array.append(SensorTemp_RTD_array[-1] - random.randint(0,1))
        if SensorTemp_Cuprum_array[-1] <= 0:
            SensorTemp_Cuprum_array.append(0)
        else:
            SensorTemp_Cuprum_array.append(SensorTemp_Cuprum_array[-1] - random.randint(1,3))
        if SensorTemp_TPL_array[-1] <= 0:
            SensorTemp_TPL_array.append(0)
        else:
            SensorTemp_TPL_array.append(SensorTemp_TPL_array[-1] - random.randint(1,2))
        if SensorTemp_TPK_array[-1] <= 0:
            SensorTemp_TPK_array.append(0)
        else:
            SensorTemp_TPK_array.append(SensorTemp_TPK_array[-1] - random.randint(1,4))
        if SensorTemp_RT100_array[-1] <= 0:
            SensorTemp_RT100_array.append(0)
        else:
            SensorTemp_RT100_array.append(SensorTemp_RT100_array[-1] - random.randint(1,2))


    ArrX.append(x)
    plot.clear()
    plot.set_xlabel('Время [cек]')
    plot.set_ylabel('Температура [°C]')
    plot.plot(ArrX, SensorTemp_RTD_array, 'o-c',
            ArrX, SensorTemp_Cuprum_array, 'o--b',
            ArrX, SensorTemp_TPL_array, 'o-.r',
            ArrX, SensorTemp_TPK_array, 'o:g',
            ArrX, SensorTemp_RT100_array, 'o:k')
    canvas.draw()
    labelRTD.config(text=str(round(SensorTemp_RTD_array[-1], 2)))
    labelCuprum.config(text=str(round(SensorTemp_Cuprum_array[-1], 2)))
    labelTPL.config(text=str(round(SensorTemp_TPL_array[-1], 2)))
    labelTPK.config(text=str(round(SensorTemp_TPK_array[-1], 2)))
    labelRT100.config(text=str(round(SensorTemp_RT100_array[-1], 2)))
    frame.after(1000, update_plot)
    print(ArrX)
    print(SensorTemp_RTD_array)
    if CountBtnClck2 % 2 == 1:
        return

# сброс графика
def reset_plot():
    global ArrX, SensorTemp_RTD_array, SensorTemp_Cuprum_array, SensorTemp_TPL_array, SensorTemp_TPK_array, SensorTemp_RT100_array, start_time
    start_time = datetime.now()
    ArrX = [0.0]
    SensorTemp_RTD_array = [20.0]
    SensorTemp_Cuprum_array = [20.0]
    SensorTemp_TPL_array = [20.0]
    SensorTemp_TPK_array = [20.0]
    SensorTemp_RT100_array = [20.0]
    plot.clear()
    canvas.draw()

# Скрытие графика
def destroy_plot():
    global ArrX, SensorTemp_RTD_array, SensorTemp_Cuprum_array, SensorTemp_TPL_array, SensorTemp_TPK_array, SensorTemp_RT100_array, start_time
    start_time = datetime.now()
    ArrX = [0.0]
    SensorTemp_RTD_array = [20.0]
    SensorTemp_Cuprum_array = [20.0]
    SensorTemp_TPL_array = [20.0]
    SensorTemp_TPK_array = [20.0]
    SensorTemp_RT100_array = [20.0]
    canvas.get_tk_widget().destroy()

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

# описание кнопок
AutoRegulation = Button(frame, text='Авт. вентилирование', bg = 'grey', width=21, height=2, state = None, command=lambda: BtnChangeState('1'))
ManualRegulation = Button(frame, text='Вкл. вентилирование', bg = 'grey', width=21, height=2, state = None, command=lambda: BtnChangeState('2'))
btn = Button(frame, text='Запуск/стоп', bg = 'grey', width=21, height=2, state = None, command=lambda: BtnChangeState('3'))
RedrawBtn = Button(frame, text='Сбросить значения', bg = 'grey', width=21, height=2, command=reset_plot)
AutoRegulation.place(x=1011, y=619)
ManualRegulation.place(x=1010, y=662)
btn.place(x=50, y=50)
RedrawBtn.place(x = 150, y = 575)

# описание ползунка
scale_tittle = Label(frame, text = 'Нагрев %', width=10, height=1, bg = 'grey80')
scale_tittle.place(x = 1057, y = 348)
scale = Scale(frame, orient='vertical', from_= 100, to=0, width=70, length=220, showvalue=0, sliderlength=20, sliderrelief='raised', command=scaleget)
scale.place(x=1057, y=368)
currentValue = Label(frame, width=9, height=1, bg = 'grey80', highlightbackground = 'black')
currentValue.place(x=1273, y=521)

# лейблы для датчиков

labelRTD = Label(frame, text = "", width = 11, height = 1, bg = 'grey80')
labelCuprum = Label(frame, text = "", width = 15, height = 1, bg = 'grey80')
labelTPL = Label(frame, text = "", width = 13, height = 1, bg = 'grey80')
labelTPK = Label(frame, text = "", width = 13, height = 1, bg = 'grey80')
labelRT100 = Label(frame, text = "", width = 15, height = 1, bg = 'grey80')

labelRTD.place(x=1063, y =304)
labelCuprum.place(x=1055, y=246)
labelTPL.place(x=1241,y=217)
labelTPK.place(x=1305, y=323)
labelRT100.place(x=1178, y=333)



main.mainloop()