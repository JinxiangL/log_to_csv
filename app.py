import pandas
import csv
from datetime import datetime
from tkinter.filedialog import askopenfilename, askdirectory 
from tkinter import Tk, ttk
import tkinter as tk
from tkinter import *

class APP_GUI:
    def __init__(self, window):
        self.window = window
        self.table = [] ## store the data from the log file
        self.listBox = None
        self.filename = '' ## store the filename of the log file
    
    ## make a layout for the application
    def set_init_window(self):
        label = tk.Label(self.window, text="LOG to CSV Converter", font=("Arial",20)).grid(row=0, columnspan=4)
        cols = ('Log Message', 'Start Time', 'End Time', 'Time Diff')
        self.listBox = ttk.Treeview(self.window, columns=cols, show='headings')
        for col in cols:
            self.listBox.heading(col, text=col)    
        self.listBox.grid(row=1, column=0, columnspan=3)
        
        importbutton = Button(self.window, text="Import log file", width=15, command=self.display_data).grid(row=4, column=0)
        downloadbutton = Button(self.window, text="Download csv file", width=15, command=self.write_data).grid(row=4, column=1)
        downloadbutton = Button(self.window, text="Exit", width=15, command=self.window.destroy).grid(row=4, column=2)
    
    ## get the data from the log file
    def get_data(self, path):
        data = pandas.read_csv(path, delimiter = " ", header = None)
        data.drop(data.columns[[3, 4, 6]], axis = 1, inplace = True)
        data = data.values
        self.table = []
        for i in range(0, len(data)):
            if "starts" in data[i][5]:
                s = data[i][5]
                s = s[:len(s)-7]
                for j in range(i+1, len(data)):
                    if "end" in data[j][5] and s in data[j][5]:
                        log_message = data[i][5]+' - '+data[j][5]
                        start_time = data[i][0]+' '+data[i][1]
                        end_time = data[j][0]+' '+data[j][1]
                        time1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S,%f")
                        time2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S,%f")
                        time_diff = (time2 - time1).total_seconds()/60
                        time_diff = round(time_diff, 5)
                        row = [log_message, start_time.replace(',', '.'), end_time.replace(',', '.'), time_diff]
                        self.table.append(row)
                        break;
    
    ## get the address of a log file
    def get_path(self):
        path = askopenfilename()
        return path
    
    ## show the data to download
    def display_data(self):
        path = self.get_path()
        self.get_data(path)
        self.filename = path.split('/')[-1]
        self.filename = self.filename[:len(self.filename)-4]
        for i in self.listBox.get_children():
            self.listBox.delete(i)
        self.window.update()
        for line in self.table:
            self.listBox.insert("", "end", values=line)
    
    ## get the address to store the csv file
    def get_download_dir(self):
        folder = askdirectory()
        return folder
    
    ## write the data to the csv file
    def write_data(self):
        path = self.get_download_dir()
        path = path+'/'+self.filename+'.csv'
        with open(path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',quoting = csv.QUOTE_NONE)
            csvwriter.writerow(["Log Message", "Start Time", "End Time", "Time Diff"])
            for line in self.table:
                csvwriter.writerow(line)

window = Tk() 
gui = APP_GUI(window)
gui.set_init_window()
window.mainloop() 
