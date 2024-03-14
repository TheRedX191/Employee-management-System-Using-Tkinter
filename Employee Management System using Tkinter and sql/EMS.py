import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import requests
import matplotlib.pyplot as plt

#*******Fuctions********
def close():
    if askyesno("Exit","Are you sure you want to exit? "):
        mw.destroy()
def f1():
    mw.withdraw()
    aw.deiconify()

def f2():
    aw.withdraw()
    mw.deiconify()

def f3():
    mw.withdraw()
    uw.deiconify()

def f4():
    uw.withdraw()
    mw.deiconify()

def f5():
    mw.withdraw()
    dw.deiconify()

def f6():
    dw.withdraw()
    mw.deiconify()

def f7():
    mw.withdraw()
    vw.deiconify()
    vw_st_data.config(state=NORMAL)
    vw_st_data.delete(1.0,END)
    con = None
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql = "select * from emp"
        cursor.execute(sql)
        data = cursor.fetchall()
        info = ""
        for d in data:
            info = info +"EMP ID: "+str(d[0])+"\nNAME: "+str(d[1])+"\nAGE: "+str(d[2])+"\nPHN NO: "+str(d[3])+"\nSALARY: "+str(d[4])+"\n------------------------------\n"
        vw_st_data.insert(INSERT,info)
        vw_st_data.config(state=DISABLED)
    except Exception as e:
        showerror("Issue",e)
    finally:
        if con is not None:
            con.close()

def f8():
    vw.withdraw()
    mw.deiconify()

def add():
    con = None
    sp = "!@#$%^&*()_+-{}|[]:;'<>/."
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        #cursor.execute("drop table emp")
        #.execute("create table emp (id int primary key, name text,age int,phn int, salary int)")
        sql = "insert into emp values('%d','%s','%d','%d','%d');"
        try:
            eid = int(aw_ent_eid.get())
            if eid<1:
                raise Exception("ID should not be 0 or negative")
        except ValueError:
            showerror("Issue","Invalid ID")
        except Exception as e:
            showerror("Issue",e)
            return
        try:
            name = aw_ent_ename.get()
            if len(name)<2:
                raise Exception("Length of name should be more than 2 alphabets")
            for i in name:
                if i.isnumeric():
                    raise Exception("Name should only contain alphabates")
                elif i in sp:
                    raise Exception("Name should not contain Special Characters")
        except Exception as e:
            showerror("Issue",e)
            return
        try:
            age = int(aw_ent_age.get())
            if age<18:
                raise Exception("Employee is below 18 years ")
            elif age>75 :
                raise Exception("Employee is too old")
        except ValueError:
            showerror("Issue","Invalid Age")
        except Exception as e:
            showerror("Issue",e)
            return
        try:
            phn = int(aw_ent_phn.get())
            cursor.execute("select count(*) from emp where phn = ?",(phn,))
            r = cursor.fetchone()[0]
            if len(str(phn))<10:
                raise Exception("Phone Number must be of 10 digits")
            elif len(str(phn))>11:
                raise Exception("Phone Number must be of 10 digits")
            elif r>0:
                raise Exception("Phone No is already present")
        except ValueError:
            showerror("Issue","Invalid Phone Number")
        except Exception as e:
            showerror("Issue",e)
            return
        try:
            sal = int(aw_ent_salary.get())
            if sal<8000:
                raise Exception("Salary is too low or negative")
        except Exception as e:
                showerror("Issue",e)
                return
        cursor.execute(sql %(eid,name,age,phn,sal))
        con.commit()
        showinfo("Success","info Saved")
    except Exception as e:
        if type(e).__name__ =="IntegrityError":
            showerror("Issue","Id is already present")
        else:
            showerror("Issue",e)
    finally:
        if con is not None:
            con.close()
        aw_ent_eid.delete(0,END)
        aw_ent_ename.delete(0,END)
        aw_ent_age.delete(0,END)
        aw_ent_phn.delete(0,END)
        aw_ent_salary.delete(0,END)
        aw_ent_eid.focus()

