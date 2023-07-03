import matplotlib.pyplot as plt
import numpy as np
import random
import io
import base64


def modify(a):
    return (a[0] / 255, a[1] / 255, a[2] / 255)


def create_diagram(groups, array):
    # Список названий параметров
    parameters = np.array(groups)

    # Список значений для каждого параметра (ранги от 0 до 100)
    values = np.array([round(i, 2) for i in array])

    # Определение максимального значения параметров
    max_value = 100

    # Создание углов для всех параметров
    angles = np.linspace(0, 2 * np.pi, len(parameters), endpoint=False).tolist()
    angles += angles[:1]  # Добавление первого угла в конец списка для замыкания

    # Создание фигуры и осей
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_rlim(0, 100)

    # Настройка полярных координат
    ax.set_theta_offset(np.pi / 2)  # Поворот на 90 градусов (чтобы 0 было сверху)
    ax.set_theta_direction(-1)  # Инверсия направления (против часовой стрелки)

    # Определение количества делений на оси радиуса в зависимости от максимального значения
    division_count = max_value // 5

    # Устанавливаем значения делений на радиальной оси
    ax.set_rticks(np.linspace(0, max_value, division_count + 1))

    # Добавление меток на каждое деление
    ax.set_yticklabels([])

    # Отключение радиальных линий, кроме делений
    ax.spines['polar'].set_visible(False)

    # Настройка заполнения столбцов
    bar_alpha = 1

    # rgbColor()
    colors = [(255, 0, 0, 'Red'), (0, 255, 0, 'Green'), (0, 0, 255, 'Blue'), (255, 255, 0, 'Yellow'),
              (255, 0, 255, 'Magenta'), (0, 255, 255, 'Light Blue'), (255, 165, 0, 'Orange'), (255, 192, 203, 'Pink')]

    cur_colors = random.sample(colors, k=len(values))

    # Построение столбцов
    for i, (angle, value) in enumerate(zip(angles[:-1], values)):
        # Делим столбик на несколько одинаковых кусков
        num_segments = 1
        segment_heights = np.linspace(0, value, num_segments + 1)
        for j in range(num_segments):
            # Разные цвета для каждого параметра
            color = modify(cur_colors[i])
            ax.bar(angle, segment_heights[j + 1] - segment_heights[j], bottom=segment_heights[j],
                   width=2 * np.pi / len(parameters), color=color, alpha=bar_alpha)

    # Добавление меток для параметров и их значений
    ax.set_xticks(angles[:-1])  # Установка положения меток по углам линий параметров
    ax.set_xticklabels([], ha='center', va='center')  # Установка названий параметров

    # Подписываем каждый параметр и его значение
    for angle, parameter, value in zip(angles[:-1], parameters, values):
        ax.text(angle, max(value, 7) + 5, str(value) + '%', ha='center', va='center')
        ax.text(angle, 130 - (15 if (angle % (np.pi / 2)) == 0 else 0), parameter, ha='center', va='center', wrap=True,
                rotation_mode='anchor')

    ax.tick_params(axis='x', pad=35)  # Установка отступа для меток

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image
