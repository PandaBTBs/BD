
import numpy as np
import matplotlib.pyplot as plt


def gradient_descent(f1, f2, x0, y0, alpha=1.0, max_iter=5000):
    """
    Решает систему из двух уравнений методом градиентного спуска.
    
    Параметры:
        f1, f2  - функции системы (должны принимать список [x, y])
        x0, y0  - начальная точка
        alpha   - начальный шаг
        max_iter - максимум итераций
    
    Возвращает:
        x, y    - найденное решение
        iters   - сколько итераций потребовалось
        path    - траектория движения (список точек)
    """
    
    # Функция невязки: Phi = f1^2 + f2^2
    def Phi(x, y):
        return f1([x, y])**2 + f2([x, y])**2
    
    # Вычисление градиента 
    def gradient(x, y, h=0.000001):
        dPhi_dx = (Phi(x + h, y) - Phi(x, y)) / h # вправо 
        dPhi_dy = (Phi(x, y + h) - Phi(x, y)) / h # вверх
        return dPhi_dx, dPhi_dy
    
    x, y = x0, y0
    path = [(x, y)] 
    
    for k in range(max_iter):
        current_phi = Phi(x, y)
        
        if current_phi < 1e-10:
            print(f"Решение найдено за {k} итераций")
            return x, y, k, path

        gx, gy = gradient(x, y) # вектор направления минимизации (антиградиент)
        
        # Подбираем шаг (уменьшаем, если не помогает)
        step = alpha
        for _ in range(50):  
            new_x = x - step * gx
            new_y = y - step * gy
            new_phi = Phi(new_x, new_y)
            
            if new_phi < current_phi:  # условие релаксации 
                break
            step = step / 2
        
        x, y = new_x, new_y
        path.append((x, y))
        
        if k % 200 == 0:
            print(f"Итерация {k}: x={x:.4f}, y={y:.4f}, Phi={current_phi:.4f}")
    
    print(f"Не сошлось за {max_iter} итераций")
    return x, y, max_iter, path






















# ВИЗУАЛИЗАЦИЯ (3D-поверхность + информация + таблица)

