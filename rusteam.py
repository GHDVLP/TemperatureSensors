from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import threading
import time

start_time = datetime.now()
CountBtnClckAutoReg = 1
CountBtnClckVentilation = 1
CountBtnClckStart = 1
CountBtnClckPlot = 1

tempR1 = 15
tempR2 = 15
pressure = 0
expenditure = 0
id = None

# функция съема значения с ползунка
def scaleget(newVal):
    currentValue['text'] = f'Задвижка открыта на\n\n {newVal}/100%'

# функция описания начальных значений "датчиков"
def update_value():
    global tempR1, tempR2, pressure, expenditure, id
    tempR1 += 5
    tempR2 += 5
    pressure += 1
    expenditure += 1
    labeltempR1.configure(text=f'Температура радиатора:\n{tempR1}°C')

    if tempR1 >= 70:
        labeltempR1.configure(bg='red')
    else:
        labeltempR1.configure(bg='green4')

    labeltempR2.configure(text=f'Температура радиатора:\n{tempR2}°C')

    if tempR2 >= 75:
        labeltempR2.configure(bg='red')
    else:
        labeltempR2.configure(bg='green4')

    labelpressure.configure(text=f'Давление в ресивере:\n{pressure}МПа')
    labelexpenditure.configure(text=f'Расход воздуха:\n{expenditure} м^3/мин')

    if tempR1 < 80: 
        id = frame.after(1000, update_value)
    else:
        frame.after_cancel(id)

# функция вентилирования
def Tempdown():
    global tempR1, tempR2
    tempR1 -= 5
    tempR2 -= 5
    if tempR1 < 80: 
        id = frame.after(1000, Tempdown)
    else:
        frame.after_cancel(id)
    labeltempR1.configure(text=f'Температура радиатора:\n{tempR1}°C')

    if tempR1 >= 70:
        labeltempR1.configure(bg='red')
    else:
        labeltempR1.configure(bg='green4')

    labeltempR2.configure(text=f'Температура радиатора:\n{tempR2}°C')
    
    if tempR2 >= 75:
        labeltempR2.configure(bg='red')
    else:
        labeltempR2.configure(bg='green4')
    
# текущее состояние кнопок
def BtnChangeState(text):
    global CountBtnClckAutoReg, CountBtnClckVentilation, CountBtnClckStart, CountBtnClckPlot, id

    if text == '1':
        CountBtnClckAutoReg += 1

        if CountBtnClckAutoReg % 2 == 0:
            AutoRegulation['bg'] = 'green'
            ManualRegulation['state'] = 'disabled'
            scale.place_forget()  # Скрыть ползунок
        else:
            ManualRegulation['state'] = 'normal'
            AutoRegulation['bg'] = 'grey'
            scale.place(x=598, y=244)  # Показать ползунок

    if text == '2':
        CountBtnClckVentilation += 1

        if CountBtnClckVentilation % 2 == 0:
            AutoRegulation['state'] = 'disabled'
            ManualRegulation['bg'] = 'green'
            scale.place_forget()  # Скрыть ползунок
            Tempdown()  # Вызов функции для понижения температуры
        else:
            AutoRegulation['state'] = 'normal'
            ManualRegulation['bg'] = 'grey' 
            scale.place(x=598, y=244)  # Показать ползунок

    if text == '3':
        CountBtnClckStart += 1

        if CountBtnClckStart % 2 == 0:
            btn['bg'] = 'green' 
            update_value()
        else:
            frame.after_cancel(id)
            btn['bg'] = 'grey'
            Tempdown()  # Вызов функции для понижения температуры

    if text == '4':
        CountBtnClckPlot += 1

        if CountBtnClckPlot % 2 == 0:
            RedrawBtn['bg'] = 'green'
        else:
            RedrawBtn['bg'] = 'grey'

        if CountBtnClckPlot % 2 != 0:
            tempR1_decreasing = False
            Tempdown()  # Вызов функции для понижения температуры

# создание графика
def create_plot():
    global fig, plot, canvas
    fig = Figure(figsize=(7, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().place(x=0, y=0)

def reset_plot():
    global start_time
    start_time = datetime.now()
    plot.clear()
    canvas.draw()

# Скрытие графика
def destroy_plot():
    global start_time
    start_time = datetime.now()
    canvas.get_tk_widget().destroy()

# главное окно
main = Tk()
main.state('zoomed')
main.title("Диспетчеризация системы автоматического регулирования воздуха")
window_width = 1920
window_height = 1080
main.geometry('%dx%d' % (window_width, window_height))

# контейнер с мнемосхемой
photo = PhotoImage(file='gh.png')
frame = Frame(main, width=1920, height=1080, bg='MistyRose1')
label = Label(frame, image=photo)
label.place(x=0, y=0)
frame.pack()

# описание кнопок
AutoRegulation = Button(frame, text='Авт. режим', bg='grey', width=26, height=4, state=None, command=lambda: BtnChangeState('1'))
ManualRegulation = Button(frame, text='Вкл. вентилирование', bg='grey', width=21, height=2, state=None, command=lambda: BtnChangeState('2'))
btn = Button(frame, text='Запуск/стоп', bg='grey', width=26, height=4, state=None, command=lambda: BtnChangeState('3'))
RedrawBtn = Button(frame, text='Сбросить значения', bg='grey', width=20, height=4, command=reset_plot)
Btnplot = Button(frame, text='График показать/скрыть', bg='grey', width=26, height=4, state=None, command=lambda: BtnChangeState('4'))
AutoRegulation.place(x=172, y=934)
ManualRegulation.place(x=1240, y=524)
btn.place(x=380, y=934)
RedrawBtn.place(x=3, y=934)
Btnplot.place(x=580, y=934)

# описание ползунка
scale = Scale(frame, orient='horizontal', highlightbackground='blue', activebackground='black',

from_=0, to=100, width=20, length=250, showvalue=0, sliderlength=20, sliderrelief='raised', command=scaleget)
scale.place(x=598, y=244)
currentValue = Label(frame, width=36, height=4, bg='grey80', highlightbackground='black', text='Задвижка открыта на\n\n 0/100%')
currentValue.place(x=598, y=271)

# лейблы для датчиков
labeltempR1 = Label(frame, text=f'Температура радиатора:\n{tempR1}°C', bg='green4', width=37, height=4, font=("Arial", 12))
labeltempR2 = Label(frame, text=f'Температура радиатора:\n{tempR2}°C', bg='green4', width=37, height=4, font=("Arial", 12))
labelpressure = Label(frame, text=f'Давление в ресивере:\n{pressure}МПа', bg='green4', width=27, height=4, font=("Arial", 12))
labelexpenditure = Label(frame, text=f'Расход воздуха:\n{expenditure} м^3\мин', bg='green4', width=27, height=4, font=("Arial", 12))

labeltempR1.place(x=1020, y=3)
labeltempR2.place(x=1239, y=598)
labelpressure.place(x=1128, y=348)
labelexpenditure.place(x=1524, y=68)

# функция обработки введенного значения
def handle_input():
    value = entry.get()
    print("Введенное значение:", value)
    entry.delete(0, END)

# создание поля ввода
entry = Entry(frame, width=10, font=("Arial", 12))
entry.place(x=182, y=625)
label_mpa = Label(frame, text="МПа", font=("Arial", 12))
label_mpa.place(x=280, y=625)

# кнопка для обработки введенного значения
input_button = Button(frame, text="Ввести", bg="grey", width=10, height=2, command=handle_input)
input_button.place(x=450, y=600)

main.mainloop()