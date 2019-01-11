#!/usr/bin/python
# -*- coding: utf-8 -*-

# conda activate pyexe2
# python -V ## == 3.4.5
# python -m py2exe.build_exe 2windows-tkinter.py ## with terminal
# python -m py2exe.build_exe 2windows-tkinter.pyw ## without terminal


import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
    
from math import sqrt, sin, pi


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'Triangulation', width = 30, command = self.new_window)
        self.button1.pack()
        self.button2 = tk.Button(self.frame, text = 'Interference', width = 30, command = self.new_window2)
        self.button2.pack()
        self.frame.pack()
        self.master.title("Lab work")
        # выключаем возможность изменять окно
        self.master.resizable(width=False, height=False)

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)
    
    def new_window2(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo3(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        # текст перед первого аргумента
        x_lab = tk.Label(self.frame, text="x =").grid(row=1,column=1)
        # поле для ввода первого аргумента уравнения (a)
        self.x = tk.Entry(self.frame, width=4)
        self.x.bind("<FocusIn>", self.clear)
        self.x.grid(row=1,column=2)#,padx=(10,0))
        a1_lab = tk.Label(self.frame, text="pxls").grid(row=1,column=3)

        b_lab = tk.Label(self.frame, text="beta =").grid(row=1, column=4) 
        # поле для ввода второго аргумента уравнения (b)
        self.b = tk.Entry(self.frame, width=6)
        self.b.bind("<FocusIn>", self.clear)
        self.b.grid(row=1,column=5)
        a2_lab = tk.Label(self.frame, text="gradus").grid(row=1,column=6)

        c_lab = tk.Label(self.frame, text="phi =").grid(row=2, column=1) 
        # поле для ввода третьего аргумента уравнения (с)
        self.c = tk.Entry(self.frame, width=4)
        self.c.bind("<FocusIn>", self.clear)
        self.c.grid(row=2, column=2)
        a3_lab = tk.Label(self.frame, text="gradus").grid(row=2,column=3)

        n_lab = tk.Label(self.frame, text="n =").grid(row=3, column=4) 
        # поле для ввода третьего аргумента уравнения (с)
        self.n = tk.Entry(self.frame, width=6)
        self.n.bind("<FocusIn>", self.clear)
        self.n.grid(row=3, column=5)
        #a4_lab = tk.Label(self.frame, text="nm").grid(row=2,column=6)

        e_lab = tk.Label(self.frame, text="alpha =").grid(row=3, column=1) 
        # поле для ввода третьего аргумента уравнения (с)
        self.e = tk.Entry(self.frame, width=4)
        self.e.bind("<FocusIn>", self.clear)
        self.e.grid(row=3, column=2)
        a5_lab = tk.Label(self.frame, text="gradus").grid(row=3,column=3)

        k_lab = tk.Label(self.frame, text="k =").grid(row=2, column=4) 
        # поле для ввода третьего аргумента уравнения (с)
        self.k = tk.Entry(self.frame, width=6)
        self.k.bind("<FocusIn>", self.clear)
        self.k.grid(row=2, column=5)
        a6_lab = tk.Label(self.frame, text="mm/pxls").grid(row=2,column=6)

        M_lab = tk.Label(self.frame, text="M =").grid(row=3, column=6) 
        # поле для ввода третьего аргумента уравнения (с)
        self.M = tk.Entry(self.frame, width=6)
        self.M.bind("<FocusIn>", self.clear)
        self.M.grid(row=3, column=7)
        #a6_lab = tk.Label(self.frame, text="mm/pxls").grid(row=2,column=6)
         
        # кнопка решить
        self.but = tk.Button(self.frame, text="Solve", width=7, command=self.handler).grid(row=1, column=7, padx=(10,0))
         
        # место для вывода решения уравнения
        self.output = tk.Text(self.frame, bg="lightblue", font="Arial 12", width=40, height=10)
        self.output.grid(row=4, columnspan=8)
        self.frame.pack()
        self.master.title("Thickness")
        # выключаем возможность изменять окно
        self.master.resizable(width=False, height=False)

    def close_windows(self):
        self.master.destroy()

    def handler(self):
        """ Get the content of entries and passes result to the output area """
        try:
            # make sure that we entered correct values
            x_val = float(self.x.get())
            b_val = float(self.b.get())
            c_val = float(self.c.get())
            n_val = float(self.n.get())
            e_val = float(self.e.get())
            k_val = float(self.k.get())
            M_val = float(self.M.get())
            self.inserter(self.solver(x_val, b_val, c_val, n_val, e_val, k_val, M_val))
        except ValueError:
            self.inserter("Make sure you entered all values like a numbers!")
        except ZeroDivisionError:
            self.inserter("Linear increase, refractive index  or viewing angle of light marks cannot be zero!")
        except:
            self.inserter("Unexpected error!")
    
    def solver(self, x,b,c,n,e,k,M):
        D = (2*x*k*sin(b*180/pi)*sqrt((n**2-(sin(e*180/pi))**2)*(n**2-(sin(c*180/pi))**2)))/(M*n*sin(2*e*180/pi))
        if D >= 0:
            text = "The thickness is {:.2f} mm".format(D)        
        else:
            text = "The thickness is not exist" 
        return text

    def clear(self, event):
        """ Clears entry form """
        caller = event.widget
        caller.delete("0", "end")

    def inserter(self, value):
        """ Inserts specified value into text widget """
        self.output.delete("0.0","end")
        self.output.insert("0.0",value)

class Demo3:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        # текст перед первого аргумента
        a_lab = tk.Label(self.frame, text="z =").grid(row=1,column=1)
        # поле для ввода первого аргумента уравнения (a)
        self.a = tk.Entry(self.frame, width=4)
        self.a.bind("<FocusIn>", self.clear)
        self.a.grid(row=1,column=2)#,padx=(10,0))
        a1_lab = tk.Label(self.frame, text="mm").grid(row=1,column=3)

        b_lab = tk.Label(self.frame, text="s =").grid(row=1, column=4) 
        # поле для ввода второго аргумента уравнения (b)
        self.b = tk.Entry(self.frame, width=4)
        self.b.bind("<FocusIn>", self.clear)
        self.b.grid(row=1,column=5)
        a2_lab = tk.Label(self.frame, text="pxls").grid(row=1,column=6)

        c_lab = tk.Label(self.frame, text="L =").grid(row=2, column=1) 
        # поле для ввода третьего аргумента уравнения (с)
        self.c = tk.Entry(self.frame, width=4)
        self.c.bind("<FocusIn>", self.clear)
        self.c.grid(row=2, column=2)
        a3_lab = tk.Label(self.frame, text="cm").grid(row=2,column=3)

        d_lab = tk.Label(self.frame, text="lambda =").grid(row=2, column=4) 
        # поле для ввода третьего аргумента уравнения (с)
        self.d = tk.Entry(self.frame, width=4)
        self.d.bind("<FocusIn>", self.clear)
        self.d.grid(row=2, column=5)
        a4_lab = tk.Label(self.frame, text="nm").grid(row=2,column=6)

        e_lab = tk.Label(self.frame, text="alpha =").grid(row=3, column=1) 
        # поле для ввода третьего аргумента уравнения (с)
        self.e = tk.Entry(self.frame, width=4)
        self.e.bind("<FocusIn>", self.clear)
        self.e.grid(row=3, column=2)
        a5_lab = tk.Label(self.frame, text="gradus").grid(row=3,column=3)

        k_lab = tk.Label(self.frame, text="k =").grid(row=3, column=4) 
        # поле для ввода третьего аргумента уравнения (с)
        self.k = tk.Entry(self.frame, width=4)
        self.k.bind("<FocusIn>", self.clear)
        self.k.grid(row=3, column=5)
        a6_lab = tk.Label(self.frame, text="mm/pxls").grid(row=3,column=6)
    
         
        # кнопка решить
        self.but = tk.Button(self.frame, text="Solve", width=8, command=self.handler).grid(row=2, column=7, padx=(10,0))
         
        # место для вывода решения уравнения
        self.output = tk.Text(self.frame, bg="lightyellow", font="Arial 12", width=40, height=10)
        self.output.grid(row=4, columnspan=8)
        self.frame.pack()
        self.master.title("Refractive index")
        # выключаем возможность изменять окно
        self.master.resizable(width=False, height=False)

    def close_windows(self):
        self.master.destroy()

    def handler(self):
        """ Get the content of entries and passes result to the output area """
        try:
            # make sure that we entered correct values
            a_val = float(self.a.get())
            b_val = float(self.b.get())
            c_val = float(self.c.get())
            d_val = float(self.d.get())
            e_val = float(self.e.get())
            k_val = float(self.k.get())
            self.inserter(self.solver(a_val, b_val, c_val, d_val, e_val, k_val))
        except ValueError:
            self.inserter("Make sure you entered all values like a numbers!")
        except ZeroDivisionError:
            self.inserter("The wavelength or distance to the screen cannot be zero!")
        except:
            self.inserter("Unexpected error!")
    
    def solver(self, a,b,c,d,e,k):
        D = ((a*b*k*sin(2*e*180/pi)*10**5)/(d*c))**2+(sin(e*180/pi))**2
        if D >= 0:
            n = sqrt(D)
            text = "The refractive index is {:.2f}".format(n)        
        else:
            text = "The refractive index is not real" 
        return text
                 

    def clear(self, event):
        """ Clears entry form """
        caller = event.widget
        caller.delete("0", "end")

    def inserter(self, value):
        """ Inserts specified value into text widget """
        self.output.delete("0.0","end")
        self.output.insert("0.0",value)


def main(): 
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()
