import re

def calculate(data, findall):
    reg = r"([a-c])([+-]?=)([a-c]?)([+-]?\d*)"
    matches = findall(reg)

    for v1, s, v2, n in matches:
        if s == '=':
            data[v1] = data.get(v2, 0) + int(n or 0)
        elif s == "-=":
            data[v1] -= data.get(v2, 0) + int(n or 0)
        elif s == "+=":
            data[v1] += data.get(v2, 0) + int(n or 0)

    return data

# CТАРАЯ ВЕРСИЯ
    # reg = r"(([abc])([+-]?)(=)(?:([+-]?\d+)|(?:([abc])([+-]?\d*)?)))"
    # ans = findall(reg)  # Если придумать хорошую регулярку, будет просто
    #
    # for i in range(len(ans)):
    #     right = 0
    #
    #     sym0 = ans[i][1]  # буква0
    #     zn0 = ans[i][2]  # знак0
    #     ravno = ans[i][3]  # равно
    #     num1 = ans[i][4]  # число 1
    #     sym2 = ans[i][5]  # буква 2
    #     num2 = ans[i][6]  # число 2
    #
    #     """Правая часть"""
    #     if num1 != '':
    #         right += int(num1)
    #     elif sym2 != '':
    #         right += data[sym2]
    #     elif num2 != '':
    #         right += int(num2)
    #     else:
    #         print("Err")
    #     """Левая часть"""
    #     if zn0 == "+":
    #         data[sym0] += right
    #     elif zn0 == "-":
    #         data[sym0] -= right
    #     elif zn0 == "":
    #         data[sym0] = right
    #     else:
    #         print('Eror2')