def show_result(f1, f2, path, true_x=None, true_y=None, title=""):
    """
    Показывает результат:
    1. 3D-поверхность с траекторией
    2. Информационную панель
    3. Таблицу итераций
    """
    
    def Phi(x, y):
        return f1([x, y])**2 + f2([x, y])**2
    
    # Подготовка данных
    path_x = np.array([p[0] for p in path])
    path_y = np.array([p[1] for p in path])
    path_z = np.array([Phi(x, y) for x, y in path])
    
    converged = path_z[-1] < 1e-8
    
    # ---------- Сетка для 3D-поверхности ----------
    X = np.linspace(-3, 3, 60)
    Y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(X, Y)
    Z = np.zeros_like(X)
    
    for i in range(60):
        for j in range(60):
            Z[i, j] = Phi(X[i, j], Y[i, j])
    
    Z_plot = np.minimum(Z, 20)  # обрезаем большие значения
    
    fig = plt.figure(figsize=(18, 6))
    
    # 3D-поверхность с траекторией
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    
    # Поверхность
    surf = ax1.plot_surface(X, Y, Z_plot, cmap='viridis', alpha=0.7, 
                            linewidth=0, antialiased=True)
    
    # Траектория спуска
    ax1.plot(path_x, path_y, path_z, 'r-', linewidth=2.5, label='Траектория')
    
    # Старт и финиш
    ax1.scatter([path_x[0]], [path_y[0]], [path_z[0]], 
                color='lime', s=100, edgecolors='darkgreen', 
                linewidth=2, label='Старт')
    
    if converged:
        ax1.scatter([path_x[-1]], [path_y[-1]], [path_z[-1]], 
                    color='red', s=120, marker='*', edgecolors='darkred',
                    linewidth=1.5, label='Решение')
    else:
        ax1.scatter([path_x[-1]], [path_y[-1]], [path_z[-1]], 
                    color='orange', s=120, marker='X', edgecolors='darkorange',
                    linewidth=2, label='Не сошлось')
    
    # Проекция траектории на плоскость z=0
    ax1.plot(path_x, path_y, 0, 'grey', linewidth=0.8, 
             alpha=0.4, linestyle='--', label='Проекция')
    
    # Точный корень (если задан)
    if true_x is not None and true_y is not None:
        true_z = Phi(true_x, true_y)
        ax1.scatter([true_x], [true_y], [true_z], 
                    color='white', s=80, marker='D', 
                    edgecolors='black', linewidth=2, label='Точный корень')
    
    ax1.set_xlabel('x', fontsize=10)
    ax1.set_ylabel('y', fontsize=10)
    ax1.set_zlabel('Phi', fontsize=10)
    ax1.set_title('3D-поверхность с траекторией', fontsize=12)
    ax1.legend(loc='upper left', fontsize=8)
    
    # Цветовая шкала
    cbar = fig.colorbar(surf, ax=ax1, shrink=0.5, pad=0.1)
    cbar.set_label('Phi', fontsize=9)
    
    # Информация о решении
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.axis('off')
    
    # Формируем текст
    status = "РЕШЕНИЕ НАЙДЕНО" if converged else "РЕШЕНИЕ НЕ НАЙДЕНО"
    color = 'green' if converged else 'red'
    
    lines = []
    lines.append("=" * 32)
    lines.append(f"  {status}")
    lines.append("=" * 32)
    lines.append("")
    lines.append("Стартовая точка:")
    lines.append(f"  x0 = ({path_x[0]:.4f}, {path_y[0]:.4f})")
    lines.append("")
    lines.append("Найденное решение:")
    lines.append(f"  x = {path_x[-1]:.8f}")
    lines.append(f"  y = {path_y[-1]:.8f}")
    lines.append("")
    lines.append(f"  Phi(x,y) = {path_z[-1]:.10f}")
    lines.append("")
    
    # Точный корень
    if true_x is not None:
        dist = np.sqrt((path_x[-1]-true_x)**2 + (path_y[-1]-true_y)**2)
        lines.append("-" * 32)
        lines.append("Точный корень (эталон):")
        lines.append(f"  x = {true_x:.8f}")
        lines.append(f"  y = {true_y:.8f}")
        lines.append(f"  Phi = {Phi(true_x, true_y):.10f}")
        lines.append("")
        lines.append("Отклонение:")
        lines.append(f"  dx = {abs(path_x[-1]-true_x):.8f}")
        lines.append(f"  dy = {abs(path_y[-1]-true_y):.8f}")
        lines.append(f"  расстояние = {dist:.8f}")
        
        # if dist < 1e-6:
        #     lines.append("  Статус: СОВПАДАЕТ")
        # elif dist < 0.01:
        #     lines.append("  Статус: БЛИЗКО")
        # else:
        #     lines.append("  Статус: ДАЛЕКО")
        # lines.append("-" * 32)
    
    lines.append("")
    lines.append(f"Итераций: {len(path)-1}")
    if not converged:
        lines.append("(достигнут лимит)")
    lines.append("")
    lines.append("Невязки уравнений:")
    lines.append(f"  f1 = {f1([path_x[-1], path_y[-1]]):+.8f}")
    lines.append(f"  f2 = {f2([path_x[-1], path_y[-1]]):+.8f}")
    lines.append("")
    
    # Скорость сходимости
    if len(path_z) > 10:
        recent = path_z[-10:]
        ratios = []
        for i in range(len(recent)-1):
            if recent[i] > 1e-16:
                ratios.append(recent[i+1] / recent[i])
        if ratios:
            avg_ratio = np.mean(ratios)
            lines.append(f"Сходимость (посл. шаги):")
            lines.append(f"  phi(k+1)/phi(k) = {avg_ratio:.4f}")
            if avg_ratio > 0.99:
                lines.append("  Внимание: стагнация!")
    
    lines.append("")
    lines.append("Метод: градиентный спуск")
    lines.append("с дроблением шага")
    lines.append("=" * 32)
    
    info_text = "\n".join(lines)
    
    # Рамка с результатом
    ax2.text(0.5, 0.5, info_text, transform=ax2.transAxes,
             fontsize=8, verticalalignment='center',
             horizontalalignment='center',
             fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow',
                      alpha=0.95, edgecolor=color, linewidth=2))
    
    # Таблица итераций
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.axis('off')
    
    # Заголовок таблицы
    table_data = [['k', 'x', 'y', 'Phi', 'Шаг']]
    
    # Первые 5 итераций
    for idx in range(min(5, len(path))):
        x, y = path[idx]
        step_size = 0 if idx == 0 else np.sqrt((path[idx][0]-path[idx-1][0])**2 + 
                                                (path[idx][1]-path[idx-1][1])**2)
        step_str = '---' if idx == 0 else f'{step_size:.4f}'
        table_data.append([
            str(idx),
            f'{x:.4f}',
            f'{y:.4f}',
            f'{Phi(x, y):.4f}',
            step_str
        ])
    
    # Разделитель, если итераций много
    if len(path) > 10:
        table_data.append(['...', '...', '...', '...', '...'])
    
    # Последние 4 итерации
    for idx in range(max(5, len(path)-4), len(path)):
        x, y = path[idx]
        step_size = np.sqrt((path[idx][0]-path[idx-1][0])**2 + 
                           (path[idx][1]-path[idx-1][1])**2)
        table_data.append([
            str(idx),
            f'{x:.4f}',
            f'{y:.4f}',
            f'{Phi(x, y):.6f}',
            f'{step_size:.6f}'
        ])
    
    # Точный корень (если задан)
    if true_x is not None:
        table_data.append(['---', '---', '---', '---', '---'])
        table_data.append([
            'точн',
            f'{true_x:.4f}',
            f'{true_y:.4f}',
            f'{Phi(true_x, true_y):.6f}',
            'эталон'
        ])
    
    # Создаём таблицу
    table = ax3.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.5)
    
    # Раскрашиваем таблицу
    n_rows = len(table_data)
    for j in range(5):
        # Заголовок
        table[0, j].set_facecolor('#2c3e50')
        table[0, j].set_text_props(weight='bold', color='white', fontsize=9)
        
        # Строка с решением (предпоследняя или последняя)
        last_data_row = n_rows - 1
        if true_x is not None:
            last_data_row = n_rows - 3  # перед точным корнем
        
        if converged:
            table[last_data_row, j].set_facecolor('#d5f5e3')
        else:
            table[last_data_row, j].set_facecolor('#fadbd8')
        
        # Строка с точным корнем
        if true_x is not None:
            table[n_rows-1, j].set_facecolor('#d6eaf8')
    
    ax3.set_title('Таблица итераций', fontsize=12, pad=15, fontweight='bold')
    
    # Общий заголовок
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# ПРИМЕРЫ

