from matplotlib.pyplot import subplot, subplots, savefig
from numpy import array, linspace, pi
from random import sample
from io import BytesIO
from base64 import b64encode


def modify(a):
    return (a[0] / 255, a[1] / 255, a[2] / 255)


def create_diagram(groups, arr):
    if len(groups) and len(arr):
        # Список названий параметров
        parameters = array(groups)

        # Список значений для каждого параметра (ранги от 0 до 100)
        values = array([round(i, 2) for i in arr])

        # Определение максимального значения параметров
        max_value = 100

        # Создание углов для всех параметров
        angles = linspace(0, 2 * pi, len(parameters), endpoint=False).tolist()
        angles += angles[:1]  # Добавление первого угла в конец списка для замыкания

        # Создание фигуры и осей
        fig, ax = subplots(subplot_kw={'projection': 'polar'})
        ax.set_rlim(0, 100)

        # Настройка полярных координат
        ax.set_theta_offset(pi / 2)  # Поворот на 90 градусов (чтобы 0 было сверху)
        ax.set_theta_direction(-1)  # Инверсия направления (против часовой стрелки)

        # Определение количества делений на оси радиуса в зависимости от максимального значения
        division_count = max_value // 5

        # Устанавливаем значения делений на радиальной оси
        ax.set_rticks(linspace(0, max_value, division_count + 1))

        # Добавление меток на каждое деление
        ax.set_yticklabels([])

        # Отключение радиальных линий, кроме делений
        ax.spines['polar'].set_visible(False)

        # Настройка заполнения столбцов
        bar_alpha = 1

        # rgbColor()
        colors = [(255, 0, 0, 'Red'), (0, 255, 0, 'Green'), (0, 0, 255, 'Blue'), (255, 255, 0, 'Yellow'),
                  (255, 0, 255, 'Magenta'), (0, 255, 255, 'Light Blue'), (255, 165, 0, 'Orange'), (255, 192, 203, 'Pink')]

        cur_colors = sample(colors, k=len(values))

        # Построение столбцов
        for i, (angle, value) in enumerate(zip(angles[:-1], values)):
            # Делим столбик на несколько одинаковых кусков
            num_segments = 1
            segment_heights = linspace(0, value, num_segments + 1)
            for j in range(num_segments):
                # Разные цвета для каждого параметра
                color = modify(cur_colors[i])
                ax.bar(angle, segment_heights[j + 1] - segment_heights[j], bottom=segment_heights[j],
                       width=2 * pi / len(parameters), color=color, alpha=bar_alpha)

        # Добавление меток для параметров и их значений
        ax.set_xticks(angles[:-1])  # Установка положения меток по углам линий параметров
        ax.set_xticklabels([], ha='center', va='center')  # Установка названий параметров

        # Подписываем каждый параметр и его значение
        for angle, parameter, value in zip(angles[:-1], parameters, values):
            ax.text(angle, max(value, 7) + 5, str(value) + '%', ha='center', va='center')
            ax.text(angle, 130 - (15 if (angle % (pi / 2)) == 0 else 0), parameter, ha='center', va='center', wrap=True,
                    rotation_mode='anchor')

        ax.tick_params(axis='x', pad=35)  # Установка отступа для меток

        image_stream = BytesIO()
        savefig(image_stream, format='png')
        image_stream.seek(0)
        encoded_image = b64encode(image_stream.read()).decode('utf-8')
        return encoded_image
