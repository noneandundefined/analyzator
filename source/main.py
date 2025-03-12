# Анализ кода на потенциальные ошибки:
# Созданные но не использованные переменные
# Созданные но не используемые функции (публичные)
# Вывод в стиле дерева зависимости папок и файлов
# Анализ кода на потенциальные ошибки

from load_config import load_config
from view_tree import viewTree


def __setup__():
    # Checking for a config file, if not, create
    load = load_config()

    if load["analysis"]["security"]:
        pass
    elif load["analysis"]["viewTree"]:
        viewTree("./")


def __main__():
    __setup__()


__main__()
