import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showinfo, showerror
from sqlite3 import connect

def create_chart_window(main_window):
    main_window.deiconify()
    main_window.withdraw()
    def plot_chart():   
        con = None
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql = "select name, salary from emp group by salary order by salary desc limit 5;"
        cursor.execute(sql)
        data = cursor.fetchall()
        con.commit()
        ids=[]
        sal=[]
        i,j=0,0
        while(i<5):
            ids.append(data[i][0])
            i+=1
        while(j<5):
            sal.append(data[j][1])
            j+=1
        plt.bar(ids,sal,color="#CBC3E9")
        plt.xlabel("EMP Name")
        plt.ylabel("SALARY")
        plt.title("Top five Employees salary chart")
        plt.show()
    except Exception as e:
        showerror("Issue",e)
        plt.show(False)
        main_window.deiconify()
    finally:
        if con is not None:
            con.close()
        main_window.deiconify()

    plot_chart()
