# -*- coding: utf-8 -*-s

                  ####################################
                  #                                  #
                  #  TFG Aitor Invernón De Campos    #
                  #  Universitat de Barcelona        #
                  #  Facultat de Física              #
                  #                                  #
                  #  Direcció del TFG:               #
                  #  J. M. Hernàndez Ferràs          #
                  #  Antoni García Santiago          #
                  #                                  #
                  #  Barcelona, 2017                 #
                  #                                  #
                  ####################################
                  #                                  #
                  # Versió amb GUI adaptada per l'ús #
                  # al laboratori de física moderna. #
                  #                                  #
                  ####################################

################################################################################
################################################################################

import time
import warnings
import platform
import os
import csv

import serial
import serial.tools.list_ports

import threading

from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
from tkinter import Button
from tkinter import PhotoImage
from tkinter import font
import PIL.Image
import PIL.ImageTk

################################################################################
################################################################################

# Definició de funcions necessàries

def CleanBuffer(n, ser):
    
 # Funció per netejar el buffer del port sèrie, on espera "n" segons entre el
 # "flushInput" i el "flushOutput"
 
 import time
    
 ser.setDTR(False)
 #ser.flushInput()
 time.sleep(n)
 ser.flushInput()
 ser.setDTR(True)
 
#------------------------------------------------------------------------------#

def GoTo(linenum):
    
 # Funció "goto" per anar a una línia de codi detrminada "linenum"
    
 global line
 line = linenum

################################################################################
################################################################################

# Per pyinstaller

def resource_path(relative_path):

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

P13aImg3_path = resource_path('P13aImg3.png')
P13aICO_path = resource_path('P13a.ico')

################################################################################
################################################################################

# Cridem la funció que ens permet saber la data i hora actual

DataMessures = time.strftime("%d-%m-%Y a les %Hh %Mmin %Sseg", time.localtime())

# Determinem el directori actual i si cal creem un de nou per guardar les dades

DadesDirAlumnes = os.getcwd() + "/Dades P13a alumnes"
       
if not os.path.exists(os.path.join(DadesDirAlumnes)):
       os.makedirs(os.path.join(DadesDirAlumnes))

# Obrim els arxius ".csv" que permetran guardar les dades provinents del port 
# sèrie, en un nou directori que conté l'hora local en la qual es realitza la 
# captura de les dades

rootArxiu = tkinter.Tk()
rootArxiu.withdraw()

rootArxiu.overrideredirect(True)
rootArxiu.geometry('0x0+0+0')

rootArxiu.deiconify()
rootArxiu.lift()
rootArxiu.focus_force()

ArxiuAlumnes = tkinter.simpledialog.askstring("Informació necessària", "Introduïu un nom pels arxius CSV finals", parent=rootArxiu)
askTlim = tkinter.simpledialog.askinteger("Informació necessària", "Introduïu la temperatura límit inferior per començar i aturar la captura de dades (en °C)", parent=rootArxiu)

rootArxiu.destroy()

# Es crea dins el directori actual una carpeta per cada grup i sessió

DadesDirAlumnesGrup = DadesDirAlumnes + "/" + ArxiuAlumnes + " ("+DataMessures+")"
       
if not os.path.exists(os.path.join(DadesDirAlumnesGrup)):
       os.makedirs(os.path.join(DadesDirAlumnesGrup))

Arxiu5 = open(os.path.join(DadesDirAlumnesGrup, ArxiuAlumnes+" - Registre total (Només dades numèriques) "+" ("+DataMessures+").csv"),
              'w', encoding='utf-8', errors='replace')
Arxiu6 = open(os.path.join(DadesDirAlumnesGrup, ArxiuAlumnes+" - Registre refredament (Amb informació) "+" ("+DataMessures+").csv"),
              'w', encoding='utf-8', errors='replace')
Arxiu7 = open(os.path.join(DadesDirAlumnesGrup, ArxiuAlumnes+" - Registre refredament (Només dades numèriques) "+" ("+DataMessures+").csv"),
              'w', encoding='utf-8', errors='replace')

