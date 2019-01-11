# conda activate py2ins2exe ## python --version ### 3.7.1
# pip install matplotlib
# pip install PyQt5
# pip install wheel
# pip install pyinstaller

# pyinstaller --onedir --onefile --noconsole --icon=app.ico --name=second_lab "C:путь_до_файла\qtplot.py"


import sys
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QVBoxLayout,
 QTextEdit, QLabel, QLineEdit)

from PyQt5 import QtCore, QtGui, QtWidgets
import time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import numpy as np
import math
import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        '''
        self.setGeometry(QApplication.desktop().width()/2,
                        0,
                        QApplication.desktop().width()/2,
                        QApplication.desktop().height())
        '''
               
        self.label0 = QLabel("Толщина слоя L_sl, мм")#, flag=QtCore.Qt.Window)
        self.line_edit0 = QLineEdit('0.5')
        self.label0.setAlignment(QtCore.Qt.AlignHCenter)
        # value = line_edit.text()
        # int(value)

        self.label1 = QLabel("Коэффициент рассеяния mu_s")#, flag=QtCore.Qt.Window)
        self.line_edit1 = QLineEdit('187.5')
        self.label1.setAlignment(QtCore.Qt.AlignHCenter)

        self.label2 = QLabel("Коэффициент поглощения mu_a")#, flag=QtCore.Qt.Window)
        self.line_edit2 = QLineEdit('5')
        self.label2.setAlignment(QtCore.Qt.AlignHCenter)

        self.label3 = QLabel("Средний косинус угла рассеяния g")#, flag=QtCore.Qt.Window)
        self.line_edit3 = QLineEdit('0.9')
        self.label3.setAlignment(QtCore.Qt.AlignHCenter)

        self.label4 = QLabel("Число падающих фотонов в единицу времени N")#, flag=QtCore.Qt.Window)
        self.line_edit4 = QLineEdit('100')
        self.label4.setAlignment(QtCore.Qt.AlignHCenter)

        #self.label5 = QLabel("Радиус лазерного пучка на поверхности  R, mm")#, flag=QtCore.Qt.Window)
        #self.line_edit5 = QLineEdit('5')
        

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        # self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Построить случай Circle')
        self.button.clicked.connect(lambda: self.transmittance('circle'))

        self.button1 = QPushButton('Построить случай Quadrangle')
        self.button1.clicked.connect(lambda: self.transmittance('square'))

        self.text_edit = QTextEdit() # тестовое поле для вывода информации

        self.button2 = QPushButton('Очистить текстовое поле вывода')
        self.button2.clicked.connect(self.clear_text)

        # set the layout
        layout = QVBoxLayout()
        #layout.addWidget(self.toolbar)
        
        layout.addWidget(self.label0)
        layout.addWidget(self.line_edit0)
        layout.addWidget(self.label1)
        layout.addWidget(self.line_edit1)
        layout.addWidget(self.label2)
        layout.addWidget(self.line_edit2)
        layout.addWidget(self.label3)
        layout.addWidget(self.line_edit3)
        layout.addWidget(self.label4)
        layout.addWidget(self.line_edit4)
        #layout.addWidget(self.label5)
        #layout.addWidget(self.line_edit5)
        

        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.button1)
        layout.addWidget(self.text_edit)

        layout.addWidget(self.button2)
        self.setLayout(layout)

    def clear_text(self):
        self.text_edit.clear()

    def load_data(self,sp):
        for i in range(1,11):
            time.sleep(2)
            sp.showMessage("<h1>Загрузка данных...{0}%</h1>".format(i*10),
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
            QtWidgets.qApp.processEvents()

    def generate_theta(self, g):
        if (g > 0) and (g < 1):
            #return math.acos((1+g**2-((1-g**2)/(1-g+2*g*random.SystemRandom().random()))**2)/(2*g))    
            
            try:
                return math.acos((1+g**2-((1-g**2)/(1-g+2*g*random.SystemRandom().random()))**2)/(2*g))
            except ValueError:
                text_error = "Это ещё что за нахёр? "
                self.text_edit.append('Средний косинус угла рассеяния должен лежать в открытом интервале от 0 до 1')
            except ArithmeticError:
                text_error = "Это ещё что за нахёр? "
                self.text_edit.append('Средний косинус угла рассеяния должен лежать в открытом интервале от 0 до 1')
            except Exception:
                text_error = "Это ещё что за нахёр? "
                self.text_edit.append('Средний косинус угла рассеяния должен лежать в открытом интервале от 0 до 1')
        #except ZeroDivisionError:
            #text_error = "Это ещё что за нахёр? "
            #self.text_edit.append(text_error + 'Средний косинус угла рассеяния должен лежать в открытом интервале от 0 до 1')
        else:
            self.text_edit.clear()
            text_error = "Это ещё что за нахёр? "
            self.text_edit.append(text_error+ 'Средний косинус угла рассеяния должен лежать в открытом интервале от 0 до 1')
                

    def transmittance(self, shape):#, L_sl=5,mu_s=287.5,mu_a=15,g=.8,N=99): 
        """
        L_sl - толщина слоя
        mu_s - коэффициент рассеяния
        mu_a - коэффициент поглощения
        g - средний косинус угла рассеяния
        """
        
        #N = 99 # число падающих фотонов в единицу времени
        
        L_sl = float(self.line_edit0.text()) # 0.5
        mu_s = float(self.line_edit1.text()) # 157.5
        mu_a = float(self.line_edit2.text()) # 5
        g = float(self.line_edit3.text()) # .8
        N = int(self.line_edit4.text()) # 100

        if N < 0 or N == 0:
            self.text_edit.clear()
            self.text_edit.append('N падающих должно быть > 0')
            return

        if L_sl < 0:
            self.text_edit.clear()
            self.text_edit.append('Толщина слоя должна быть неотрицательной')
            return

        if mu_s < 0 or mu_s == 0:
            self.text_edit.clear()
            self.text_edit.append('Коэффициент рассеяния должен быть > 0')
            return

        if mu_a < 0 or mu_a == 0:
            self.text_edit.clear()
            self.text_edit.append('Коэффициент поглощения должен быть > 0')
            return

        if g <= 0 or g > 1:
            #self.text_edit.clear()
            text_error = "Это ещё что за нахёр? "
            self.text_edit.append(text_error+ 'Средний косинус угла рассеяния должен лежать в открытом интервале от 0 до 1')
            return

        L_ph = -1./(mu_a+mu_s) # средняя длина свободного пробега
        p_s = mu_s/(mu_a+mu_s) # вероятность рассеяния ## оптическое альбедо

        #x = 1
        #y = 1
        #z = 0 # начальные координаты для N падающих фотонов

        R = 1

        N_a = 0 # начальное число поглощёных фотонов
        N_out = 0 # начальное число прошедших фотонов

        r_int = [] 
        psi_int = []

        r_out = [] 
        psi_out = []
        
        for i in range(N):
            z = 0
            if shape == 'square':
                x = R*(random.SystemRandom().random() - 0.5)
                y = R*(random.SystemRandom().random() - 0.5)

                r = np.sqrt(x**2+y**2)
                psi = np.arctan2(y, x)

                r_int.append(r)
                psi_int.append(psi)

                phi = 2*np.pi*random.SystemRandom().random()

                L = L_ph*np.log(1-random.SystemRandom().random()) # длина свободного пробега фотона
                
                theta = None
                while not theta:
                    theta = self.generate_theta(g)
                
                absorbed = False
                while z < L_sl and not absorbed:    
                    generator = random.SystemRandom().random()
                    if generator < p_s:
                        x += L*np.sin(theta)*np.cos(phi)
                        y += L*np.sin(theta)*np.sin(phi)
                        z += L*np.cos(theta)
                    else:
                        absorbed = True
                if not absorbed:
                    r = np.sqrt(x**2+y**2)
                    psi = np.arctan2(y, x)
                    #print(r, psi)
                    r_out.append(r)
                    psi_out.append(psi)
                    #print(x_out)
                    #print(y_out)
                    N_out += 1
            elif shape == 'circle':
                r = R*random.SystemRandom().random()
                psi = 2*np.pi*np.random.sample()

                #r = np.sqrt(x**2+y**2)
                #psi = np.arctan2(y, x)

                r_int.append(r)
                psi_int.append(psi)

                phi = 2*np.pi*random.SystemRandom().random()

                L = L_ph*np.log(1-random.SystemRandom().random()) # длина свободного пробега фотона
                
                theta = None
                while not theta:
                    theta = self.generate_theta(g)
                
                absorbed = False
                while z < L_sl and not absorbed:    
                    generator = random.SystemRandom().random()
                    if generator < p_s:
                        r += L*np.sin(theta)*np.cos(phi)
                        r = abs(r)
                        psi += 2*np.pi*random.SystemRandom().random()
                        z += L*np.cos(theta)
                    else:
                        absorbed = True
                if not absorbed:
                    r_out.append(r)
                    psi_out.append(psi)
                    N_out += 1
            else:
                self.text_edit.append('Укажите форму пучка')
        
        #r_out.append(r)
        #psi_out.append(psi)

        try:
            T = N_out / N
        except ArithmeticError:
            T = 0
        
        try:
            A = N_a / N
        except ArithmeticError:
            A = 0

        R_koef = 1 - (T + A)
        #return N_tr
        #print('N_out = ', N_out, '\n')
        
        #self.text_edit.clear()
        self.text_edit.append('N прошедших = ' + str(N_out))
        
        self.figure.clear()

        ax1 = self.figure.add_subplot(121, projection='polar')
        #print(psi_out, r_out)
        ax2 = self.figure.add_subplot(122, projection='polar')
        ax1.plot(psi_int, r_int, 'g.')
        ax2.plot(psi_out, r_out, 'r.')
        #plt.subplots_adjust(hspace=.6)
        self.canvas.draw()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # показать окно-картинку загрузки
    
    '''
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("zen_img.jpg"))
    splash.showMessage("<h1>Загрузка данных... 0%</h1>", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()
    QtWidgets.qApp.processEvents()
    window = Window()
    #window.setWindowTitle("Использование класса QSplashScreen")
    #window.resize(300, 30)
    window.load_data(splash)
    #window.show()
    splash.finish(window)
    '''

    main = Window()
    
    # цвет фона
    pal = main.palette()
    pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
        QtGui.QColor('#ADFF2F')) # GreenYellow
    pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window,
        QtGui.QColor('#F08080')) # LightCoral
    main.setPalette(pal)

    main.show()
    #main.showMaximized()

    sys.exit(app.exec_())