# необходимые библиотеки

from tkinter import *
import random
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

ArrX = [0] # время на графике
SensorTemp_RTD_array = [20] # массив значений температуры RTD
SensorTemp_Cuprum_array = [20] # массив значений температуры Cuprum
SensorTemp_TPL_array = [20] # массив значений температуры TPL
SensorTemp_TPK_array = [20] # массив значений температуры TPK
SensorTemp_RT100_array = [20] # массив значений температуры RT100
start_time = datetime.now()

CountBtnClck = 1
CountBtnClck1 = 1
CountBtnClck2 = 1
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
            create_chart_widget()
        else:
            destroy_chart_widget()

def create_chart_widget():
    global fig
    global ax
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().place(x=500, y=100)

    def update_chart():
        global x, SensorTemp_RTD, SensorTemp_Cuprum, SensorTemp_TPL, SensorTemp_TPK, SensorTemp_RT100 # значения температуры текущие
        elapsed_time = datetime.now() - start_time
        x = elapsed_time.total_seconds()
        if CountBtnClck % 2 == 1:
            SensorTemp_RTD = x*scale.get()*0.01+SensorTemp_RTD_array[-1]
            SensorTemp_Cuprum = x*scale.get()*0.02+SensorTemp_Cuprum_array[-1]
            SensorTemp_TPL = x*scale.get()*0.03+SensorTemp_TPL_array[-1]
            SensorTemp_TPK = x*scale.get()*0.04+SensorTemp_TPK_array[-1]
            SensorTemp_RT100 = x*scale.get()*0.05+SensorTemp_RT100_array[-1]

            SensorTemp_RTD_array.append(SensorTemp_RTD)
            SensorTemp_Cuprum_array.append(SensorTemp_Cuprum)
            SensorTemp_TPL_array.append(SensorTemp_TPL)
            SensorTemp_TPK_array.append(SensorTemp_TPK)
            SensorTemp_RT100_array.append(SensorTemp_RT100)
        if CountBtnClck % 2 == 0:
            SensorTemp_RTD -= random.randint(0,1)
            SensorTemp_Cuprum -= random.randint(1,3)
            SensorTemp_TPL -= random.randint(1,2)
            SensorTemp_TPK -= random.randint(1,4)
            SensorTemp_RT100 -= random.randint(1,2)

            SensorTemp_RTD_array.append(SensorTemp_RTD)
            SensorTemp_Cuprum_array.append(SensorTemp_Cuprum)
            SensorTemp_TPL_array.append(SensorTemp_TPL)
            SensorTemp_TPK_array.append(SensorTemp_TPK)
            SensorTemp_RT100_array.append(SensorTemp_RT100)
        ArrX.append(x)
        ax.clear()
        ax.set_xlabel('Время [cек]')
        ax.set_ylabel('Температура [°C]')
        ax.plot(ArrX, SensorTemp_RTD_array, 'o-c',
                ArrX, SensorTemp_Cuprum_array, 'o--b',
                ArrX, SensorTemp_TPL_array, 'o-.r',
                ArrX, SensorTemp_TPK_array, 'o:g',
                ArrX, SensorTemp_RT100_array, 'o:k')
        canvas.draw_idle()

        frame.after(1000, update_chart)
    update_chart()

def destroy_chart_widget():
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
btn = Button(frame, text='График', bg = 'grey', width=21, height=2, state = None, command=lambda: BtnChangeState('3'))
AutoRegulation.place(x=1011, y=619)
ManualRegulation.place(x=1010, y=662)
btn.place(x=50, y=50)

# описание ползунка
scale_tittle = Label(frame, text = 'Нагрев %', width=10, height=1, bg = 'grey80')
scale_tittle.place(x = 1057, y = 348)
scale = Scale(frame, orient='vertical', from_= 100, to=0, width=70, length=220, showvalue=0, sliderlength=20, sliderrelief='raised', command=scaleget)
scale.place(x=1057, y=368)
currentValue = Label(frame, width=9, height=1, bg = 'grey80', highlightbackground = 'black')
currentValue.place(x=1273, y=521)

main.mainloop()