################################################################################
################################################################################

# Es genera la App per tal que quan es cridi "sys.stdout.write", automàticament 
# s'activi "redirector".

def redirector(inputStr):
    textbox.insert(INSERT, inputStr)

sys.stdout.write = redirector

# Classe aplicació per tal d'enviar tot el contingut a la GUI com un "thread" 
# a part del programa principal

class GUIapp(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):

        self.root=tkinter.Tk()
        self.root.title("UB - Laboratori de Física Moderna - Pràctica 13a: Banda prohibida del germani")

        textfont1 = font.Font(family='Helvetica', size=8, weight='normal')
        textfont2 = font.Font(family='Helvetica', size=10, weight='normal')
        textfont3 = font.Font(family='Helvetica', size=12, weight='normal')
        textfont4 = font.Font(family='Helvetica', size=14, weight='normal')
        textfont5 = font.Font(family='Helvetica', size=18, weight='normal')
        textfont6 = font.Font(family='Helvetica', size=20, weight='normal')
        textfont7 = font.Font(family='Helvetica', size=30, weight='normal')
        textfont1b = font.Font(family='Helvetica', size=8, weight='bold')
        textfont2b = font.Font(family='Helvetica', size=10, weight='bold')
        textfont3b = font.Font(family='Helvetica', size=12, weight='bold')
        textfont4b = font.Font(family='Helvetica', size=14, weight='bold')
        textfont5b = font.Font(family='Helvetica', size=18, weight='bold')
        textfont6b = font.Font(family='Helvetica', size=20, weight='bold')
        textfont7b = font.Font(family='Helvetica', size=30, weight='bold')
        textfont1i = font.Font(family='Helvetica', size=8, slant='italic')
        textfont2i = font.Font(family='Helvetica', size=10, slant='italic')
        textfont3i = font.Font(family='Helvetica', size=12, slant='italic')
        textfont4i = font.Font(family='Helvetica', size=14, slant='italic')
        textfont5i = font.Font(family='Helvetica', size=18, slant='italic')
        textfont6i = font.Font(family='Helvetica', size=20, slant='italic')
        textfont7i = font.Font(family='Helvetica', size=30, slant='italic')
        textfont1ib = font.Font(family='Helvetica', size=8, slant='italic', weight='bold')
        textfont2ib = font.Font(family='Helvetica', size=10, slant='italic', weight='bold')
        textfont3ib = font.Font(family='Helvetica', size=11, slant='italic', weight='bold')
        textfont4ib = font.Font(family='Helvetica', size=13, slant='italic', weight='bold')
        textfont5ib = font.Font(family='Helvetica', size=18, slant='italic', weight='bold')
        textfont6ib = font.Font(family='Helvetica', size=19, slant='italic', weight='bold')
        textfont7ib = font.Font(family='Helvetica', size=30, slant='italic', weight='bold')
        font.families()
        bgcolor='white'

        self.root.configure(background=bgcolor)
        self.root.wm_state('zoomed')

        self.s1 = tkinter.StringVar()
        self.s1.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labels1 = tkinter.Label(self.root, textvariable=self.s1, bg=bgcolor, fg="black", font=textfont2ib, borderwidth=1, relief="flat")
        labels1.place(relx=.50, rely=.275, anchor="center")

        self.s2red = tkinter.StringVar()
        self.s2red.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labels2red = tkinter.Label(self.root, textvariable=self.s2red, bg=bgcolor, fg="red", font=textfont4b)
        labels2red.place(relx=.50, rely=.435, anchor="center")
        
        #self.s2redel = tkinter.StringVar()
        #self.s2redel.set(' ')
        #self.root.protocol("WM_DELETE_WINDOW", self.callback)
        #labels2redel = tkinter.Label(self.root, textvariable=self.s2redel, bg=bgcolor, fg="red", font=textfont4b)
        #labels2redel.place(relx=.50, rely=.435, anchor="center")

        self.s2 = tkinter.StringVar()
        self.s2.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labels2 = tkinter.Label(self.root, textvariable=self.s2, bg=bgcolor, fg="black", font=textfont4b)
        labels2.place(relx=.50, rely=.405, anchor="center")

        self.sDades = tkinter.StringVar()
        self.sDades.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labelsDades = tkinter.Label(self.root, textvariable=self.sDades, bg=bgcolor, fg="black", font=textfont6ib)
        labelsDades.place(relx=.50, rely=.607, anchor="center")

        self.sSeparadorNoArd = tkinter.StringVar()
        self.sSeparadorNoArd.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labelsSeparadorNoArd = tkinter.Label(self.root, textvariable=self.sSeparadorNoArd, bg=bgcolor, fg="black", font=textfont4ib)
        labelsSeparadorNoArd.place(relx=.50, rely=.584, anchor="center")

        self.sSeparador = tkinter.StringVar()
        self.sSeparador.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labelsSeparador = tkinter.Label(self.root, textvariable=self.sSeparador, bg=bgcolor, fg="black", font=textfont4ib)
        labelsSeparador.place(relx=.50, rely=.572, anchor="center")

        self.sTlim = tkinter.StringVar()
        self.sTlim.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posTlim = tkinter.Label(self.root, textvariable=self.sTlim, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont5)
        posTlim.place(relx=.35, rely=.538, anchor="center")
        titTlim = tkinter.Label(self.root, text="T límit inferior (°C)", bg=bgcolor, fg="black", font=textfont4b)
        titTlim.place(relx=.35, rely=.498, anchor="center")

        self.sTact = tkinter.StringVar()
        self.sTact.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posTact = tkinter.Label(self.root, textvariable=self.sTact, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont5)
        posTact.place(relx=.50, rely=.538, anchor="center")
        titTact = tkinter.Label(self.root, text="T actual (°C)", bg=bgcolor, fg="black", font=textfont4b)
        titTact.place(relx=.50, rely=.498, anchor="center")

        self.sTmax = tkinter.StringVar()
        self.sTmax.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posTmax = tkinter.Label(self.root, textvariable=self.sTmax, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont5)
        posTmax.place(relx=.65, rely=.538, anchor="center")
        titTmax = tkinter.Label(self.root, text="T màxima (°C)", bg=bgcolor, fg="black", font=textfont4b)
        titTmax.place(relx=.65, rely=.498, anchor="center")

        self.sT = tkinter.StringVar()
        self.sT.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posT = tkinter.Label(self.root, textvariable=self.sT, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont6)
        posT.place(relx=.12, rely=.737, anchor="center")
        titT = tkinter.Label(self.root, text="T (K)", bg=bgcolor, fg="black", font=textfont5b)
        titT.place(relx=.12, rely=.682, anchor="center")

        self.sdT = tkinter.StringVar()
        self.sdT.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posdT = tkinter.Label(self.root, textvariable=self.sdT, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont6)
        posdT.place(relx=.25, rely=.737, anchor="center")
        titdT = tkinter.Label(self.root, text="δT (K)", bg=bgcolor, fg="black", font=textfont5b)
        titdT.place(relx=.25, rely=.682, anchor="center")

        self.sI = tkinter.StringVar()
        self.sI.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posI = tkinter.Label(self.root, textvariable=self.sI, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont6)
        posI.place(relx=.43, rely=.737, anchor="center")
        titI = tkinter.Label(self.root, text="I (mA)", bg=bgcolor, fg="black", font=textfont5b)
        titI.place(relx=.43, rely=.682, anchor="center")

        self.sdI = tkinter.StringVar()
        self.sdI.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posdI = tkinter.Label(self.root, textvariable=self.sdI, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont6)
        posdI.place(relx=.56, rely=.737, anchor="center")
        titdI = tkinter.Label(self.root, text="δI (mA)", bg=bgcolor, fg="black", font=textfont5b)
        titdI.place(relx=.56, rely=.682, anchor="center")

        self.sV = tkinter.StringVar()
        self.sV.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posV = tkinter.Label(self.root, textvariable=self.sV, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont6)
        posV.place(relx=.74, rely=.737, anchor="center")
        titV = tkinter.Label(self.root, text="V (mV)", bg=bgcolor, fg="black", font=textfont5b)
        titV.place(relx=.74, rely=.682, anchor="center")

        self.sdV = tkinter.StringVar()
        self.sdV.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        posdV = tkinter.Label(self.root, textvariable=self.sdV, bg=bgcolor, borderwidth=2, relief="sunken", fg="black", font=textfont6)
        posdV.place(relx=.87, rely=.737, anchor="center")
        titdV = tkinter.Label(self.root, text="δV (mV)", bg=bgcolor, fg="black", font=textfont5b)
        titdV.place(relx=.87, rely=.682, anchor="center")

        self.s3red = tkinter.StringVar()
        self.s3red.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labels3red = tkinter.Label(self.root, textvariable=self.s3red, bg=bgcolor, fg="red", font=textfont4ib)
        labels3red.place(relx=.5, rely=.847, anchor="center")

        #self.s3bis = tkinter.StringVar()
        #self.s3bis.set(' ')
        #self.root.protocol("WM_DELETE_WINDOW", self.callback)
        #labels3bis = tkinter.Label(self.root, textvariable=self.s3bis, bg=bgcolor, fg="black", font=textfont2ib)
        #labels3bis.place(relx=.5, rely=.91, anchor="center")

        self.s3green = tkinter.StringVar()
        self.s3green.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labels3green = tkinter.Label(self.root, textvariable=self.s3green, bg=bgcolor, fg="green", font=textfont5ib)
        labels3green.place(relx=.5, rely=.847, anchor="center")

        self.s3red2 = tkinter.StringVar()
        self.s3red2.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labels3red2 = tkinter.Label(self.root, textvariable=self.s3red2, bg=bgcolor, fg="red", font=textfont4ib)
        labels3red2.place(relx=.5, rely=.915, anchor="center")

        self.s3 = tkinter.StringVar()
        self.s3.set(' ')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        labels3 = tkinter.Label(self.root, textvariable=self.s3, bg=bgcolor, fg="black", font=textfont4ib)
        labels3.place(relx=.5, rely=.847, anchor="center")

        btnSortir = Button(self.root, text="Sortir", command=self.root.destroy, bg=bgcolor, fg="black", font=textfont4b)
        btnSortir.place(relx=.5, rely=.962, anchor="center")

        #self.bkgrnd = PIL.Image.open('P13aImg3.png') # 7
        self.bkgrnd = PIL.Image.open(P13aImg3_path) # 7
        self.bkgrnd = self.bkgrnd.resize((1120, 160), PIL.Image.ANTIALIAS)
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        bkgrndtk = PIL.ImageTk.PhotoImage(self.bkgrnd)
        labelbkgrnd = tkinter.Label(self.root, image=bkgrndtk)
        labelbkgrnd.place(relx=.5, rely=.125, anchor="center")

        self.root.mainloop()

