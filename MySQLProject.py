from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import *
import mysql.connector


# ========================================================================= Splash Window (Root) =========================================================================
def main_window():
    splash_root.destroy()
    root.deiconify()


# ========================================================================= Main Window (CalculateBMI) =========================================================================

def f1():
    root.withdraw()
    Calculate.deiconify()


# ========================================================================= Main Window (History) =========================================================================

def f2():
    root.withdraw()
    History.deiconify()
    con = mysql.connector.connect(host="localhost", user="root", password="abc456", database="bmicalc")
    try:
        cursor = con.cursor()
        sql = "select name, age, phone, gender, bmi, date from patient;"
        cursor.execute(sql)
        data = cursor.fetchall()
        info = " "
        for d in data:
            # print("rno ", d[0], "name", d[1], "marks", d[2])
            info = "\n**************************\n" + "Name= " + str(d[0]) + "\nAge= " + str(
                d[1]) + "\nPhone= " + str(
                d[2]) + "\nGender= " + str(d[3]) + "\nBMI= " + str(d[4])
            History_data.insert(INSERT, info)
    except Exception as e:
        showerror("Issue", "No such database or table exists!  " + str(e))
    finally:
        if con is not None:
            con.close()


# ========================================================================= Main Window (Export) =========================================================================

def f3():
    pass
    con = mysql.connector.connect(host="localhost", user="root", password="abc456", database="bmicalc")
    try:
        cursor = con.cursor()
        cursor.callproc('p3')
    except Exception as e:
        showerror("Issue", "No such database or table exists!  " + str(e))
    finally:
        if con is not None:
            con.close()


# ======================================================================== Calculate Tab (Convert) ========================================================================

def f4():
    Calculate.withdraw()
    Convert.deiconify()


# ======================================================================== Calculate Tab (Calculate) ========================================================================

def f5():
    con = None
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="abc456", database="bmicalc")
        name = entName.get()
        strAge = entAge.get()
        strPhone = entPhone.get()
        strHeight = entHeight.get()
        strWeight = entWeight.get()
        r = selection.get()
        if r == 1:
            gender = "Male"
        else:
            gender = "Female"
        if len(name) == 0:
            showerror("Empty Name", "Enter Valid Credentials!")
        elif name.isdigit():
            showerror("Invalid Name", "Name can only contain Alphabets!")
        elif len(strAge) == 0:
            showerror("Empty Age", "Enter Valid Credentials!")
        elif strAge.isalpha():
            showerror("Integer Only", "Enter Age in Numbers!")
        elif len(strPhone) == 0:
            showerror("Empty Phone Number", "Enter Valid Credentials!")
        elif strPhone.isalpha():
            showerror("Integer Only", "Enter Phone number in Numbers!")
        elif len(strHeight) == 0:
            showerror("Empty Height", "Enter Valid Credentials!")
        elif strHeight.isalpha():
            showerror("Invalid Height", "Enter a valid height!")
        elif len(strWeight) == 0:
            showerror("Empty Weight", "Enter Valid Credentials!")
        elif strWeight.isalpha():
            showerror("Invalid Height", "Enter a valid Weight!")
        else:
            height = float(strHeight)
            weight = float(strWeight)
            age = int(entAge.get())
            phone = int(entPhone.get())
            if age > 120:
                showerror("Invalid Age","Age cannot be negative! Neither can it be 0! Nor can it be more than 120 ")
            elif height < 0.63:
                showerror("Invalid Height", "Enter a valid height!")
            elif height > 2.72:
                showerror("Invalid Height", "Enter a valid height!")
            elif weight < 2.5:
                showerror("Invalid Weight", "Enter a valid Weight!")
            else:
                BMI = weight / (height ** 2)
                if BMI < 18.5:
                    showinfo("Underweight", "BMI: " + str(round(BMI, 2)) + "\n" + "You Are Really Skinny!")
                elif 18.5 < BMI < 25:
                    showinfo("Normal Weight", "BMI: " + str(round(BMI, 2)) + "\n" + "You Are Healthy!")
                elif 25 < BMI < 30:
                    showinfo("Overweight", "BMI: " + str(round(BMI, 2)) + "\n" + "You Are Fat!")
                else:
                    showinfo("Obese", "BMI: " + str(round(BMI, 2)) + "\n" + "You Are A Giant!")
                try:
                    cursor = con.cursor()
                    sql = "call p1('%s', '%d', '%d', '%s', '%d');"
                    cursor.execute(sql % (name, age, phone, gender, BMI))
                    con.commit()
                    showinfo("Success", "Record inserted")
                    args = ['@c']
                    result = cursor.callproc("p2", args)
                    lblCount.configure(text="Count = " + str(result[0]))
                except Exception as e:
                    showerror("SQL Error", str(e))
                    con.rollback()

    except Exception as e:
        showerror("SQL Error", str(e))
        con.rollback()
    finally:
        if con is not None:
            con.close()
    entName.focus()
    entName.delete(0, END)
    entAge.focus()
    entAge.delete(0, END)
    entPhone.focus()
    entPhone.delete(0, END)
    entHeight.focus()
    entHeight.delete(0, END)
    entWeight.focus()
    entWeight.delete(0, END)


# ======================================================================== Calculate Tab (Back) ========================================================================

def f6():
    Calculate.withdraw()
    root.deiconify()


# ========================================================================= Convert Tab (Convert) =========================================================================

