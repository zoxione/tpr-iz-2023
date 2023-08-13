# Частные целевые функции:
# G1 = d1^(+) -> min (для выполнения условия по рекламной аудитории)
# G2 = d2^(-) -> min (для выполнения условия по бюджету)
# Ограничения:
# 4x1 + 8х2 + d1^(+) - d1^(-) = 45 (условие по рекламной аудитории),
# 8x1 + 24x2 + d2^(+) - d2^(-) = 100 (условие по бюджету),
# x1 + 2x2 <= 10 (ограничение по рекламным агентам),
# x1 <= 6 (ограничение на рекламу по радио),
# x1, x2, d1^(+), d1^(-), d2^(+), d2^(-) >= 0.
#
# G1 > G2
#
# Шаг 1
# G1 = d1^(+) -> min
# 4x1 + 8х2 + d1^(+) - d1^(-) = 45 (условие по рекламной аудитории),
# 8x1 + 24x2 + d2^(+) - d2^(-) = 100 (условие по бюджету),
# x1 + 2x2 <= 10 (ограничение по рекламным агентам),
# x1 <= 6 (ограничение на рекламу по радио),
# x1, x2, d1^(+), d1^(-), d2^(+), d2^(-) >= 0.
#
# Шаг 2
# G2 = d2^(-) -> min
# d1^(+) = 5 (дополнительное ограничение из 1-го шага),
# 4x1 + 8х2 + d1^(+) - d1^(-) = 45 (условие по рекламной аудитории),
# 8x1 + 24x2 + d2^(+) - d2^(-) = 100 (условие по бюджету),
# x1 + 2x2 <= 10 (ограничение по рекламным агентам),
# x1 <= 6 (ограничение на рекламу по радио),
# x1, x2, d1^(+), d1^(-), d2^(+), d2^(-) >= 0.


# Зависимости
import os
import sys
from scipy.optimize import linprog, OptimizeResult
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()


# Инициализация
inputC = []             # коэффициенты целевой функции (если макс, то с -)
inputAub = []           # коэффициенты ограничений
inputBub = []           # правые части ограничений


# Перевести строку в массив
def str_to_array(str):
	array = str.split(' ')
	return list(map(float, array))


# Ввод данных
def input_data():
	global inputC, inputAub, inputBub
	inputC.clear()
	inputAub.clear()
	inputBub.clear()

	chooseInput = int(input('Как вы хотите ввести данные? (1 - файл, 2 - вручную, 3 - назад) '))

	# Ввод из файла
	if chooseInput == 1:
		# Определение пути к файлу
		application_path = ''
		if getattr(sys, 'frozen', False):
			application_path = os.path.dirname(sys.executable)
		elif __file__:
			application_path = os.path.dirname(__file__)
		fileName = input('Имя файла: ')
		file_path = f'{os.path.join(application_path, fileName)}'

		try:
			with open(file_path) as file:
				lines = file.readlines()
				# Ввод целевых функций
				countGoals = int(lines[0][:-1])
				for i in range(0, countGoals):
					cSingle = str_to_array(lines[1 + i][:-1])
					inputC.append(cSingle)

				# Ввод ограничений
				countConstraints = int(lines[countGoals + 1][:-1])
				for i in range(0, countConstraints):
					ASingle = lines[countGoals + 2 + i][0:-1]
					if '==' in ASingle:
						tt = ASingle.split(' == ')
						Aeq = str_to_array(tt[0])
						Beq = float(tt[1])
						inputAub.append(Aeq)
						inputAub.append([elem * -1 for elem in Aeq])
						inputBub.append(Beq)
						inputBub.append(Beq * -1)
					elif '<=' in ASingle:
						tt = ASingle.split(' <= ')
						inputAub.append(str_to_array(tt[0]))
						inputBub.append(float(tt[1]))
					else:
						print(f'{Fore.RED}Ошибка в файле{Style.RESET_ALL}')
						return
			print(f'Данные успешно прочитаны')
		except FileNotFoundError:
			print(f'{Fore.RED}Файл не найден{Style.RESET_ALL}')

	# Ручной ввод
	elif chooseInput == 2:
		# Ввод целевых функций
		countGoals = int(input('(1) Введите количество целевых функций: '))
		for i in range(0, countGoals):
			cSingle = str_to_array(input(f'Введите коэффициенты {i + 1} целевой функции: '))
			inputC.append(cSingle)

		# Ввод ограничений
		countConstraints = int(input('(2) Введите количество ограничений: '))
		for i in range(0, countConstraints):
			ASingle = input(f'Введите {i + 1} ограничение: ')
			if '==' in ASingle:
				tt = ASingle.split(' == ')
				Aeq = str_to_array(tt[0])
				Beq = float(tt[1])
				inputAub.append(Aeq)
				inputAub.append([elem * -1 for elem in Aeq])
				inputBub.append(Beq)
				inputBub.append(Beq * -1)
			elif '<=' in ASingle:
				tt = ASingle.split(' <= ')
				inputAub.append(str_to_array(tt[0]))
				inputBub.append(float(tt[1]))
			else:
				print(f'{Fore.RED}Ошибка ввода{Style.RESET_ALL}')
				return

	elif chooseInput == 3:
		return

	else:
		print(f'{Fore.RED}Неверный ввод!{Style.RESET_ALL}')


