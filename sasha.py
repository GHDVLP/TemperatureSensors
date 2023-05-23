from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
ArrX = []
ArrY = []
start_time = datetime.now()
value_temp_sush=52
value_temp_pech=600
value_mokr_zern=100
value_topl=20
value_otkr_klap=30
value_syh_zern=40
CountBtn = 1
CountBtn1 = 1
CountBtn2 = 1
#Принятие значения с уставки температуры
def change(newVal):
    label["text"] = scale.get()
#Реализация режимо кнопки    
def change_button(text):
    global CountBtn
    if text == "1":
        global CountBtn
        CountBtn += 1
        if CountBtn % 2 == 0:
            btn1["text"] = "Вкл"
            btn1["bg"] = "green"
            btn2['state'] = 'normal'
        else:
            btn1["text"] = "Выкл"
            btn1["bg"] = "red"
            btn2['state'] = 'disabled'
    if text == "2":
        global CountBtn1
        CountBtn1 += 1
        if CountBtn1 % 2 == 0:
            btn2["text"] = "Руч"
            btn2["bg"] = "white"
            scale.place(x=1057, y=368)
            label.place(x=1112, y=466)
 
        else:
            btn2["text"] = "Авт"
            btn2["bg"] = "white"
            scale.place_forget()
            label.place_forget()
    if text == "3":
        global CountBtn2
        CountBtn2 += 1
        if CountBtn2 % 2 == 0:
            btn3["text"] = "Температурный\n график"
            btn3["bg"] = "green"
            create_chart_window()   
        else:
            btn3["text"] = "Температурный\n график"
            btn3["bg"] = "grey"
            destroy_chart_window()  
 
def create_chart_window():
    main.chart_window = Toplevel()
    main.chart_window.title("График")
    main.chart_window.geometry("600x400+{}+{}".format(main.winfo_screenwidth() // 2 - 100, main.winfo_screenheight() // 2 - 150))
 
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
 
    canvas = FigureCanvasTkAgg(fig, master=main.chart_window)
    canvas.get_tk_widget().pack()
 
    def update_chart():
        elapsed_time = datetime.now() - start_time
        x = elapsed_time.total_seconds()
        y = scale.get()
        ArrX.append(x)
        ArrY.append(y)
 
        ax.clear()
        ax.plot(ArrX, ArrY, marker='o', color='b')
 
        canvas.draw()
 
        main.chart_window.after(5000, update_chart)
 
    update_chart()
 
def destroy_chart_window():
    if hasattr(main, "chart_window"):
        main.chart_window.destroy()               
#Фон Scada 
main = Tk()
main.state('zoomed')
main.title("SCADA САР автоматического управления шахтной зерносушилки")
window_width = 1920
window_height = 1080
main.geometry('%dx%d' % (window_width, window_height))
 
photo = PhotoImage(file='gh.png')
 
frame = Frame(main, width=1920, height=1080, bg='MistyRose1')
label = Label(frame, image=photo)
label.pack(fill=BOTH)
frame.pack()
#Задана первая кнопка Вкл/Выкл
btn1 = Button(main, text="Выкл", bg="red", width=12, height=2, font=("Arial", 12), command = lambda: change_button('1'))
btn1.place(x=259, y=70)
#Задана вторая кнопка Авт/Руч
btn2 = Button(main, text="Авт", bg="azure2", width=12, height=2, state = 'disabled', font=("Arial", 12), command = lambda: change_button('2'))
btn2.place(x=428, y=70)
#Задана третья кнопка которая вызывает новый экран
btn3 = Button(main, text="Температурный\n график", bg="grey", width=12, height=2, font=("Arial", 12), command = lambda: change_button('3'))
btn3.place(x=800, y=500)
#Ползунок на уставку температуры
scale = Scale(frame, bg='grey', activebackground='white', highlightbackground='grey', from_= 100, to=0, width=50, length=220, showvalue=0, label="         ", command=change)
#Записываем значение с уставки температуры
label = Label(frame, width=5, height=2, bg="grey50")
#Метка с надписью "Температура в сушке:"
label1 = Label(frame, width=20, height=2, bg="grey61",text="Температура в сушке:",font=("Arial", 12),anchor="nw")
label1.place(x=1112, y=120)
#Метка с надписью "Температура в печи:" 
label2 = Label(frame, width=20, height=2, bg="grey61",text="Температура в печи:",font=("Arial", 12),anchor="nw")
label2.place(x=1112, y=160)
#Метка со значением которая имеет "Температура в сушке:"
label3 = Label(frame, width=5, height=2, bg="grey61",text=value_temp_sush,font=("Arial", 12),anchor="nw")
label3.place(x=1280, y=120)
#Метка со значением которая имеет "Температура в печи:" 
label4 = Label(frame, width=5, height=2, bg="grey61",text=value_temp_pech,font=("Arial", 12),anchor="nw")
label4.place(x=1280, y=160)
#Метка с надписью "Количесто зерна:" 
label5 = Label(frame, width=21, height=10, bg="grey61",text="Количество зерна:",font=("Arial", 12))
label5.place(x=126, y=410)
#Метка со значением которая имеет "Количесто зерна:"
label6 = Label(frame, width=5, height=2, bg="grey61",text=f"{value_mokr_zern}%",font=("Arial", 12))
label6.place(x=195, y=520)
#Метка с надписью "Количесто топлива:" 
label7 = Label(frame, width=9, height=5, bg="grey61",text="Количество\n топлива:",font=("Arial", 12))
label7.place(x=59, y=730)
#Метка со значением которая имеет "Количесто топлива:"
label8 = Label(frame, width=5, height=2, bg="grey61",text=f"{value_topl}%",font=("Arial", 12))
label8.place(x=77, y=795)
#Метка с надписью "Количесто топлива:" 
label9 = Label(frame, width=13, height=2, bg="grey75",text="Открытие\n клапана:",font=("Arial", 12))
label9.place(x=305, y=730)
#Метка со значением которая имеет "Количесто топлива:"
label10 = Label(frame, width=5, height=1, bg="grey75",text=f"{value_otkr_klap}%",font=("Arial", 12))
label10.place(x=340, y=775)
#Метка с надписью "Количесто высушенного зерна:" 
label9 = Label(frame, width=30, height=7, bg="grey61",text="Количество зерна:",font=("Arial", 12))
label9.place(x=1248, y=517)
#Метка со значением которая имеет "Количесто высушенного зерна:"
label10 = Label(frame, width=5, height=1, bg="grey61",text=f"{value_syh_zern}%",font=("Arial", 12))
label10.place(x=1360, y=600) 
main.mainloop()