import time
from random import *
import threading
from threading import Thread
import tkinter as tk
from tkinter import BOTH, W, NW, SUNKEN, TOP, X, FLAT, LEFT, SW, SE
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ArrX = []
ArrY1 = []
ArrY2 = []
start_time = datetime.now()

global temp1
global temp2
temp1 = 0
temp2 = 0

global progress_percent_fire
global progress_percent_smoke
progress_percent_fire = 0
progress_percent_smoke = 0

global StartKey
global HandKey
StartKey = 0
HandKey = 0


window = tk.Tk()
window.title('SCADA')
window.geometry('650x450+700+200')

window.resizable(False, False)
window.config(bg="grey50")

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)



frame_bars = tk.Frame(window, bg="grey50", highlightthickness=10, highlightbackground="grey50")

frame_fire_bar = tk.Frame(frame_bars, bg="grey50", highlightthickness=10, highlightbackground="grey50")

frame_smoke_bar = tk.Frame(frame_bars, bg="grey50", highlightthickness=10, highlightbackground="grey50")

frame_buttons = tk.Frame(window, bg="grey50")

frame_datas = tk.Frame(window, bg="grey80")

frame_handmod = tk.Frame(window, bg="grey80")

frame_handmod_side1 = tk.Frame(frame_handmod, bg="grey80")

frame_handmod_side2 = tk.Frame(frame_handmod, bg="grey80")

temp1str = tk.StringVar()
temp1str.set(f"Температурный датчик 1: {temp1}°С")

temp2str = tk.StringVar()
temp2str.set(f"Температурный датчик 2: {temp2}°С")


