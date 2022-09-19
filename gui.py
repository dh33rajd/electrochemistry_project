
#from .core import startCV, exportCSV
from core import *
from utilties import *

root.wm_title("CVGIT")
root.geometry('1100x500')

TITLE = Label(root, text='Cyclic Voltammetry GIT Client Interface')
TITLE.grid(column='1',row='1',columnspan='3',rowspan='1',pady=20)

substance = Label(root, text='Substance: Pottasium ferrocyanide in KCl')
substance.grid(column='1',row='2',columnspan='2',rowspan='1')

TIA_label = Label(root,text='TIA gain')
TIA_label.grid(column='3',row='2',columnspan='1',rowspan='1')

TIA = OptionMenu(root, variable_TIA, "Default", "2.75 KOhms",
                 "3.5 KOhms", "7 KOhms", "14 KOhms",
                 "35 KOhms", "120 KOhms", "350 KOhms")
TIA.grid(column='3',row='3',columnspan='1',rowspan='1')

w.grid(column='1',row='9',columnspan='3',rowspan='1',pady=50,padx=20)
w.insert('1.0','\n Welcome to Cyclic Voltammetry Client Interface.\n Please:\n 1) Connect the module to the cell \n 2) Choose your fit config.\n 3) Click Start and export .csv file.\n'+'\n'+'\n'+'IISER Bhopal')

a.plot(t_cv,DATA_cv,'blue')
a.grid(True)
dataPlot.draw()
dataPlot.get_tk_widget().grid(column='5',row='3', columnspan='2', rowspan='10')

menubar = Menu(root)
menubar.add_command(label="Start",command=start_CV)
menubar.add_command(label="Save graph",command=saveCV)
menubar.add_command(label="Export .csv",command=exportCSV)
menubar.add_command(label="Close",command=closeCV)

root.config(menu=menubar)
root.mainloop()
