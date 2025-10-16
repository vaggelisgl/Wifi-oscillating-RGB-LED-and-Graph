import sys
from PyQt5.QtWidgets import *
import pyqtgraph as pg

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication

from math import sin,pi
import time
import socket




HOST="INPUT_your_host"
PORT=12345
mysocket =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
mysocket.settimeout(5.0)
on=True
print("UDP Client started. Enter data")

period=5
frequency = 1/period
numpoints=50
timestep=period/numpoints

redData= [0]*numpoints
greenData=[0]*numpoints
blueData=[0]*numpoints
timeData=[0]*numpoints

app=QApplication([])
window=QMainWindow()
window.setWindowTitle("WAVE GRAPH")
window.setGeometry(100,100,800,600)



widgetContainer=QWidget()
window.setCentralWidget(widgetContainer)
mainLayout=QVBoxLayout(widgetContainer)
plotWidget= pg.PlotWidget()
plotWidget.setLabel("left","y=sin(2*π*F*t)")
plotWidget.setLabel("bottom","time (s)")
plotWidget.setTitle("Things that oscillate")
plotWidget.addLegend()

mainLayout.addWidget(plotWidget)

for i in range (0,numpoints):
    t=i*timestep
    timeData[i]=t
    redData[i]=sin(2*pi*frequency*t)
    greenData[i]=sin(2*pi*frequency*t+(2*pi/3))
    blueData[i]=sin(2*pi*frequency*t-(2*pi/3))
redPlot=plotWidget.plot(timeData,redData,pen=pg.mkPen("r",width=3),name="Red")
greenPlot=plotWidget.plot(timeData,greenData,pen=pg.mkPen("g",width=3),name="Green")
bluePlot=plotWidget.plot(timeData,blueData,pen=pg.mkPen("b",width=3),name="Blue")
window.show()
tStart = time.perf_counter()

def updateGraph():
   global t,tStart,frequency
   t=t+timestep
   r=sin(2*pi*frequency*t)
   g=sin(2*pi*frequency*t+(2*pi/3))
   b=sin(2*pi*frequency*t-(2*pi/3))
   for i in range(numpoints-1):
       redData[i]=redData[i+1]
       blueData[i]=blueData[i+1]
       greenData[i]=greenData[i+1]
       timeData[i]=timeData[i+1]
   redData[numpoints-1]=r
   blueData[numpoints-1]=b
   greenData[numpoints-1]=g
   timeData[numpoints-1]=t
   
   r=0.5*255*(r+1)
   b=0.5*255*(b+1)
   g=0.5*255*(g+1)

   mydata=str(r)+":"+str(g)+":"+str(b)+'\n'
   mysocket.sendto(mydata.encode(),(HOST,PORT))
   redPlot.setData(timeData,redData)
   greenPlot.setData(timeData,greenData)
   bluePlot.setData(timeData,blueData)

   if redData[0]<=0 and redData[1]>0 :
       measuredPeriod = time.perf_counter()-tStart
       print("Measured Period: ",measuredPeriod)
       tStart=time.perf_counter()
    

timer =QTimer()
timer.timeout.connect(updateGraph)
timer.start(int(timestep*1000))
    
sys.exit(app.exec_())