def create_chart_window():
	window.chart_window = tk.Toplevel()
	window.chart_window.title("График")
	window.chart_window.geometry("600x400+{}+{}".format(window.winfo_screenwidth() // 2 - 100, window.winfo_screenheight() // 2 - 400))
 
	fig = plt.Figure(figsize=(5, 4), dpi=100)
	ax = fig.add_subplot(111)
	
 
	canvas = FigureCanvasTkAgg(fig, master=window.chart_window)
	canvas.get_tk_widget().pack()
	
	

	def update_chart():
		global temp1
		global progress_percent_fire

		elapsed_time = datetime.now() - start_time
		x = elapsed_time.total_seconds()
		y = progress_percent_fire, temp1
		ArrX.append(x)
		ArrY1.append(temp1)
		ArrY2.append(progress_percent_fire)
		ax.clear()
		ax.plot(ArrX, ArrY1, label = "Темп. датчик 1", color='g')
		ax.plot(ArrX, ArrY2, color='r', label = "Мощность горелки")
		ax.legend()
		canvas.draw()
		
		window.chart_window.after(1000, update_chart)
 
	update_chart()


def hand_update():
	global progress_percent_fire
	global progress_percent_smoke

	progress_percent_fire = SettingFire.get()
	progress_percent_smoke = SettingSmoke.get()

	update_progress()


# Обновление шкалы прогресса
def update_progress():

	global progress_percent_fire
	global progress_percent_smoke
	
	for i in range(10):
		if i < progress_percent_fire // 10:
			cells[i].configure(bg="green")
		else:
			cells[i].configure(bg="red")

	for i in range(10):
		if i < progress_percent_smoke // 10:
			cells1[i].configure(bg="green")
		else:
			cells1[i].configure(bg="red")

def StartClicked():
	global StartKey
	global HandKey
	if StartKey == 0:
		startbutton.configure(bg='green')
		StartKey = 1
		run_function_in_thread(startagregat)

	else:
		startbutton.configure(bg='red')
		autobutton.configure(bg='red')
		StartKey = 0
		HandKey = 0
		run_function_in_thread(stopagregat)
		hideframe(frame_handmod)

def toggle_frame(frame):
	if frame.winfo_ismapped():
		frame.pack_forget()  # Скрыть фрейм
	else:
		frame.pack()

	if isinstance(frame, tk.Frame):
		for child in frame.winfo_children():
			toggle_frame(child)	

def HandClicked():
	global StartKey
	global HandKey

	if StartKey == 1 and HandKey == 0:
		autobutton.configure(bg='green')
		HandKey = 1
		showhandframe()
	elif StartKey == 1:
		
		autobutton.configure(bg='red')
		HandKey = 0
		hideframe(frame_handmod)
	else:
		tk.messagebox.showerror(title="Ошибка", message="Ручной режим недоступен пока система отключена",)

def set_widgets_color(frame, color):
	# Получить все виджеты внутри фрейма
	frame.configure(bg=color)
	widgets = frame.winfo_children()
	
	if isinstance(frame, tk.Frame):
		for child in frame.winfo_children():
			set_widgets_color(child, color)
	for widget in widgets:
		widget.configure(bg=color)
	
def hideframe(frame):
	frame.configure(bg='grey50')
	if isinstance(frame, tk.Frame):
		for child in frame.winfo_children():
			hideframe(child)	
	frame.pack_forget()

def showframe(frame):
	if isinstance(frame, tk.Frame):
		for child in frame.winfo_children():
			showframe(child)	
	frame.grid()

def showhandframe():

	DataText.pack(side='top', anchor='nw')
	SettingFireText.pack(side=tk.LEFT, anchor='w')
	SettingFire.pack()
	SettingSmokeText.pack(side=tk.LEFT, anchor='w')
	SettingSmoke.pack()
	SettingButton.pack(anchor='se', side='bottom')
	frame_handmod_side1.pack()
	frame_handmod_side2.pack()
	set_widgets_color(frame_handmod, 'grey80')

def startagregat():

	global temp1
	global StartKey
	global progress_percent_fire

	while temp1 < 100 and StartKey == 1:
		progress_percent_fire = progress_percent_fire + randint(0, 15)
		temp1 = temp1 + progress_percent_fire
		temp1str.set(f"Температурный датчик 1: {temp1}°С")
		update_progress()
		time.sleep(1)

	while StartKey == 1:
		continueagregat()
		time.sleep(1)

def continueagregat():

	global progress_percent_fire, temp1
	

	progress_percent_fire = progress_percent_fire + randint(0, 10)
	progress_percent_fire = progress_percent_fire - randint(0, 10)
	update_progress()
	if progress_percent_fire < 10:
		progress_percent_fire = 11
	if progress_percent_fire > 50:
		progress_percent_fire = 51
	temp1 = randint(95, 110)
	temp1str.set(f"Температурный датчик 1: {temp1}°С")

def stopagregat():

	global temp1

	while temp1 > 0 and StartKey == 0:
		global progress_percent_fire
		global progress_percent_smoke

		progress_percent_smoke = 0
		progress_percent_fire = 0
		update_progress()
		time.sleep(1)
		temp1 = temp1 - randint(1, 10)
		temp1str.set(f"Температурный датчик 1: {temp1}°С")
		
	temp1 = 0
	temp1str.set(f"Температурный датчик 1: {temp1}°С")

def run_function_in_thread(function, *args, **kwargs):
	thread = threading.Thread(target=function, args=args, kwargs=kwargs)
	thread.start()


# Создание кнопок старта и ручника

startbutton = tk.Button(frame_buttons,text="START/STOP",bg="red", font="ARIAL50", padx=10, pady=5, height=3, width=10, command = StartClicked)
startbutton.pack(pady=0, anchor='w')

autobutton = tk.Button(frame_buttons, text="Ручной режим", bg='red', font="ARIAL50", pady=5, height=2, width=12, command = HandClicked)
autobutton.pack(pady=10, anchor='w')

grafbutton = tk.Button(frame_buttons, text="Построить график", bg='red', font="ARIAL50", pady=5, height=2, width=15, command = create_chart_window)
grafbutton.pack(pady=0)



# Создание текстовых полей датчиков

datatemp1 = tk.Label(frame_datas, font="ARIAL50", textvariable=temp1str, bg="grey80")
datatemp1.pack(pady=10)


datatemp2 = tk.Label(frame_datas, textvariable=temp2str, font="ARIAL50", bg="grey80")
datatemp2.pack(side=LEFT, pady=10)


# Создание 10 ячеек для полоски прогресса дыма

smoke_text=tk.Label(frame_smoke_bar,text="Мощность дымососа",font="ARIAL",	bg="grey50")
smoke_text.pack(side="bottom", pady=1,)

global cells1
cells1 = []
for i in range(10):
	cell1 = tk.Label(frame_smoke_bar, width=4, height=2, bg="red", highlightthickness=1, highlightbackground="black")
	cell1.pack(side="left", pady=1, )
	cells1.append(cell1)



# Создание 10 ячеек для полоски прогресса огня

fire_text=tk.Label(frame_fire_bar,text="Мощность горелки",font="ARIAL",	bg="grey50")
fire_text.pack(side="bottom", pady=1, )

global cells
cells = []
for i in range(10):
	cell = tk.Label(frame_fire_bar, width=4, height=2, bg="red",highlightthickness=1, highlightbackground="black")
	cell.pack(side="left", pady=1, )
	cells.append(cell)


# Поля для ручного управления

DataText = tk.Label(frame_handmod, text='Задайте значения', font='arial50',)
DataText.pack(side='top', anchor='nw')

SettingFireText = tk.Label(frame_handmod_side1, text='Мощность горелки',font="ARIAL50")
SettingSmokeText = tk.Label(frame_handmod_side2, text='Мощность дымососа',font="ARIAL50")

SettingFire = tk.Scale(frame_handmod_side1,from_=0, to=100, orient=tk.HORIZONTAL,highlightbackground="grey80")
SettingFireText.pack(side=tk.LEFT, anchor='w')
SettingFire.pack()

SettingSmoke = tk.Scale(frame_handmod_side2,from_=0, to=100, orient=tk.HORIZONTAL,highlightbackground="grey80")
SettingSmokeText.pack(side=tk.LEFT, anchor='w')
SettingSmoke.pack()

SettingButton = tk.Button(frame_handmod, text='Применить', font='arial50', command=hand_update)
SettingButton.pack(anchor='se', side='bottom')
	
set_widgets_color(frame_handmod, 'grey80')

frame_smoke_bar.pack()
frame_fire_bar.pack()
frame_buttons.grid(row=1, column=1, sticky=tk.NW, padx=20, pady=20)
frame_bars.grid(row=1, column=2, sticky=tk.SE)
frame_datas.grid(sticky=tk.SW, row=1, column=1)
frame_handmod.grid(row=1, column=2, sticky=tk.NE)
frame_handmod_side1.pack()
frame_handmod_side2.pack()

hideframe(frame_handmod)

window.mainloop()