app = GUIapp()

################################################################################
################################################################################

# Variable "arduino_ports" com a llistat de unitats Arduino connectades 
# als ports COM disponibles (Font: https://goo.gl/lGd3LA)

arduino_ports = [p.device       
                 for p in serial.tools.list_ports.comports()
                 if 'Arduino' in p.description ] 

if not arduino_ports:              # Si no hi ha cap Arduino connectat

    app.s1.set("\n No s'ha detectat cap Arduino "
             +"\n\n Si us plau, reviseu la configuració experimental! "+
             "\n _________ ")
    
    app.sSeparadorNoArd.set("\n __________________ ")

    app.sTlim.set("n/a")
    app.sTact.set("n/a")
    app.sTmax.set("n/a")
    app.sT.set("n/a")
    app.sdT.set("n/a")
    app.sI.set("n/a")
    app.sdI.set("n/a")
    app.sV.set("n/a")
    app.sdV.set("n/a")

    app.s3red2.set("\nSORTIU I INICIEU DE NOU!\n")
    
if len(arduino_ports) > 1:         # Si hi ha més d'un Arduino connectat   

    app.s1.set("\n S'ha detectat més d'un Arduino!!! "
             +"\n S'utilitzarà el primer de la llista "+
             "\n _________ ")
    
    app.sSeparadorNoArd.set("\n __________________ ")

