import tkinter as tk
#from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import time, serial, csv
from datetime import datetime
from threading import Thread

start = time.time()
s = serial.Serial("COM10")
s.baudrate = 9600
s.setRTS(0)

f = open('Test.csv','w', encoding='UTF8', newline='')
writer = csv.writer(f)
row = 0

xar = []
yar1 = []
yar2 = []
yar3 = []
yar4 = []
yar5 = []
yar6 = []
yar7 = []
yar8 = []
yar9 = []
yar10 = []
    
    
def listadd(text):
    listNodes.insert(END, " "+str(round(time.time()-start,4))+" "+str(text))
    listNodes.yview(END)

def animate(i):
    a=1
    
def serialListen():
    while True:     
        data = s.readline()    
        #Data Cleanup
        data = data.decode('utf-8')
        list1 = str(data).split(",")
        
        #Variable Creation 
        ID = list1[0]
        BV = list1[1]
        BV2 = list1[2]
        ALTN = list1[3]
        ALT = list1[4]
        PA = list1[5]
        TMP = list1[6]
        CO2 = list1[7]
        X = list1[8]
        Y = list1[9]
        Z = list1[10]
        TMP2 = list1[11]
        
        list1.append(float(time.time()-start))
        now = datetime.now()
        tm = now.strftime("%H:%M:%S")      
        printdata = str(tm+" "+ID+" "+BV+" "+BV2+" "+ALTN+" "+ALT+" "+PA+" "+TMP+" "+CO2+" "+X+" "+Y+" "+Z+" "+TMP2)
        
        if ID == "table":
          #wks.update('A'+str(row+1)+':''G'+str(row+1), [[rotation,acceleration,compass,noise,light,pressure1,alt]]) 
          print(printdata)
          writer.writerow(list1)
          listadd("---> Data Recieved")
          xar.append(round(time.time()-start,4))
          yar1.append(float(ALT))
          yar2.append(float(ALTN))
          yar3.append(float(PA))
          yar4.append(float(CO2))
          yar5.append(float(TMP))
          yar6.append(float(TMP2))
          yar7.append(float(BV))
          yar8.append(float(BV2))
          
          ax1.clear()
          ax1.plot(xar,yar1)
          ax2.clear()
          ax2.plot(xar,yar2)
          ax3.clear()
          ax3.plot(xar,yar3)
          ax4.clear()
          ax4.plot(xar,yar4)
          ax5.clear()
          ax5.plot(xar,yar5)
          ax6.clear()
          ax6.plot(xar,yar6)
          ax7.clear()
          ax7.plot(xar,yar7)
          ax8.clear()
          ax8.plot(xar,yar8)
          

window = tk.Tk()
#window.geometry("1920x1060")
window.state('zoomed')
window.title("Simple Text Editor")
window.configure(bg='white')
frame1 = tk.Frame(master=window, height=60, bg="#4cd3f5")
frame1.pack(fill=tk.X)


tabControl = ttk.Notebook(window, width=1180, height=530) 
tab1 = ttk.Frame(tabControl, width=10, height=45)
tab2 = ttk.Frame(tabControl, width=10, height=45)
tab3 = ttk.Frame(tabControl, width=10, height=45)
tab4 = ttk.Frame(tabControl, width=10, height=45)
tab5 = ttk.Frame(tabControl, width=10, height=45)
tab6 = ttk.Frame(tabControl, width=10, height=45)
tab7 = ttk.Frame(tabControl, width=10, height=45)
tab8 = ttk.Frame(tabControl, width=10, height=45)
  
tabControl.add(tab1, text =' Altitude ')
tabControl.add(tab2, text =' Altitude normalised ')
tabControl.add(tab3, text =' Pressure ')
tabControl.add(tab4, text =' CO2 ')
tabControl.add(tab5, text =' Temp1 ')
tabControl.add(tab6, text =' Temp2 ')
tabControl.add(tab7, text =' Battery ')
tabControl.add(tab8, text =' Battery %')

#Pages

fig = plt.figure(figsize=(6,5), dpi=100)
fig.set_figwidth(14)
fig.set_figheight(5.3)
ax1 = fig.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig, tab1)
chart_type.get_tk_widget().pack()

fig2 = plt.figure(figsize=(6,5), dpi=100)
fig2.set_figwidth(14)
fig2.set_figheight(5.3)
ax2 = fig2.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig2, tab2)
chart_type.get_tk_widget().pack()

fig3 = plt.figure(figsize=(6,5), dpi=100)
fig3.set_figwidth(14)
fig3.set_figheight(5.3)
ax3 = fig3.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig3, tab3)
chart_type.get_tk_widget().pack()

fig4 = plt.figure(figsize=(6,5), dpi=100)
fig4.set_figwidth(14)
fig4.set_figheight(5.3)
ax4 = fig4.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig4, tab4)
chart_type.get_tk_widget().pack()

fig5 = plt.figure(figsize=(6,5), dpi=100)
fig5.set_figwidth(14)
fig5.set_figheight(5.3)
ax5 = fig5.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig5, tab5)
chart_type.get_tk_widget().pack()

fig6 = plt.figure(figsize=(6,5), dpi=100)
fig6.set_figwidth(14)
fig6.set_figheight(5.3)
ax6 = fig6.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig6, tab6)
chart_type.get_tk_widget().pack()

fig7 = plt.figure(figsize=(6,5), dpi=100)
fig7.set_figwidth(14)
fig7.set_figheight(5.3)
ax7 = fig7.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig7, tab7)
chart_type.get_tk_widget().pack()

fig8 = plt.figure(figsize=(6,5), dpi=100)
fig8.set_figwidth(14)
fig8.set_figheight(5.3)
ax8 = fig8.add_subplot(1,1,1)
plt.tight_layout()
chart_type = FigureCanvasTkAgg(fig8, tab8)
chart_type.get_tk_widget().pack()

ani1 = animation.FuncAnimation(fig, animate, interval=100)
ani2 = animation.FuncAnimation(fig2, animate, interval=100)
ani3 = animation.FuncAnimation(fig3, animate, interval=100)
ani4 = animation.FuncAnimation(fig4, animate, interval=100)
ani5 = animation.FuncAnimation(fig5, animate, interval=100)
ani6 = animation.FuncAnimation(fig6, animate, interval=100)
ani7 = animation.FuncAnimation(fig7, animate, interval=100)
ani8 = animation.FuncAnimation(fig8, animate, interval=100)


tabControl.place(x=25, y=400)
frame2 = tk.Frame(master=window)
frame2.place(x=1225, y=150)

listNodes = tk.Listbox(frame2, width=50, height=29, font=("Helvetica", 12))
listNodes.pack(side="left", fill="y")

scrollbar = tk.Scrollbar(frame2, orient="vertical")
scrollbar.config(command=listNodes.yview)
scrollbar.pack(side="right", fill="y")

listNodes.config(yscrollcommand=scrollbar.set)
#scrollbar.yview_pickplace("end")

t1 = Thread(target=serialListen)
t1.start()
#window.after(5000, lambda : serialListen())
window.mainloop()