def update():
    con = None
    sp = "!@#$%^&*()_+-{}|[]:;'<>/."
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql = "UPDATE emp SET name = '%s',age='%d',phn='%d',salary='%d' WHERE id = '%d'" 
        try:
            eid = int(uw_ent_eid.get())
            if eid<0:
                raise Exception("ID should not be 0 or negative")
        except ValueError:
            showerror("Issue","Invalid ID")
        except Exception as e:
            showerror("Issue",e)
        try:
            name = uw_ent_ename.get()
            if len(name)<2:
                raise Exception("Invalid Name")
            for i in name:
                if i.isnumeric():
                    raise Exception("Name should only contain alphabates")
                elif i in sp:
                    raise Exception("Name should not contain Special Characters")
        except Exception as e:
            showerror("Issue",e)
            return
        try:
            age = int(uw_ent_age.get())
            if age<18:
                raise Exception("Employee is below 18 yrs ")
            elif age>75 :
                raise Exception("Employee is too old")
        except ValueError:
            showerror("Issue","Invalid Age")
        except Exception as e:
            showerror("Issue",e)
            return
        try:
            phn = int(uw_ent_phn.get())
            cursor.execute("select count(*) from emp where phn = ?",(phn,))
            r = cursor.fetchone()[0]
            if len(str(phn))<10:
                raise Exception("Phone Number must be of 10 digits")
            elif len(str(phn))>11:
                raise Exception("Phone Number must be of 10 digits")
            elif r>1:
                raise Exception("Phone No is already present")
        except ValueError:
            showerror("Issue","Invalid Phone Number")
        except Exception as e:
            showerror("Issue",e)
            return
        try:
            sal = int(uw_ent_salary.get())
            if sal<8000:
                raise Exception("Salary is too low or negative")
            else:
                cursor.execute("select id from emp where id = ?",(eid,))
                r = cursor.fetchone()
                if r is None:
                    raise Exception("Id does not Exist ")
        except ValueError:
            showerror("Issue","Invalid Salary")
        except Exception as e:
            showerror("Issue",e)
            return
        cursor.execute(sql %(name,age,phn,sal,eid))
        con.commit()
        showinfo("Success","Info Updated")
    except Exception as e:
        showerror("Issue",e)
    finally:
        if con is not None:
            con.close()
        uw_ent_eid.delete(0,END)
        uw_ent_ename.delete(0,END)
        uw_ent_age.delete(0,END)
        uw_ent_phn.delete(0,END)
        uw_ent_salary.delete(0,END)
        uw_ent_eid.focus()

def delete():
    con = None  
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql = "DELETE FROM emp WHERE id = '%d'"
        try:
            eid = int(dw_ent_eid.get())
            cursor.execute("select id from emp where id = ?",(eid,))
            r = cursor.fetchone()
            if r is None:
                raise Exception("ID does not exist")
            if eid<1:
                raise Exception("ID should not be 0 or negative")
            else:
                cursor.execute(sql %(eid))
                con.commit()
            showinfo("Success","Info Deleted")
        except ValueError:
            showerror("issue","Invalid ID")
        except Exception as e:
            showerror("Issue",e)
    finally:
        if con is not None:
            con.close()
        dw_ent_eid.delete(0,END)
        dw_ent_eid.focus()
    