# Definim una variable que enmagatzema la informació del port sèrie actiu

nameArduino = list(serial.tools.list_ports.comports())
for p in nameArduino:
    ArduinoName = str(p[1])

ser = serial.Serial(arduino_ports[0])
port = ser.port
baudrate = 57600
versioPy = (platform.python_version())

app.s1.set("\n Versió de Python utilitzada: "
         +str(versioPy)+" \n"+
         "\n Dispositiu connectat: "+ArduinoName+" (Baudrate: "+str(baudrate)+") "+
         "\n _________ ")

CleanBuffer(0, ser)
ser.close()
ser = serial.Serial(arduino_ports[0],baudrate=57600)

################################################################################
################################################################################

# Format de les dades a guardar

T_formtext = ("{0:^6s}".format("T"))
errorT_formtext = ("{:^4s}".format("δ(T)   (K)"))
I_formtext = ("{:^5s}".format("I"))
errorI_formtext = ("{:^6s}".format(" δ(I)   (mA)"))
DifV_formtext = ("{:^5s}".format("dV"))
errorDifV_formtext = ("{:^5s}".format("δ(dV)  (mV)"))
  
# Capçalera de cada arxiu de dades generat
             
Arxiu6.write("Arxiu en format CSV creat el/l´: " + DataMessures + "\n")
Arxiu6.write("\nNomés s'inclouen les dades acumulades durant el refredament des de la temperatura"
             +"\nmàxima assolida fins a una certa temperatura límit inferior.\n")
