import sys
import threading
from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
import pyqtgraph as pg

import serial, csv, os
from datetime import datetime

current_directory = os.getcwd()
starttime = datetime.now()
starttime = str(starttime.strftime("%m%d%Y%H%M%S"))
folder = current_directory+"\logs\log "+str(starttime)
os.mkdir(folder)

f = open(folder+'/imudata.csv', 'w', encoding='UTF8', newline='')
header = ['Time', 'Type', 'X', 'y', 'Z']
writer = csv.writer(f)
writer.writerow(header)
f1 = open(folder+'/gpsdata.csv', 'w', encoding='UTF8', newline='')
header1 = ['Time', 'Type', 'X', 'y', 'Z'] 
writer1 = csv.writer(f1)
writer.writerow(header1)
f2 = open(folder+'/bmp280.csv', 'w', encoding='UTF8', newline='')
header2 = ['Time', 'Altitude', 'Temperature', 'Pressure']
writer2 = csv.writer(f2)
writer2.writerow(header2)
f3 = open(folder+'/mq135.csv', 'w', encoding='UTF8', newline='')
header3 = ['Time', 'Analog value']
writer3 = csv.writer(f3)
writer3.writerow(header3)


print("function running..")
try:
    s = serial.Serial("COM6")
    s.baudrate = 19200
    s.setRTS(0)
except:
    print("Serial Unavailable!")