def search():
        con  = None
        try:
            con = connect("ems.db")
            cursor = con.cursor()
            sql = "select * from emp WHERE id = '%d'"
            try:
                eid = int(vw_e_search.get())
                if eid<1:
                    raise Exception("ID shuld not be 0 or Negative")
                else:
                    cursor.execute("SELECt * FROM emp WHERE id=?",(eid,))
                    r = cursor.fetchone()
                    # print(r)
                    if r is None:
                        raise Exception("ID does not Exist")
                    else:
                        cursor.execute(sql %(eid))
                        srch_data = cursor.fetchmany()
                        # print("data:",srch_data)
                        srch_info = " "
                        for d in srch_data:
                            # print(d)
                            srch_info = srch_info +"EMP ID: "+str(d[0])+"\nNAME: "+str(d[1])+"\nAGE: "+str(d[2])+"\nPHN NO: "+str(d[3])+"\nSALARY: "+str(d[4])+"\n------------------------------\n"
                        vw_st_data.config(state=NORMAL)
                        vw_st_data.delete(1.0,END)
                        vw_st_data.insert(INSERT,srch_info)
                        vw_st_data.config(state=DISABLED)
            except Exception as e:
                showerror("Issue",e)
        except Exception as e:
            showerror("Issue",e)
        finally:
            if con is not None:
                con.close()
            vw_e_search.delete(0,END)
def chart():
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

#*************temp and loc**************
try:
    wa="https://ipinfo.io/"
    res = requests.get(wa)
    data = res.json()
    city_name = data["city"]
    a1 = "https://api.openweathermap.org/data/2.5/weather"
    a2 = "?q="+city_name
    a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
    a4 = "&units="+"metric"
    wa2 = a1+a2+a3+a4
    res1 = requests.get(wa2)
    data1 =  res1.json()
    tempr = data1["main"]["temp"]
except Exception as e:
    showerror("Issue",e)

#**********Main_WINDOW********************
mw = tk.Tk()
mw.title("Employee Management System")
mw.geometry("850x850+20+20")
mw.configure(bg="linen")
f=("Times",20,"bold")
f01=("Times",25,"bold")
fo1 =("Times",15,"bold")
mw_lab_title = Label(mw,text="EMPLOYEE MANAGEMENT SYSTEM",font=f01,bg="linen")
mw_btn_add = Button(mw, text="ADD", font=f, width=10, bg="burlywood",command=f1)
mw_btn_update = Button(mw, text="UPDATE", font=f, width=10, bg="burlywood", command=f3)
mw_btn_view = Button(mw, text="VIEW", font=f, width=10,bg="burlywood",command=f7)
mw_btn_delete = Button(mw, text="DELETE", font=f, width=10,bg="burlywood", command=f5)
mw_btn_chart = Button(mw, text="CHART", font=f, width=10,bg="burlywood",command=chart)
mw_loc_lab = Label(mw,text="Location: "+city_name, font=f, bg="linen")
mw_temp_lab = Label(mw,text="Temperature: "+str(tempr)+"°C", font=f, bg="linen")
mw_lab_title.pack(pady=50)
mw_btn_add.pack(pady=20)
mw_btn_update.pack(pady=20)
mw_btn_view.pack(pady=20)
mw_btn_delete.pack(pady=20)
mw_btn_chart.pack(pady=20)
mw_loc_lab.place(x=30,y=790)
mw_temp_lab.place(x=480,y=790)
mw.protocol("WM_DELETE_WINDOW",close)

#*************ADD_WINDOW********************
aw = Toplevel(mw)
aw.title("Add Employee")
aw.geometry("850x850+20+20")
aw.configure(bg="linen")
aw_lab_eid = Label(aw, text="Enter Employee ID ", font=f, bg="linen")
aw_ent_eid = Entry(aw,font=f)
aw_lab_ename = Label(aw, text="Enter Name ", font=f,bg="linen")
aw_ent_ename = Entry(aw,font=f)
aw_lab_age = Label(aw, text="Enter age ", font=f,bg="linen")
aw_ent_age = Entry(aw,font=f)
aw_lab_phn = Label(aw, text="Enter Phone No ", font=f,bg="linen")
aw_ent_phn = Entry(aw,font=f)
aw_lab_salary = Label(aw, text="Enter Employee Salary ", font=f, bg="linen")
aw_ent_salary = Entry(aw,font=f)
aw_btn_save = Button(aw,text="Save", font=f, bg="burlywood", command=add)
aw_btn_back = Button(aw,text="Back", font=f, bg="burlywood", command=f2)
aw_lab_eid.pack(pady=10)
aw_ent_eid.pack(pady=10)
aw_lab_ename.pack(pady=10)
aw_ent_ename.pack(pady=10)
aw_lab_age.pack(pady=10)
aw_ent_age.pack(pady=10)
aw_lab_phn.pack(pady=10)
aw_ent_phn.pack(pady=10)
aw_lab_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)
aw.protocol("WM_DELETE_WINDOW",close)
aw.withdraw()

