from sqlite3 import connect
import tkinter as tk
from tkinter import *
from tkinter.messagebox import askyesno, showerror
from matplotlib import pyplot as plt
import requests
from addEmp import create_add_window
from viewEmp import create_view_window
from updateEmp import create_update_window
from deleteEmp import create_delete_window
from showChart import create_chart_window

#*******Functions********
def close():
    if askyesno("Exit", "Are you sure you want to exit?"):
        mw.destroy()

def get_weather_and_location():
    try:
        wa = "https://ipinfo.io/"
        res = requests.get(wa)
        data = res.json()
        city_name = data["city"]
        a1 = "https://api.openweathermap.org/data/2.5/weather"
        a2 = "?q=" + city_name
        a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
        a4 = "&units=" + "metric"
        wa2 = a1 + a2 + a3 + a4
        res1 = requests.get(wa2)
        data1 = res1.json()
        tempr = data1["main"]["temp"]
        return city_name, tempr
    except Exception as e:
        showerror("Issue", e)
        return None, None
    
def plot_chart():
    mw.withdraw()
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
        mw.deiconify()
    finally:
        if con is not None:
            con.close()
        mw.deiconify()

#**********Main_WINDOW********************
mw = tk.Tk()
mw.title("Employee Management System")
mw.geometry("1920x1080")
mw.configure(bg="#222831")
f = ("Times", 20, "bold")
f01 = ("Times", 25, "bold")

city_name, tempr = get_weather_and_location()

mw_lab_title = Label(mw, text="EMPLOYEE MANAGEMENT SYSTEM", font=f01,fg="#EEEEEE", bg="#222831")
mw_btn_add = Button(mw, text="ADD", font=f, width=10, bg="#9B3922", fg="#EEEEEE",command= lambda: create_add_window(mw))
mw_btn_update = Button(mw, text="UPDATE", font=f, width=10, bg="#9B3922",fg="#EEEEEE", command=lambda: create_update_window(mw))
mw_btn_view = Button(mw, text="VIEW", font=f, width=10, bg="#9B3922", fg="#EEEEEE",command=lambda: create_view_window(mw))
mw_btn_delete = Button(mw, text="DELETE", font=f, width=10, bg="#9B3922",fg="#EEEEEE", command=lambda: create_delete_window(mw))
mw_btn_chart = Button(mw, text="CHART", font=f, width=10, bg="#9B3922", fg="#EEEEEE",command= lambda:create_chart_window(mw))

if city_name and tempr:
    mw_loc_lab = Label(mw, text="Location: " + city_name, font=f, bg="#222831",fg="#EEEEEE")
    mw_temp_lab = Label(mw, text="Temperature: " + str(tempr) + "°C", font=f, bg="#222831",fg="#EEEEEE")
    mw_loc_lab.place(x=20, y=20)
    mw_temp_lab.place(x=1600, y=20)

mw_lab_title.pack(pady=80)
mw_btn_add.pack(pady=20)
mw_btn_update.pack(pady=20)
mw_btn_view.pack(pady=20)
mw_btn_delete.pack(pady=20)
mw_btn_chart.pack(pady=20)

mw.protocol("WM_DELETE_WINDOW", close)
mw.mainloop()