def seriallisten(window):
    count=0
    while True:
        count = count + 1
        if count == 100:
            f.flush()
            fl.flush()
            f2.flush()
            f3.flush()
            count = 0
            
        data_recieved = s.readline()
        try:
            #Data Cleanup data_recieved data recieved
            data_recieved = data_recieved.decode('utf-8')
            data_recieved = data_recieved.strip()
            data_recieved = data_recieved.replace("\r", "")
           
            initialparse = str(data_recieved).split("(")
            #print(initialparse)
            
            datatype = initialparse[0]
            data = initialparse[1].split(')')
            data = data[0]
            #print(data)
            
        except:
            print("Parsing Error: "+str(data_recieved))
            continue
        
        
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        
        
        if datatype == "gpslocation":
            gpsllist = data.split(",")
            if len(gpsllist) !=3:
                print("Parsing Error GPS lenght: "+str(gpsllist))
                continue
            gpsllist.insert(0, tine)
            try:
                window.update_data_for_tab(7, float(gpsllist[3]))
                writer1.writerow(gpsllist)
            except:
                print("Parsing Error GPS: "+str(gpsllist))
                continue
                print(data)
                
        if datatype == "imuaccel":
            imuaccellist = data.split(",")
            imuaccellist.insert(0, time)
            imuaccellist.insert(1, "Accelerometer")
            writer.writerow(imuaccellist)
            
        if datatype == "imugyro":
            imugyrolist = data.split(",")
            if len(imugyrolist) == 3:
                print("Parsing Error IMU gyro >3: "+str(imugyrolist))
                continue
            imugyrolist.insert(0, time)
            imugyrolist.insert(1, "Gyro")
            try:
                if len(str(imugyrolist[2])) > 3:
                    window.update_data_for_tab(1, float(imugyrolist[2]))
                if len(str(imugyrolist[3])) > 3:
                    window.update_data_for_tab(2, float(imugyrolist[3]))
                if len(str(imugyrolist[4])) > 3:
                    window.update_data_for_tab(8, float(imugyrolist[4])) 
                writer.writerow(imugyrolist)
            except:
                print("Parsing Error IMU gyro: "+str(imugyrolist))
                continue
            
            
        if datatype == "bmp280":
            bmp280list = data.split(",")
            if len(bmp280list) != 3:
                print("Parsing Error bmp280: "+str(bmp280list))
                continue
            bmp2801ist.insert(0, time)
            try:
                if len(str(bmp2801ist[1])):
                    window.update_data_for_tab(3, float(bmp2881ist[1]))
                if len(str(bmp2881ist[2])) == 5:
                    window.update_data_for_tab(4, float(bmp2881ist[2]))
                if len(str(bmp2881ist[3])) == 9:
                    window.update_data_for_tab(5, float(bmp2881ist[3]))
                writer2.writerow(bmp2801ist)
            except:
                print("Parsing Error bmp288: "+str(bmp280list))
                continue



        if datatype == "mq135":
            mq1351ist = []
            mq1351ist.append(data)
            if len(mq1351ist) != 1:
                print("Parsing Error mq135: "+str(mq1351ist))
                continue
            mq1351ist.insert(0, time)
            try:
                window.update_data_for_tab(6, int(data))
                writer3.writerow(mg1351ist)
            except Exception as e:
                print("Parsing Error mq135: "+str(mq1351ist) + str(e))
                continue
           
           
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set the window title
        self.setWindowTitle("Cansat Live Data view")
        self.setWindowIcon (QIcon("Cansat_key_visual_pillars.png"))
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(self.tab1, "Gyro X")
        self.tabs.addTab(self.tab2, "Gyro Y")
        self.tabs.addTab(self.tab8, "Gyro Z")
        self.tabs.addTab(self.tab7, "GPS Altitude")
        self.tabs.addTab(self.tab3, "BMP Altitude")
        self.tabs.addTab(self.tab4, "BMP Temperature")
        self.tabs.addTab(self.tab5, "BMP Pressure")
        self.tabs.addTab(self.tab6, "MQ135 sensor")
        
        # Set the central widget of the main window to the tab widget
        self.setCentralWidget(self.tabs)
        # Create the graphs for each tab
        
        self.curves = []
        self.xrange = []
        for i, tab in enumerate(
            [self.tab1, self.tab2, self.tab3, self.tab4, self.tab5, self.tab6, self.tab7, self.tab8]
        ):
        
            graph = pg.PlotWidget()
            tab.layout = QVBoxLayout()
            tab.layout.addWidget(graph)
            tab.setLayout(tab.layout)
            
            # Generate initial data and plot it
            x = [0]
            y = [0]
            pen = pg.mkPen(color="r", width=2)
            curve = graph.plot(x, y, pen=pen)
            self.xrange.append([0, 100])
            
            # Add the curve to the list of curves
            self.curves.append(curve)
            
            reset_button=QPushButton("Reset Graph")
            reset_button.clicked.connect(lambda checked, i=i: self.reset_graph(i))
            tab.layout.addWidget(reset_button)
          
          
    def update_data(self):
        # Update all graphs
        for i in range(len(self.curves)):
            self.update_data_for_tab(1)
            
    def reset_graph(self, tab_index):
        curve = self.curves[tab_index]
        curve.setData([0], [0])
        self.xrange[tab_index] [0, 100]
        curve.getViewBox().setRange(self.xrange[tab_index][0], self.xrange[tab_index][1])
        
    def update_data_for_tab(self, tab_index, y):
        # Generate new random data for the specified graph
        tab_index = tab_index-1
        max_data_points = 1000
        curve = self.curves[tab_index]
        
        # Add the new data point to the existing plot
        x, y_old = curve.getData()   
        x = list(x) + [x[-1] + 1]
        y = list(y_old) + [y]
        
        if len(x) > max_data_points:
            print("point limit reached")
            x = x[max_data_points:]
            y = y[max_data_points:]
            
        curve.setData(x, y)
        
        # Shift the visible range of the x-axis to scroll the plot
        if x[-1]> self.xrange[tab_index][1]:
            self.xrange[tab_index][0] += 1
            self.xrange[tab_index][1] += 1
            curve.getViewBox().setXRange(self.xrange[tab_index][0], self.xrange[tab_index][1])
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # Create and start a new thread for the update_data_caller function
    # Example: update tab 1 (index 0) every 2 seconds (sleep_time = 2)
    update_thread = threading.Thread(target=seriallisten, args=[window])
    update_thread.start()
    
    sys.exit(app.exec_())