def example1():
    """
    Система:
        x² + y² = 4
        x² - y  = 1
    Точное решение: x ≈ 1.4015, y ≈ 0.9643
    """
    print("\n" + "="*50)
    print("ПРИМЕР 1: x² + y² = 4, x² - y = 1")
    print("="*50)
    
    def f1(p):
        x, y = p[0], p[1]
        return x**2 + y**2 - 4
    
    def f2(p):
        x, y = p[0], p[1]
        return x**2 - y - 1
    
    x, y, iters, path = gradient_descent(f1, f2, x0=0.5, y0=0.5)
    
    show_result(f1, f2, path, true_x=1.401525087, true_y=0.964253156,
                title="Пример 1: x²+y²=4, x²-y=1")


def example2():
    """
    Система:
        y = x² - 1
        y = 2 - x²
    Точные корни: x ≈ ±1.2247, y = 0.5
    """
    print("\n" + "="*50)
    print("ПРИМЕР 2: y = x²-1, y = 2-x²")
    print("="*50)
    
    def f1(p):
        x, y = p[0], p[1]
        return y - x**2 + 1
    
    def f2(p):
        x, y = p[0], p[1]
        return y - 2 + x**2
    
    x, y, iters, path = gradient_descent(f1, f2, x0=-0.5, y0=2.0)
    
    show_result(f1, f2, path, true_x=-1.22474487, true_y=0.5,
                title="Пример 2: y=x²-1, y=2-x²")


# def example3():
#     """
#     Система:
#         x + e^y = 3
#         x² + y² = 4
#     Точное решение: x ≈ 1.3035, y ≈ 0.5291
#     """
#     print("\n" + "="*50)
#     print("ПРИМЕР 3: x + e^y = 3, x² + y² = 4")
#     print("="*50)
    
#     def f1(p):
#         x, y = p[0], p[1]
#         return x + np.exp(y) - 3
    
#     def f2(p):
#         x, y = p[0], p[1]
#         return x**2 + y**2 - 4
    
#     x, y, iters, path = gradient_descent(f1, f2, x0=0.0, y0=0.0)
    
#     show_result(f1, f2, path, true_x=1.30351647, true_y=0.52906815,
#                 title="Пример 3: x+e^y=3, x²+y²=4")


if __name__ == "__main__":
    print("Решение систем уравнений методом градиентного спуска\n")
    
    example1()
    example2()
    # example3()
    
    print("\nГотово!")