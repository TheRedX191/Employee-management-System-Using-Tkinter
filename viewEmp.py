import tkinter as tk
from tkinter import *
from tkinter.messagebox import askyesno, showinfo, showerror
from tkinter.scrolledtext import ScrolledText
from sqlite3 import connect

def create_view_window(main_window):
    main_window.withdraw()
    
    def mainWindow():
        vw.withdraw()
        main_window.deiconify()
    
    def close_view_window():
        if askyesno("Exit", "Are you sure you want to exit?"):
            main_window.destroy()

    def view():
        vw_st_data.config(state=NORMAL)
        vw_st_data.delete(1.0, END)
        con = None
        try:
            con = connect("ems.db")
            cursor = con.cursor()
            sql = "select * from emp"
            cursor.execute(sql)
            data = cursor.fetchall()
            info = ""
            for d in data:
                info += f"ID : {d[0]}\nName : {d[1]}\nAge : {d[2]}\nPhone Number : {d[3]}\nSalary : {d[4]}\n" + ("*"*20) + "\n"
            vw_st_data.insert(INSERT, info)
            vw_st_data.config(state=DISABLED)
        except Exception as e:
            showerror("Issue", e)
        finally:
            if con is not None:
                con.close()

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
                            srch_info += f"ID : {d[0]}\nName : {d[1]}\nAge : {d[2]}\nPhone Number : {d[3]}\nSalary : {d[4]}\n" + ("*"*20) + "\n"
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

    vw = Toplevel(main_window)
    vw.title("View Employee")
    vw.geometry("1920x1080+0+0")
    vw.configure(bg="#222831")
    f = ("Times", 20, "bold")
    fo1 =("Times",15,"bold")
    vw_lab_srch = Label(vw,text = "Search by ID",font = fo1,bg = "#222831",fg="#EEEEEE")
    vw_e_search = Entry(vw,font = f)
    vw_btn_srch = Button(vw,text="Search",font=f,fg="#EEEEEE",bg="#9B3922",command=search,height=2)
    vw_st_data = ScrolledText(vw, width=35, height=20, font=f)
    vw_btn_back = Button(vw, text="Back", font=f, fg="#EEEEEE",bg="#9B3922", command=mainWindow)

    vw_lab_srch.place(x = 680,y = 35)
    vw_e_search.place(x = 840,y = 35)
    vw_btn_srch.place(x = 1200,y = 35)
    vw_st_data.pack(pady=120)
    vw_btn_back.pack(pady=10)

    vw.protocol("WM_DELETE_WINDOW", close_view_window)
    view()

    vw.withdraw()
    main_window.withdraw()
    vw.deiconify()

# # Example main window for testing
# def main():
#     root = tk.Tk()
#     root.title("Main Window")
#     root.geometry("300x200")

#     btn_view = Button(root, text="View Employees", command=lambda: create_view_window(root))
#     btn_view.pack(pady=20)

#     root.mainloop()

# if __name__ == "__main__":
#     main()