# Вывод данных
def show_data():
	# Вывод целевых функций
	print(f'Целевые функции ({len(inputC)}):')
	for i in range(0, len(inputC)):
		str = ''
		for j in range(0, len(inputC[i])):
			str += f'{inputC[i][j]}'
			if j != len(inputC[i]) - 1:
				str += ' + '
			else:
				str += ' -> min'
		print(str)

	# Вывод ограничений
	print(f'Ограничения ({len(inputAub)}):')
	for i in range(0, len(inputAub)):
		str = ''
		for j in range(0, len(inputAub[i])):
			str += f'{inputAub[i][j]}'
			if j != len(inputAub[i]) - 1:
				str += ' + '
			else:
				str += ' <= '
		str += f'{inputBub[i]}'
		print(str)


# Изменить данные
def edit_data():
	if len(inputC) == 0 or len(inputAub) == 0 or len(inputBub) == 0:
		print(f'{Fore.RED}Сначала надо ввести данные{Style.RESET_ALL}')
		return

	chooseEdit = int(input('Какие данные вы хотите изменить? (1 - целевые функции, 2 - ограничения, 3 - назад) '))

	# Измение целевых функций
	if chooseEdit == 1:
		for i in range(0, len(inputC)):
			print(f'Текущая {i + 1} целевая функция: {inputC[i]}')
			str = input(f'Введите новые коэффициенты (enter, чтобы пропустить): ')
			if str != '':
				array = str_to_array(str)
				if len(array) == len(inputC[i]):
					inputC[i] = array
				else:
					print(f'{Fore.RED}Неверный ввод!{Style.RESET_ALL}')
					return

	# Измение ограничений
	elif chooseEdit == 2:
		for i in range(0, len(inputAub)):
			print(f'Текущие коэффициенты {i + 1} ограничения (равенство): {inputAub[i]}')
			str = input(f'Введите новые коэффициенты (enter, чтобы пропустить): ')
			if str != '':
				array = str_to_array(str)
				if len(array) == len(inputAub[i]):
					inputAub[i] = array
				else:
					print(f'{Fore.RED}Неверный ввод!{Style.RESET_ALL}')
					return
			print(f'Текущая правая часть {i + 1} ограничения (равенство): {inputBub[i]}')
			str = input(f'Введите новую правую часть (enter, чтобы пропустить): ')
			if str != '':
				inputBub[i] = float(str)

	elif chooseEdit == 3:
		return

	else:
		print(f'{Fore.RED}Неверный ввод!{Style.RESET_ALL}')


