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

fig_window = None

global pressure
tempR1 = 15
tempR2 = 17
pressure = 0
expenditure = 0
id = None
updateid = None

# функция съема значения с ползунка
def scaleget(newVal):
    global expenditure
    newVal = float(newVal)  # Преобразование строки в число
    currentValue['text'] = f'Задвижка открыта на\n\n {newVal}/100%'

    expenditure = newVal * 20 / 100  # Пропорциональное значение expenditure от 0 до 60
    # Обновление метки с расходом воздуха
    labelexpenditure.config(text=f'Расход воздуха:\n{expenditure} м^3/мин')

# функция описания начальных значений "датчиков"
def update_value():
    global tempR1, tempR2, id, updateid
    tempR1 += 5
    tempR2 += 5

    labeltempR1.configure(text=f'Температура радиатора:\n{tempR1}°C')

    if tempR1 >= 80:
        labeltempR1.configure(bg='red')
    else:
        labeltempR1.configure(bg='green4')

    labeltempR2.configure(text=f'Температура радиатора:\n{tempR2}°C')

    if tempR2 >= 80:
        labeltempR2.configure(bg='red')
    else:
        labeltempR2.configure(bg='green4')
    updateid = frame.after(1000, update_value)
    if tempR1 and tempR2 > 100:
        frame.after_cancel(updateid)

    
# функция вентилирования
def Tempdown():
    global tempR1, tempR2, id

    if CountBtnClckVentilation % 2 == 0:
        tempR1 -= 8
        tempR2 -= 8
        tempR1 = max(tempR1, 15)
        tempR2 = max(tempR2, 17)  
        #frame.after_cancel(id)  # Исправлено: Отменить вызов функции после достижения целевого значения

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
    id = frame.after(1000, Tempdown)

# текущее состояние кнопок
def BtnChangeState(text):
    global CountBtnClckAutoReg, CountBtnClckVentilation, CountBtnClckStart, CountBtnClckPlot, id

    if text == '1':
        CountBtnClckAutoReg += 1

        if CountBtnClckAutoReg % 2 == 0:
            AutoRegulation['bg'] = 'green'
            ManualRegulation['state'] = 'disabled'
            update_value()
            if tempR1 or tempR2 > 75:
                frame.after_cancel(updateid)
                updateid = None
                Tempdown()
            if tempR1 and tempR2 < 20:
                frame.after_cancel(id)
                id = None
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
            threadminus = threading.Thread(target=Tempdown)
            threadminus.start()
            frame.after_cancel(updateid)
            updateid = None
            if tempR2 or tempR1 <= 20:
                frame.after_cancel(id)
                id = None
        else:
            AutoRegulation['state'] = 'normal'
            ManualRegulation['bg'] = 'grey'
        

    if text == '3':
        CountBtnClckStart += 1

        if CountBtnClckStart % 2 == 0:
            btn['bg'] = 'green'
            threadplus = threading.Thread(target=update_value)
            threadplus.start()
            if (tempR1 or tempR2) >= 80:
                frame.after_cancel(updateid)
                updateid = None
        else:
            btn['bg'] = 'grey'

    if text == '4':
        CountBtnClckPlot += 1
        if CountBtnClckPlot == 2:
            create_chart_window()
        

ArrX = []
ArrYR1 = []
ArrYR2 = []

start_time = datetime.now()

def create_chart_window():
    main.chart_window = Toplevel()
    main.chart_window.title("График")
    main.chart_window.geometry("600x400+{}+{}".format(main.winfo_screenwidth() // 2 - 100, main.winfo_screenheight() // 2 - 400))
 
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
 
    canvas = FigureCanvasTkAgg(fig, master=main.chart_window)
    canvas.get_tk_widget().pack()
 
    def update_chart():
        global tempR1, tempR2

        elapsed_time = datetime.now() - start_time
        x = elapsed_time.total_seconds()
        y = scale.get()
        ArrX.append(x)
        ArrYR1.append(tempR1)
        ArrYR2.append(tempR2)
        ax.clear()
        ax.plot(ArrX, ArrYR1, label = "Темп. датчик радиатора 1", color='g')
        ax.plot(ArrX, ArrYR2, label = "Темп. датчик радиатора 2", color ='red')
        ax.legend()
        canvas.draw()
        main.chart_window.after(1000, update_chart)
        
    update_chart()
 

# Обновление шкалы прогресса
def update_progress():
    global pressure
    
    for i in range(15):
        if i < pressure // 100:
            cells[i].configure(bg="red")
        else:
            cells[i].configure(bg="red4")
    frame.after(1000, update_progress)  

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

# создания фрейма для шкалы заполнения
frame_bar = Frame(frame)
frame_bar.place(x=824, y=402)

global cells
cells = []
for i in range(15):
    cell = Label(frame_bar, width=37, height=1, bg="red4",highlightthickness=1, highlightbackground="black")
    cell.pack(side="bottom", pady=1, )
    cells.append(cell)

# описание кнопок
AutoRegulation = Button(frame, text='Авт. режим', bg='grey', width=26, height=4, state=None, command=lambda: BtnChangeState('1'))
ManualRegulation = Button(frame, text='Вкл. вентилирование', bg='grey', width=21, height=2, state=None, command=lambda: BtnChangeState('2'))
btn = Button(frame, text='Запуск/стоп', bg='grey', width=26, height=4, state=None, command=lambda: BtnChangeState('3'))
RedrawBtn = Button(frame, text='Сбросить значения', bg='grey', width=20, height=4)
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

    global pressure
    update_progress()
    target_pressure = int(entry.get())
    entry.delete(0, END)

    pressure = 0  

    def increase_pressure():
        global pressure  

        if pressure < target_pressure:
            pressure += 1
            labelpressure.config(text=f'Давление в ресивере:\n{pressure} Па')
            frame.after(20, increase_pressure)
        else:
            labelpressure.config(text=f'Давление в ресивере:\n{pressure} Па')  # Обновляем метку после достижения целевого значения

    increase_pressure()

# создание поля ввода
entry = Entry(frame, width=20, font=("Arial", 12))
entry.place(x=185, y=634)

# создание кнопки для отправки введенного значения
send_btn = Button(frame, text="Отправить", width=10, height=1, command=handle_input)
send_btn.place(x=300, y=632)

# запуск главного цикла
main.mainloop()