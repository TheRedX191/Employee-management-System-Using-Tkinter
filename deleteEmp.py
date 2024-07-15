import tkinter as tk
from tkinter import *
from tkinter.messagebox import askyesno, showinfo, showerror
from sqlite3 import connect

def create_delete_window(main_window):
    main_window.withdraw()
    
    def mainWindow():
        dw.withdraw()
        main_window.deiconify()
    
    def close_delete_window():
        if askyesno("Exit", "Are you sure you want to exit?"):
            main_window.destroy()

    def delete():
        con = None
        try:
            con = connect("ems.db")
            cursor = con.cursor()
            sql = "delete from emp where eid = '%d';"
            try:
                eid = int(dw_ent_eid.get())
                if eid < 1:
                    raise Exception("ID should not be 0 or negative")
            except ValueError:
                showerror("Issue", "Invalid ID")
                return
            except Exception as e:
                showerror("Issue", e)
                return

            cursor.execute(sql % eid)
            if cursor.rowcount == 0:
                raise Exception("Employee ID not found")
            con.commit()
            showinfo("Success", "Info Deleted")
        except Exception as e:
            showerror("Issue", e)
        finally:
            if con is not None:
                con.close()
            dw_ent_eid.delete(0, END)
            dw_ent_eid.focus()

    dw = Toplevel(main_window)
    dw.title("Delete Employee")
    dw.geometry("1920x1080+0+0")
    dw.configure(bg="#222831")
    f = ("Times", 20, "bold")

    dw_lab_eid = Label(dw, text="Enter Employee ID ", font=f, bg="#222831")
    dw_ent_eid = Entry(dw, font=f)
    dw_btn_delete = Button(dw, text="Delete", font=f, bg="#9B3922",fg="#EEEEEE", command=delete)
    dw_btn_back = Button(dw, text="Back", font=f, bg="#9B3922",fg="#EEEEEE", command=mainWindow)

    dw_lab_eid.pack(pady=10)
    dw_ent_eid.pack(pady=10)
    dw_btn_delete.pack(pady=10)
    dw_btn_back.pack(pady=10)

    dw.protocol("WM_DELETE_WINDOW", close_delete_window)
    dw.withdraw()
    main_window.withdraw()
    dw.deiconify()
