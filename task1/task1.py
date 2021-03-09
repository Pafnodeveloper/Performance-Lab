import sys


def itoBase2(num, to_base=10, from_base=10):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return itoBase2(n // to_base, to_base) + alphabet[n % to_base]


def itoBase(num, base):
    try:
        if base.lower() == 'двоичная':
            return bin(int(num))
        elif base.lower() == 'восьмиричная':
            return oct(int(num))
        elif base.lower() == 'шестнадцатиричная':
            return hex(int(num))
        else:
            return "Доступны следующие системы:\n 'двоичная', 'восьмиричная', 'шестнадцатиричная'"
    except ValueError:
        return "Введите число в десятичной системе счисления"


if __name__ == "__main__":
    user_args = sys.argv
    try:
        to_base = int(user_args[2])
        from_base = int(user_args[3])
        print(itoBase2(user_args[1], to_base, from_base))
    except ValueError:
        print("Вы должны вводить числа, сначала число, потом какой системе оно принадлежит и в какую переводить")