Arxiu6.write("\n\n1a i 2a columna: " +T_formtext+'±  '+errorT_formtext
             +"\n3a i 4a columna: " +I_formtext+' ± '+errorI_formtext
             +"\n5a i 6a columna: "+DifV_formtext+' ±  '
             +errorDifV_formtext+ "\n\n")

################################################################################
################################################################################

# Definim vectors de variables

Temperatura = []
errorTemperatura = []
Intensitat = []
errorIntensitat = []
DifV = []
errorDifV = []

AUXTemperatura = []
AUXerrorTemperatura = []
AUXIntensitat = []
AUXerrorIntensitat = []
AUXDifV = []
AUXerrorDifV = []

# Definició de contadors

cnt=0
cnt2=0

tempON = 0
linemax = 0

strout0 = 0
strout1 = 0
strout2 = 0

################################################################################
################################################################################     

# Per limitar el temps d'espera quan T<30°C

tinicial = time.time()
MAXt = 180.0 # En segons

# Control i límit de T per gestionar quan capturar les dades

TmaxAssolida = 0.0
TLIMassolida = 0.0    

# Es duplica la lectura de T per si llegeix una línia a mitjes

Tread = ser.readline().decode('utf8').strip('\r').strip('\n').split(' , ')
Tread = ser.readline().decode('utf8').strip('\r').strip('\n').split(' , ')

Taux = float(Tread[0])
TCaux = float(Tread[12])

TmaxAssolida = TmaxAssolida  if TmaxAssolida>TCaux else TCaux
app.sTmax.set(str("{:5.2f}".format(TmaxAssolida)))

T_K = 273.15
TLIM = float(askTlim) + T_K
TMAX = 172.00 + T_K


if Taux < TLIM: GoTo(1)

elif Taux >= TLIM: GoTo(2)
 
################################################################################
################################################################################

#########
line = 1#
#########

app.sT.set("n/a")
app.sdT.set("n/a")
app.sI.set("n/a")
app.sdI.set("n/a")
app.sV.set("n/a")
app.sdV.set("n/a")

#while Taux < TLIM:

