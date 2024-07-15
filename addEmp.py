import tkinter as tk
from tkinter import *
from tkinter.messagebox import askyesno, showinfo, showerror
from sqlite3 import connect

def create_add_window(main_window):
    main_window.withdraw()

    def mainWindow():
        aw.withdraw()
        main_window.deiconify()
        
    def close_add_window():
         if askyesno("Exit", "Are you sure you want to exit?"):
            main_window.destroy()

    def add():
        con = None
        sp = "!@#$%^&*()_+-{}|[]:;'<>/."
        try:
            con = connect("ems.db")
            cursor = con.cursor()
            sql = "insert into emp values('%d','%s','%d','%d','%d');"
            try:
                eid = int(aw_ent_eid.get())
                if eid < 1:
                    raise Exception("ID should not be 0 or negative")
            except ValueError:
                showerror("Issue", "Invalid ID")
                return
            except Exception as e:
                showerror("Issue", e)
                return
            try:
                name = aw_ent_ename.get()
                if len(name) < 2:
                    raise Exception("Length of name should be more than 2 alphabets")
                for i in name:
                    if i.isnumeric():
                        raise Exception("Name should only contain alphabets")
                    elif i in sp:
                        raise Exception("Name should not contain Special Characters")
            except Exception as e:
                showerror("Issue", e)
                return
            try:
                age = int(aw_ent_age.get())
                if age < 18:
                    raise Exception("Employee is below 18 years")
                elif age > 75:
                    raise Exception("Employee is too old")
            except ValueError:
                showerror("Issue", "Invalid Age")
                return
            except Exception as e:
                showerror("Issue", e)
                return
            try:
                phn = int(aw_ent_phn.get())
                cursor.execute("select count(*) from emp where phn = ?", (phn,))
                r = cursor.fetchone()[0]
                if len(str(phn)) < 10 or len(str(phn)) > 11:
                    raise Exception("Phone Number must be of 10 digits")
                elif r > 0:
                    raise Exception("Phone No is already present")
            except ValueError:
                showerror("Issue", "Invalid Phone Number")
                return
            except Exception as e:
                showerror("Issue", e)
                return
            try:
                sal = int(aw_ent_salary.get())
                if sal < 8000:
                    raise Exception("Salary is too low or negative")
            except ValueError:
                showerror("Issue", "Invalid Salary")
                return
            except Exception as e:
                showerror("Issue", e)
                return

            cursor.execute(sql % (eid, name, age, phn, sal))
            con.commit()
            showinfo("Success", "Info Saved")
        except Exception as e:
            if type(e).__name__ == "IntegrityError":
                showerror("Issue", "ID is already present")
            else:
                showerror("Issue", e)
        finally:
            if con is not None:
                con.close()
            aw_ent_eid.delete(0, END)
            aw_ent_ename.delete(0, END)
            aw_ent_age.delete(0, END)
            aw_ent_phn.delete(0, END)
            aw_ent_salary.delete(0, END)
            aw_ent_eid.focus()

    aw = Toplevel(main_window)
    aw.title("Add Employee")
    aw.geometry("1920x1080+0+0")
    aw.configure(bg="#222831")
    f = ("Times", 20, "bold")
    f01 = ("Times", 25, "bold")
    aw_lab_title = Label(aw,text="ADD EMPLOYEE DETAILS",font=f01,fg="#EEEEEE", bg="#222831")
    aw_lab_eid = Label(aw, text="Enter Employee ID ", font=f,fg="#EEEEEE", bg="#222831")
    aw_ent_eid = Entry(aw, font=f)
    aw_lab_ename = Label(aw, text="Enter Name ", font=f,fg="#EEEEEE", bg="#222831")
    aw_ent_ename = Entry(aw, font=f)
    aw_lab_age = Label(aw, text="Enter age ", font=f,fg="#EEEEEE", bg="#222831")
    aw_ent_age = Entry(aw, font=f)
    aw_lab_phn = Label(aw, text="Enter Phone No ", font=f,fg="#EEEEEE", bg="#222831")
    aw_ent_phn = Entry(aw, font=f)
    aw_lab_salary = Label(aw, text="Enter Employee Salary ", fg="#EEEEEE",font=f, bg="#222831")
    aw_ent_salary = Entry(aw, font=f)
    aw_btn_save = Button(aw, text="Save", font=f,fg="#EEEEEE", bg="#9B3922", command=add)
    aw_btn_back = Button(aw, text="Back", font=f,fg="#EEEEEE", bg="#9B3922", command=mainWindow)

    aw_lab_title.pack(pady=50)
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

    aw.protocol("WM_DELETE_WINDOW", close_add_window)
    aw.withdraw()
    # main_window.withdraw()
    aw.deiconify()
