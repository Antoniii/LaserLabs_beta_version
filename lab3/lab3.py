# conda activate py2ins2exe ## python --version ### 3.7.1
# pip install matplotlib
# pip install wheel
# pip install pyinstaller

# pyinstaller --onedir --onefile --name=3lab "C:путь_до_файла\lab3.py"

import numpy as np 
from parabolic2D import parabolic2D
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pylab

# Импортируем класс слайдера
from matplotlib.widgets import Slider


l1 = 2.
l2 = 1.

#def f(x, y, t):
#	return -1. #-(x*(l1-x)*y*(l2-y) + 2.*t*(x*(l1-x)+y*(l2-y)))
f1 = -1.

def f(x, y, t):
	global f1
	return f1

def v(x, y):
	return 0.

#def u(x, y, t):
#	return 0 #t*x*(l1-x)*y*(l2-y)

n1 = 50
n2 = 50
tEnd = 1.
#x = np.linspace(0., l1, n1+1)
#y = np.linspace(0., l2, n2+1)
ut = np.zeros((n1+1, n2+1), 'float')

'''
for i in range(1, n1):
	for j in range(1, n2):
		ut[i,j] = u(x[i], y[j], tEnd)
'''
tauList = [0.1, 0.05, 0.025]

#t, U = parabolic2D(f, v, l1, l2, tEnd, n1, n2, tau)
	

if __name__ == '__main__':

	def updateGraph():
		#'''!!! Функция для обновления графика'''
        # Будем использовать l1 и l2, установленные с помощью слайдеров
		global slider_l1
		global slider_l2
		global slider_f1
		global graph_axes

        # Используем атрибут val, чтобы получить значение слайдеров
		
		l1 = slider_l1.val
		l2 = slider_l2.val
		global f1
		f1 = slider_f1.val

		x = np.linspace(0., l1, n1+1)
		y = np.linspace(0., l2, n2+1)
		
		for tau in tauList:
			t, U = parabolic2D(f, v, l1, l2, tEnd, n1, n2, tau)
			print('tau = ', tau, 'error = {:.4f}'.format(abs(np.amax(ut-U))))
		print('\n')

		X, Y = np.meshgrid(x, y)
		ax.plot_surface(X, Y, U, rstride=1, cstride=1, cmap='gray')

		ax.set_xlabel('l1')
		ax.set_ylabel('l2')
		ax.set_zlabel('u')
		#ax.clear()
		#graph_axes.clear()
		#graph_axes.plot(x, y)
		pylab.draw()

	def onChangeValue(value):
		#'''!!! Обработчик события изменения значений слайдеров'''
		ax.clear()
		updateGraph()

	#for tau in tauList:
	#	t, U = parabolic2D(f, v, l1, l2, tEnd, n1, n2, tau)
	#	print('tau = ', tau, 'error = {:.4f}'.format(abs(np.amax(ut-U))))

	#fig = pylab.figure()
	#ax = Axes3D(fig)

	fig, graph_axes = pylab.subplots()
	graph_axes.grid()
	ax = fig.add_subplot(111, projection = '3d')

	# Оставим снизу от графика место для виджетов
	fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.4)

	#X, Y = np.meshgrid(x, y)
	#ax.plot_surface(X, Y, U, rstride=1, cstride=1, cmap='gray')
	#ax.set_aspect(aspect='auto')
	

	 # Создание слайдера для задания l1
	axes_slider_l1 = pylab.axes([0.05, 0.25, 0.85, 0.04])
	slider_l1 = Slider(axes_slider_l1,
                          label='l1',
                          valmin=0.,
                          valmax=10.0,
                          valinit=2.,
                          valfmt='%1.2f')

	# !!! Подпишемся на событие при изменении значения слайдера.
	slider_l1.on_changed(onChangeValue)

    # Создание слайдера для задания l2
	axes_slider_l2 = pylab.axes([0.05, 0.17, 0.85, 0.04])
	slider_l2 = Slider(axes_slider_l2,
                       label='l2',
                       valmin=0.,
                       valmax=10.0,
                       valinit=1.,
                       valfmt='%1.2f')

    # !!! Подпишемся на событие при изменении значения слайдера.
	slider_l2.on_changed(onChangeValue)

	axes_slider_f1 = pylab.axes([0.05, 0.09, 0.85, 0.04])
	slider_f1 = Slider(axes_slider_f1,
                          label='f',
                          valmin=-10.,
                          valmax=0.,
                          valinit=-1.,
                          valfmt='%1.2f')

	# !!! Подпишемся на событие при изменении значения слайдера.
	slider_f1.on_changed(onChangeValue)

	updateGraph()
	pylab.show()