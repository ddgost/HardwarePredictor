import time
from tkinter import *
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import psutil as ps
from sklearn.linear_model import LinearRegression

canRun = True


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def createCSVFile(self):
        global canRun
        canRun = True
        self.filename = time.strftime("%Y%m%d%H%M")
        statsTime = time.strftime("%Y-%m-%d %H:%M:%S")
        Cpu_percent = ps.cpu_percent(interval=1)
        Memory_percent = ps.virtual_memory().percent
        Disk_percent = ps.disk_usage("/").percent
        file = open(self.filename + ".csv", 'w+')
        file.write("Date,Cpu Usage,Memory Usage,Disk Usage" + "\n")
        file.write(statsTime + ',' + str(Cpu_percent) + ',' + str(Memory_percent) + ',' + str(Disk_percent) + "\n")
        file.close
        self.getData()

    def getData(self):
        if canRun is True:
            statsTime = time.strftime("%Y-%m-%d %H:%M:%S")
            Cpu_percent = ps.cpu_percent(interval=1)
            Memory_percent = ps.virtual_memory().percent
            Disk_percent = ps.disk_usage("/").percent
            stats = open(self.filename + ".csv", 'a')
            stats.write(statsTime + ',' + str(Cpu_percent) + ',' + str(Memory_percent) + ',' + str(Disk_percent) + "\n")
            stats.close()
            self.after(1.8E+6, self.getData)
            # 30 min is 1.8E+6
        else:
            return

    def stop(self):
        global canRun
        canRun = False
        self.getData()

    def loadData(self):
        Tk().withdraw()
        self.filename = askopenfilename()
        self.filename = os.path.splitext(self.filename)[0]
        file = open(self.filename + ".csv", 'r+')

    def showData(self):
        tableWindow = Toplevel(root)
        self.pack(fill=BOTH, expand=1)
        df = pd.read_csv(self.filename + ".csv")
        text = Text(tableWindow)
        text.insert(END, str(df))
        text.pack()

    def generateCharts(self):
        df = pd.read_csv(self.filename + ".csv")
        df['Date'] = pd.to_datetime(df.Date)
        date = df[['Date']]
        numericDate = df[['Date']] = pd.to_numeric(df.Date)
        cpu = df[["Cpu Usage"]]
        mem = df[["Memory Usage"]]
        disc = df[["Disk Usage"]]
        predict_data = df[["Date"]]

        solution_cpu = LinearRegression()
        solution_cpu.fit(date, cpu)
        predicted_cpu_usage = pd.DataFrame(solution_cpu.predict(predict_data))

        solution_mem = LinearRegression()
        solution_mem.fit(date, mem)
        predicted_memory_usage = pd.DataFrame(solution_mem.predict(predict_data))

        solution_disc = LinearRegression()
        solution_disc.fit(date, cpu)
        predicted_disc_usage = pd.DataFrame(solution_disc.predict(predict_data))

        plt.rcParams['figure.figsize'] = [11, 11]

        plt.subplot(221)
        plt.plot_date(date, cpu, color='black')
        plt.plot(date, cpu, color="red")
        plt.plot(date, predicted_cpu_usage, color='green')
        plt.title("Cpu Usage with predictions obtained by linear regression")
        plt.xlabel("Date")
        plt.ylabel("Cpu Usage (%)")

        plt.subplot(222)
        plt.plot_date(date, mem, color='black')
        plt.plot(date, mem, color="orange")
        plt.plot(date, predicted_memory_usage, color='purple')
        plt.title("Memory Usage with predictions obtained by linear regression")
        plt.xlabel("Date")
        plt.ylabel("Memory Usage (%)")

        plt.subplot(223)
        plt.plot_date(date, disc, color='black')
        plt.plot(date, disc, color="pink")
        plt.plot(date, predicted_disc_usage, color='blue')
        plt.title("Disc C:\ Usage with predictions obtained by linear regression")
        plt.xlabel("Date")
        plt.ylabel("Disc C:\ Usage (%)")

        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, hspace=0.25, wspace=0.35)
        plt.size = (10, 5)
        plt.show()

    def init_window(self):
        self.master.title("Hardware Predictor")
        self.pack(fill=BOTH, expand=1)

        startButton = Button(self, text="Start", bg="green", command=self.createCSVFile).grid(row=0, column=0)

        stopButton = Button(self, text="Stop", bg="red", command=self.stop).grid(row=0, column=2)

        loadDataButton = Button(self, text="Load Data", command=self.loadData).grid(row=1, column=1)

        showDataButton = Button(self, text="Show data", command=self.showData).grid(row=2, column=0)

        generateChartsButton = Button(self, text="Plot charts", command=self.generateCharts).grid(row=2, column=2)


root = Tk()
app = Window(root)
root.geometry("200x100")
root.mainloop()
