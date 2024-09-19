import math

#============================================================== 1 задача ==============================================================

def is_point_in_shaded_area(x, y, R):
    # Проверка, находится ли точка внутри квадрата
    if 0 <= x <= R and 0 <= y <= R:
        return True
    
    # Проверка, находится ли точка внутри окружности с центром на оси X (y = 0) радиуса R
    if x >= 0 and y >= 0 and math.sqrt(x**2 + y**2) <= R:
        return True
    
    # Проверка, находится ли точка внутри окружности с центром на оси Y (x = 0) радиуса R
    if x >= 0 and y >= 0 and math.sqrt(x**2 + y**2) <= R:
        return True
    
    return False

def first_task():
    N = int(input("Введите количество точек: "))
    R = float(input("Введите радиус R: "))

    for i in range(N):
        x, y = map(float, input(f"Введите координаты точки {i+1} (x y): ").split())
        if is_point_in_shaded_area(x, y, R):
            print(f"Точка ({x}, {y}) попадает в заштрихованную область")
        else:
            print(f"Точка ({x}, {y}) не попадает в заштрихованную область")

#============================================================== 2 задача ==============================================================

def function_value(x, R):
    # 1. Полукруг от -9 до -5 (центр (-7, 1), радиус R)
    if -9 <= x <= -5:
        y = 1 + math.sqrt(R**2 - (x + 7)**2)
        return y
    # 2. Прямая от -5 до -4 (y = 1)
    elif -5 < x <= -4:
        return 1
    # 3. Линейная функция от -4 до 0
    elif -4 < x <= 0:
        return (x + 4) / 4
    # 4. Синусоида от 0 до pi (y = sin(x))
    elif 0 < x <= math.pi:
        return math.sin(x)
    # 5. Возрастающая прямая после pi
    elif x > math.pi:
        return (x - math.pi) / math.sqrt(2)
    else:
        return None  # Для значений вне диапазона

def second_task():
    # Ввод данных
    R = float(input("Введите радиус R: "))
    X_start = float(input("Введите начальное значение X: "))
    X_end = float(input("Введите конечное значение X: "))
    dx = float(input("Введите шаг dx: "))

    # Вывод заголовка таблицы
    print(f"{'X':>10} | {'Y':>10}")
    print("-" * 25)

    x = X_start
    while x <= X_end:
        y = function_value(x, R)
        if y is not None:
            print(f"{x:10.4f} | {y:10.4f}")
        else:
            print(f"{x:10.4f} | {'Не определено':>10}")
        x += dx


#============================================================== 3 задча ===============================================================

def taylor_exp(x, epsilon):
    # Функция для вычисления e^x с использованием ряда Тейлора
    term = 1  # начальный член ряда (x^0 / 0!)
    sum_exp = term
    n = 1  # номер члена ряда
    while abs(term) > epsilon:
        term *= x / n  # вычисление следующего члена ряда
        sum_exp += term
        n += 1
    return sum_exp, n

def third_task ():
    # Ввод параметров
    X_start = float(input("Введите начальное значение X: "))
    X_end = float(input("Введите конечное значение X: "))
    dx = float(input("Введите шаг dx: "))
    epsilon = float(input("Введите точность ε (0 < ε < 1): "))

    # Заголовок таблицы
    print(f"{'X':<10}{'Taylor Exp':<20}{'Std Exp':<20}{'Terms Count':<15}")

    # Цикл для вычисления значений на интервале [X_start, X_end]
    x = X_start
    while x <= X_end:
        taylor_value, terms_count = taylor_exp(x, epsilon)  # вычисление по Тейлору
        std_value = math.exp(x)  # встроенная функция exp
        # Вывод строки таблицы
        print(f"{x:<10.5f}{taylor_value:<20.10f}{std_value:<20.10f}{terms_count:<15}")
        x += dx