t = time.time() 
while (Taux < TLIM) and (time.time()-t< MAXt):

 tt=MAXt-(time.time()-t)
 mins, secs = divmod(int(tt), 60)
 timeformat = '{:02d}:{:02d}'.format(mins, secs)
 
 Tread = ser.readline().decode('utf8').strip('\r').strip('\n').split(' , ')   
 Taux = float(Tread[0])
 TCaux = float(Tread[12])
 
 TmaxAssolida = TmaxAssolida  if TCaux<TmaxAssolida else TCaux
 app.sTmax.set(str("{:5.2f}".format(TmaxAssolida)))

 app.sTlim.set(TLIM - T_K)
 strTCaux = str("{0:.2f}".format(TCaux))
 app.sTact.set(strTCaux)

 app.s2.set("Disposeu de "+str(int(tt))+" segons abans que el programa s'aturi:\n")

 app.s2red.set("\nSI US PLAU, PREMEU EL BOTÓ D'ESCALFAMENT DE LA PLACA!")

 app.sSeparador.set("\n __________________ ")


 
 if Taux >= TLIM: GoTo(2)
 
 if tt < 1.0:
  
  app.sTlim.set(TLIM - T_K)
  app.sT.set("n/a")
  app.sdT.set("n/a")
  app.sI.set("n/a")
  app.sdI.set("n/a")
  app.sV.set("n/a")
  app.sdV.set("n/a") 
  
  app.s2.set("   ")

  app.s2red.set("   ")

  app.sSeparador.set("\n __________________ ")

  app.s3.set("\nHeu superat el temps màxim de què disposàveu\n"+
             "per prémer el botó d’escalfament de la placa...")

  app.s3red2.set("\nSORTIU I INICIEU L'APLICACIÓ DE NOU!\n")

  break 
  
  Arxiu5.close()
  Arxiu6.close()
  Arxiu7.close()
  
  raise SystemExit

#########
line = 2#
#########
      
