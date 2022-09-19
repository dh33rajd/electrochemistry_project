import csv
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

DATA_cv = [0]*33
t_cv=[-0.2,-0.15,-0.1,-0.05,0,0.05,0.10,0.15,0.2,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.6,0.55,0.5,0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0,-0.05,-0.1,-0.15,-0.2]

root = Tk()

variable_TIA = StringVar(root)
variable_TIA.set("Default")

variable_OPMODE = StringVar(root)
variable_OPMODE.set("Default")

variable_scan_rate = StringVar(root)
variable_scan_rate.set("0.05")

f = Figure(figsize=(4,3), dpi=120, facecolor='white', frameon=False,tight_layout=True)
a = f.add_subplot(111,title='CV - CVGIT',
                  xlabel='v, V',
                  ylabel='i,'+ u"\u00B5"+'A',autoscale_on=True)
dataPlot = FigureCanvasTkAgg(f, master=root)

w = Text(root, width='60', height='12', bg='yellow', relief = 'groove')

def exportCSV():
    str = "cv"+".csv"
    csv_out = open(str, 'w')
    mywriter = csv.writer(csv_out)
    for row in zip(t_cv, DATA_cv):
        mywriter.writerow(row)
    csv_out.close()
    w.delete("1.0","end")
    w.insert('1.0', "Data exported to .csv succesfully!"+'\n'+'\n')
    
def saveCV():
    str =  "Results"+"cv"+".png"
    f.savefig(str, dpi=None, facecolor='w', edgecolor='w',
              orientation='landscape', format='png',
              transparent=False, bbox_inches=None, pad_inches=0.1,
              frameon=False)
    w.delete("1.0","end")
    w.insert('1.0', "Graph saved succesfully!"+'\n'+'\n')
    
def closeCV():
    LOCK = int('00000000',2)
    TIACN = int('00010100',2)
    REFCN = int('10100101',2)
    MODECN = int('00000000',2)
    print('Bye!')
    root.destroy()