def f7():
    try:
        strFeet=entFeet.get()
        strInch=entInches.get()
        feet = int(entFeet.get())
        inch = int(entInches.get())
        if len(strFeet) == 0:
            showerror("Empty Feet", "Provide valid details")
        elif feet < 1:
            showerror("Wrong Info", "Provide Non Negative Details")
        elif feet > 9:
            showerror("Wrong Info", "Provide valid details")
        if len(strInch) == 0:
            showerror("Empty Inch", "Provide valid details")
        elif inch < 0:
            showerror("Wrong Info", "Provide Non Negative Details")
        elif inch > 12:
            showerror("Wrong Info", "Provide valid details")
        else:
            res = (feet + (inch / 12)) / 3.281
            showinfo("Your Height in Meters", round(res, 3))
    except ValueError:
        showerror("Wrong Info", "Provide valid details")


# ========================================================================= Convert Tab (Back) =========================================================================

def f8():
    Convert.withdraw()
    Calculate.deiconify()


# ========================================================================= History Tab (Back) ==================================================================

def f9():
    History.withdraw()
    root.deiconify()


# ========================================================================= Date and Time =======================================================================
dt = datetime.now()
if dt.hour >= 5 | dt.hour <= 12:
    greet = "Good Morning"
elif dt.hour >= 12 | dt.hour <= 17:
    greet = "Good Afternoon"
else:
    greet = "Good Evening"


# ========================================================================= Main Window =========================================================================
root = ThemedTk(theme="arc")
root.title("BMI Calculator")
root.geometry("300x300+600+200")

lblTime = ttk.Label(root, text=dt)
lblGreet = ttk.Label(root, text=greet)
btnCalculateBMI = ttk.Button(root, text="Calculate BMI", width=15, command=f1)
btnHistory = ttk.Button(root, text="View History", width=15, command=f2)
btnExport = ttk.Button(root, text="Export Data", width=15, command=f3)
con = mysql.connector.connect(host="localhost", user="root", password="abc456", database="bmicalc")
cursor = con.cursor()
args = ['@c']
result = cursor.callproc("p2", args)
lblCount = ttk.Label(root, text="Count = " + str(result[0]))

lblTime.pack(pady=10)
lblGreet.pack(pady=2)
btnCalculateBMI.pack(pady=10)
btnHistory.pack(pady=10)
btnExport.pack(pady=10)
lblCount.pack(pady=10)

root.withdraw()

# ========================================================================= Splash Window =========================================================================

splash_root = Toplevel(root)
splash_root.title("BMI Calculator")
splash_root.geometry("300x300+600+200")
splash_label = ttk.Label(splash_root, text='BMI CALCULATOR', font=('Monaco', 22, 'bold'), foreground='#03a9f4')
splash_label.pack(pady=100)

splash_root.after(2000, main_window)
# ======================================================================== Calculate Tab ========================================================================

Calculate = Toplevel(root)
Calculate.title("Calculate BMI")
Calculate.geometry("480x370+600+400")

lblName = ttk.Label(Calculate, text="Enter Name")
entName = ttk.Entry(Calculate)
lblAge = ttk.Label(Calculate, text="Enter Age")
entAge = ttk.Entry(Calculate)
lblPhone = ttk.Label(Calculate, text="Enter Phone No.")
entPhone = ttk.Entry(Calculate)
lblGender = ttk.Label(Calculate, text="Gender")
lblHeight = ttk.Label(Calculate, text="Enter Height in m")
entHeight = ttk.Entry(Calculate)
btnConvert = ttk.Button(Calculate, text="Convert", width=10, command=f4)
lblWeight = ttk.Label(Calculate, text="Enter Weight in kg")
entWeight = ttk.Entry(Calculate)
selection = IntVar()
selection.set(1)
rbMale = ttk.Radiobutton(Calculate, text="Male", variable=selection, value=1)
rbFemale = ttk.Radiobutton(Calculate, text="Female", variable=selection, value=2)
btnCalculate = ttk.Button(Calculate, text="Calculate", width=10, command=f5)
btnBack = ttk.Button(Calculate, text="Back", width=10, command=f6)

lblName.place(x=30, y=10)
entName.place(x=200, y=10)
lblAge.place(x=30, y=60)
entAge.place(x=200, y=60)
lblPhone.place(x=30, y=110)
entPhone.place(x=200, y=110)
lblGender.place(x=30, y=160)
rbMale.place(x=200, y=160)
rbFemale.place(x=300, y=160)
lblHeight.place(x=30, y=210)
entHeight.place(x=200, y=210)
btnConvert.place(x=350, y=210)
lblWeight.place(x=30, y=260)
entWeight.place(x=200, y=260)
btnCalculate.place(x=50, y=310)
btnBack.place(x=250, y=310)

Calculate.withdraw()

# ========================================================================= Convert Tab =========================================================================
Convert = Toplevel(root)
Convert.title("Calculate BMI")
Convert.geometry("300x320+600+200")

lblConvert = ttk.Label(Convert, text="Enter your Height")
lblFeet = ttk.Label(Convert, text="Feet")
entFeet = ttk.Entry(Convert)
lblInches = ttk.Label(Convert, text="Inches")
entInches = ttk.Entry(Convert)
btnConvert = ttk.Button(Convert, text="Convert", width=10, command=f7)
btnBack = ttk.Button(Convert, text="Back", width=10, command=f8)

lblConvert.pack(pady=10)
lblFeet.pack(pady=10)
entFeet.pack(pady=10)
lblInches.pack(pady=10)
entInches.pack(pady=10)
btnConvert.pack(pady=10)
btnBack.pack(pady=10)

Convert.withdraw()

# ========================================================================= History Tab =========================================================================
History = Toplevel(root)
History.title("View Student Details")
History.geometry("350x250+600+200")

History_data = ScrolledText(History, width=35, height=10, )
History_btnBack = ttk.Button(History, text="Back", width=10, command=f9)

History_data.pack(pady=5)
History_btnBack.pack(pady=5)

History.withdraw()

root.mainloop()