#************UPDATE_WINDOW*******************
uw = Toplevel(mw)
uw.title("Update Employee")
uw.geometry("850x850+20+20")
uw.configure(bg="linen")
uw_lab_eid = Label(uw, text="Enter Employee ID ", font=f, bg="linen")
uw_ent_eid = Entry(uw,font=f)
uw_lab_ename = Label(uw, text="Enter Name ", font=f, bg="linen")
uw_ent_ename = Entry(uw,font=f)
uw_lab_age = Label(uw, text="Enter age ", font=f,bg="linen")
uw_ent_age = Entry(uw,font=f)
uw_lab_phn = Label(uw, text="Enter Phone No ", font=f,bg="linen")
uw_ent_phn = Entry(uw,font=f)
uw_lab_salary = Label(uw, text="Enter Employee Salary ", font=f, bg="linen")
uw_ent_salary = Entry(uw,font=f)
uw_btn_save = Button(uw,text="Update", font=f, bg="burlywood", command=update)
uw_btn_back = Button(uw,text="Back",width=6, font=f, bg="burlywood", command=f4)
uw_lab_eid.pack(pady=10)
uw_ent_eid.pack(pady=10)
uw_lab_ename.pack(pady=10)
uw_ent_ename.pack(pady=10)
uw_lab_age.pack(pady=10)
uw_ent_age.pack(pady=10)
uw_lab_phn.pack(pady=10)
uw_ent_phn.pack(pady=10)
uw_lab_salary.pack(pady=10)
uw_ent_salary.pack(pady=10)
uw_btn_save.pack(pady=10)
uw_btn_back.pack(pady=10)
uw.protocol("WM_DELETE_WINDOW",close)
uw.withdraw()

#***********VIEW_WINDOW*****************
vw = Toplevel(mw)
vw.title("View Employee")
vw.geometry("850x850+20+20")
vw.configure(bg="linen")
vw_lab_srch = Label(vw,text = "Search by ID",font = fo1,bg = "linen")
vw_e_search = Entry(vw,font = f)
vw_btn_srch = Button(vw,text="Search",font=f,bg="burlywood",command=search)
vw_st_data = ScrolledText(vw, width=30, height=15, font= f,bg="azure")
vw_btn_back = Button(vw,text="Back", font=f, bg="burlywood",command=f8)
vw_lab_srch.pack(pady =10)
vw_e_search.pack(pady=10)
vw_btn_srch.place(x = 600,y = 25)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)
vw.protocol("WM_DELETE_WINDOW",close)
vw.withdraw()

#*************DELETE_WINDOW*********************
dw = Toplevel(mw)
dw.title("Delete Employee")
dw.geometry("850x850+20+20")
dw.configure(bg="linen")
dw_lab_eid = Label(dw,text="Enter Employee ID", font=f, bg="linen")
dw_ent_eid = Entry(dw,font=f)
dw_btn_save = Button(dw, text="Save", font=f, bg="burlywood",command=delete)
dw_btn_back = Button(dw, text="Back", font=f, bg="burlywood",command=f6)
dw_lab_eid.pack(pady=20)
dw_ent_eid.pack(pady=20)
dw_btn_save.pack(pady=20)
dw_btn_back.pack(pady=20)
dw.protocol("WM_DELETE_WINDOW",close)
dw.withdraw()

mw.mainloop()