while Taux >= TLIM:
      
 tempON = 1
    
 # Inicialitzem la lectura dels valors del port sèrie

 # Dades del port considerant valors i separadors

 DadesPortSerieOUT = ser.readline().decode('utf8').strip('\r').strip('\n').split(' , ') 

 # Definició de cada variable
 
 Temperatura = float(DadesPortSerieOUT[0])           # T
 errorTemperatura = float(DadesPortSerieOUT[1])      # δ(T)  
 Intensitat = float(DadesPortSerieOUT[4])            # I
 errorIntensitat = float(DadesPortSerieOUT[5])       # δ(I) 
 DifV = float(DadesPortSerieOUT[6])                  # dV 
 errorDifV = float(DadesPortSerieOUT[7])             # δ(dV) 
 TemperaturaC = float(DadesPortSerieOUT[12])           # T (°C)

 TmaxAssolida = TmaxAssolida  if TemperaturaC<TmaxAssolida else TemperaturaC
 app.sTmax.set(str("{:5.2f}".format(TmaxAssolida)))
 
 # Vectors de dades acumulatius per cada variable 
  
 AUXTemperatura.append(Temperatura)              # T
 AUXerrorTemperatura.append(errorTemperatura)    # δ(T)
 AUXIntensitat.append(Intensitat)                # I
 AUXerrorIntensitat.append(Intensitat)           # δ(I)
 AUXDifV.append(DifV)                            # dV
 AUXerrorDifV.append(errorDifV)                  # δ(dV)

 # Format de les dades
  
 T_format = ("{:5.2f}".format(Temperatura))
 errorT_format = ("{:3.2f}".format(errorTemperatura))
 I_format = ("{:4.3f}".format(Intensitat))
 errorI_format = ("{:4.3f}".format(errorIntensitat))
 DifV_format = ("{:6.0f}".format(DifV))
 errorDifV_format = ("{:4.0f}".format(errorDifV))
 TC_format = ("{:5.2f}".format(TemperaturaC))
 
 # Creació d'un "string" diferent per cada arxiu
  
 strDades = str(T_format+' \xc2\xb1 '+errorT_format+' | '+I_format+' \xc2\xb1 '
                +errorI_format+' | '+DifV_format+' \xc2\xb1 '+errorDifV_format)
                     
 Dades = (T_format, errorT_format, I_format, errorI_format, DifV_format, errorDifV_format)
  
 strTempIDifV = str(T_format+' \xc2\xb1 '+errorT_format+' | '+I_format
                    +' \xc2\xb1 '+errorI_format+' | '+DifV_format+' \xc2\xb1 '
                    +errorDifV_format)
  
 # Mentre, es mostren les dades arribades pel port

 cnt=cnt+1
 
 app.sTlim.set(TLIM - T_K)
 app.sTact.set(TC_format)
 
 app.s2red.set("")

 app.s2.set("\nJa s'ha superat la temperatura límit inferior seleccionada...\n"+
            "\nEn arribar la mostra de Ge a la seva temperatura màxima,\n"+
            "començarà l'enregistrament de les dades capturades:\n")

 app.sSeparador.set(" __________________ ")

 app.sDades.set("\nInformació capturada en temps real provinent del muntatge experimental:")

 app.sT.set(T_format)
 app.sdT.set(errorT_format)
 app.sI.set(I_format)
 app.sdI.set(errorI_format)
 app.sV.set(DifV_format)
 app.sdV.set(errorDifV_format)

 # S'escriuen les dades "cadena a cadena" als arxius corresponents

 Arxiu5.write(T_format+' '+errorT_format+' '+I_format+' '+errorI_format+' '
              +DifV_format+' '+errorDifV_format+"\n")
      
 if Temperatura < TLIM:

  DataFinal = time.strftime("%Hh %Mmin %Sseg del %d-%m-%Y", time.localtime())

  app.s2.set("\n \n"+
            "\n \n"+
            " \n")

  app.sSeparador.set(" __________________ ")

  app.sDades.set("\n ")

  app.sT.set("n/a")
  app.sdT.set("n/a")
  app.sI.set("n/a")
  app.sdI.set("n/a")
  app.sV.set("n/a")
  app.sdV.set("n/a")

  #app.s3.set("\nLa mostra s'ha refredat fins a la temperatura límit inferior desitjada.\n"+
  #           "\nS'HA ATURAT LA PRESA DE DADES, FINS A LA PROPERA!\n"+
  #           "\n(Arxius de dades a la carpeta:  Dades P13a alumnes)\n")

  app.s3green.set("\nLa mostra s'ha refredat fins a la temperatura límit inferior desitjada...\n"+
             "\nS'HA ATURAT LA PRESA DE DADES, FINS A LA PROPERA!\n")

  app.sDades.set("\nTrobareu els arxius de dades a la carpeta de l'escriptori: 'Dades P13a alumnes'")
  
  break

  ser.close()
     
################################################################################
################################################################################   
                        
Arxiu5.close()

if tempON == 1:
    
   for index, number in enumerate(AUXTemperatura):
    
       if number == max(AUXTemperatura):
        
          linemax = index

   numlin = len(AUXTemperatura) - linemax
                            
   tmp = open(os.path.join(DadesDirAlumnesGrup, ArxiuAlumnes+" - Registre total (Només dades numèriques) "+" ("+DataMessures+").csv"),'r')

   itmp=(linea for i,linea in enumerate(tmp) if i>=linemax)

   for linea in itmp:
    
       Arxiu6.write(linea)
       Arxiu7.write(linea)

   TmaxAssolida = max(AUXTemperatura) - T_K
   app.sTmax.set(str("{:5.2f}".format(TmaxAssolida)))
   TLIMassolida = TLIM - T_K
   Arxiu6.write("\n\nS'ha aturat la captura de dades a les: " + DataFinal +
                "\n\nDesprés de: " + str(numlin) + " mesures"+
                "\n\n\nTemperatura límit inferior introduïda per començar i aturar la captura de dades: " + str("{:5.2f}".format(TLIMassolida)) +" °C"
                "\n\nTemperatura màxima assolida: " + str("{:5.2f}".format(TmaxAssolida)) +" °C")

Arxiu6.close()
Arxiu7.close()
      
################################################################################
################################################################################