# Решение задачи целевого программирования
def resolve_goal_programming():
	if len(inputC) == 0 or len(inputAub) == 0 or len(inputBub) == 0:
		print(f'{Fore.RED}Сначала надо ввести данные{Style.RESET_ALL}')
		return

	basis = []
	optimalResult = OptimizeResult()

	# Цикл решения задачи с i-й целью
	for i in range(0, len(inputC)):
		print(f'{Fore.LIGHTCYAN_EX}Шаг {i + 1}{Style.RESET_ALL}')

		# Данные для решения
		c = inputC[i]
		A_ub = inputAub
		b_ub = inputBub

		# Добавление дополнительного ограничения из прошлого шага
		for i in range(0, len(basis)):
			if basis[i] != 0:
				a = list(np.zeros(len(inputC[0])))
				a[i + 2] = 1.0
				A_ub.append(a)
				b_ub.append(float(basis[i]))

		# Вычисление результата задачи с i-й целью
		result = resolve_linear_programming(c, A_ub, b_ub)
		if result is not None:
			optimalResult = result
			x = list([round(elem, 2) for elem in result.x]) # округление до 2-х знаков
			basis = x[2:len(x)]
			print(f'Оптимальное значение: {round(result.fun, ndigits=2)}\n'
			      f'Значения X: {x}\n'
			      f'Количество выполненных итераций: {result.nit}\n')
		else:
			return

	# Вывод итогового результата
	print(f'{Fore.LIGHTCYAN_EX}Итоговый ответ:{Style.RESET_ALL}')
	x = list([round(elem, 2) for elem in optimalResult.x])
	print(f'Оптимальная точка: {x[0:2]}')
	indexGoals = 1
	for i in range(2, len(x), 2):
		if x[i] == 0 and x[i+1] == 0:
			print(f'Цель {indexGoals} достигается')
		else:
			print(f'Цель {indexGoals} не достигается', end=": ")
			if x[i] != 0:
				print(f'отклонение от цели d{indexGoals}^(+) = {x[i]}')
			elif x[i+1] != 0:
				print(f'отклонение от цели d{indexGoals}^(-) = {x[i+1]}')
		indexGoals += 1


# Решение задачи линейного программирования
def resolve_linear_programming(c, A_ub, b_ub):
	print('Начинается вычисление...')
	result = linprog(method='simplex', c=c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)]) # ф-ия решения симплекса из SciPy
	if result.success == True:
		print('Вычисление завершилось удачно!')
		return result
	else:
		print(f'{Fore.RED}Что-то пошло не так\n{Style.RESET_ALL}')
		return None


# Выход из программы
def exit_prog():
	print('Программа завершена', end=" ")
	sys.exit()


# Класс элемента меню
class MenuItem:
	def __init__(self, title, fun):
		self.title = title
		self.fun = fun


# Содержимое меню
menu = [
	MenuItem('Выход', exit_prog),
	MenuItem('Ввод данных (имеющиеся данные очистятся)', input_data),
	MenuItem('Вывод данных', show_data),
	MenuItem('Изменить данные', edit_data),
	MenuItem('Решить задачу целевого программирования', resolve_goal_programming)
]


# Основной поток программы
if __name__ == '__main__':
	print(f'{Fore.LIGHTGREEN_EX}--------------------------------------------')
	print(f'Целевое программирование: метод приоритетов')
	print(f'Выполнил: КТбо3-8 Отхонов Б.Н.')
	print(f'--------------------------------------------\n{Style.RESET_ALL}')

	try:
		action = -1
		while (action != 0):
			for i in range(0, len(menu)):
				print(f'{i}. {menu[i].title}')

			action = int(input('Введите действие: '))
			print('')

			isAction = False
			for i in range(0, len(menu)):
				if i == action:
					isAction = True
					menu[action].fun()
					print()

			if isAction == False:
				print(f'{Fore.RED}Неверный ввод!\n{Style.RESET_ALL}')
	except Exception as e:
		print(f'{Fore.RED}Возникла ошибка:\n{e}{Style.RESET_ALL}')
