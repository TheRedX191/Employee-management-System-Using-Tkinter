import tkinter as tk
from tkinter import *
from tkinter.messagebox import askyesno, showinfo, showerror
from sqlite3 import connect

def create_update_window(main_window):
    main_window.withdraw()
    
    def mainWindow():
        uw.withdraw()
        main_window.deiconify()
    
    def close_update_window():
        if askyesno("Exit", "Are you sure you want to exit?"):
            main_window.destroy()
   

    def update():
        con = None
        sp = "!@#$%^&*()_+-{}|[]:;'<>/."
        try:
            con = connect("ems.db")
            cursor = con.cursor()
            sql = "update emp set ename = '%s', age = '%d', phn = '%d', salary = '%d' where eid = '%d';"
            try:
                eid = int(uw_ent_eid.get())
                if eid < 1:
                    raise Exception("ID should not be 0 or negative")
            except ValueError:
                showerror("Issue", "Invalid ID")
                return
            except Exception as e:
                showerror("Issue", e)
                return
            try:
                name = uw_ent_ename.get()
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
                age = int(uw_ent_age.get())
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
                phn = int(uw_ent_phn.get())
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
                sal = int(uw_ent_salary.get())
                if sal < 8000:
                    raise Exception("Salary is too low or negative")
            except ValueError:
                showerror("Issue", "Invalid Salary")
                return
            except Exception as e:
                showerror("Issue", e)
                return

            cursor.execute(sql % (name, age, phn, sal, eid))
            if cursor.rowcount == 0:
                raise Exception("Employee ID not found")
            con.commit()
            showinfo("Success", "Info Updated")
        except Exception as e:
            if type(e).__name__ == "IntegrityError":
                showerror("Issue", "ID is already present")
            else:
                showerror("Issue", e)
        finally:
            if con is not None:
                con.close()
            uw_ent_eid.delete(0, END)
            uw_ent_ename.delete(0, END)
            uw_ent_age.delete(0, END)
            uw_ent_phn.delete(0, END)
            uw_ent_salary.delete(0, END)
            uw_ent_eid.focus()

    uw = Toplevel(main_window)
    uw.title("Update Employee")
    uw.geometry("1920x1080+0+0")
    uw.configure(bg="#222831")
    f = ("Times", 20, "bold")

    uw_lab_eid = Label(uw, text="Enter Employee ID ", font=f,fg="#EEEEEE", bg="#222831")
    uw_ent_eid = Entry(uw, font=f)
    uw_lab_ename = Label(uw, text="Enter Name ", font=f, bg="#222831")
    uw_ent_ename = Entry(uw, font=f)
    uw_lab_age = Label(uw, text="Enter age ", font=f, bg="#222831")
    uw_ent_age = Entry(uw, font=f)
    uw_lab_phn = Label(uw, text="Enter Phone No ", font=f, bg="#222831")
    uw_ent_phn = Entry(uw, font=f)
    uw_lab_salary = Label(uw, text="Enter Employee Salary ", font=f, bg="#222831")
    uw_ent_salary = Entry(uw, font=f)
    uw_btn_save = Button(uw, text="Update", font=f, bg="#9B3922", command=update)
    uw_btn_back = Button(uw, text="Back", font=f, bg="#9B3922", command=mainWindow)

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

    uw.protocol("WM_DELETE_WINDOW", close_update_window)
    uw.withdraw()
    main_window.withdraw()
    uw.deiconify()
