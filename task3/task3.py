import sys
import csv
import random
import logging

options = ['wanna top up', 'wanna scoop']
fortune = ['успех', 'фейл']

total_attempt = 0
scoop_attempt = 0
top_attempt = 0
total_scoop = 0
total_top = 0
total_failed_scoop = 0
total_failed_top = 0
scoop_mistake = 0
top_mistake = 0

format = '%(asctime)s - %(name)-10s - %(message)s'
logging.basicConfig(level="DEBUG", filename='test_log.log', format=format)
logger = logging.getLogger()


def create_log():
    current_volume = random.randint(0, 100)
    cask_volume = random.randint(100, 200)
    logger.debug(f"\nMETA DATA:\n{cask_volume} объем бочки\n{current_volume} текущий объем воды в бочке")
    count = 0
    while count < 1000000:
        pour_or_scoop = options[random.randint(0, 1)]
        how_much = random.randint(0, 50)

        if pour_or_scoop == "wanna scoop" and current_volume >= how_much:
            current_volume -= how_much
            logger.debug(f"{pour_or_scoop} {how_much}l {fortune[0]}")
        elif pour_or_scoop == 'wanna top up' and (cask_volume - current_volume) >= how_much:
            current_volume += how_much
            logger.debug(f"{pour_or_scoop} {how_much}l {fortune[0]}")
        else:
            logger.debug(f"{pour_or_scoop} {how_much}l {fortune[1]}")

        count += 1


if __name__ == "__main__":
    create_log()
    user_args = sys.argv
    if len(user_args) == 4:
        location = user_args[1]
        start_time = user_args[2].replace("Т", "T")
        end_time = user_args[3].replace("Т", "T")
        start_time = start_time.replace("T", " ")
        end_time = end_time.replace("T", " ")

        current_volume = 0
        cask_volume = 0
        started_volume = 0
        try:
            with open(location, 'r') as file:
                for line in file:
                    splitted_line = line.rstrip().split(" ")
                    if ((start_time <= " ".join(splitted_line[0:2]))
                            and (end_time >= " ".join(splitted_line[0:2]))):
                        if "текущий" in splitted_line and started_volume == 0:
                            started_volume = int(splitted_line[0])
                            current_volume = started_volume
                        if "бочки" in splitted_line and cask_volume == 0:
                            cask_volume = splitted_line[0]
                        if "scoop" in splitted_line:
                            scoop_attempt += 1
                            total_attempt += 1
                            if 'успех' in splitted_line:
                                l = int(splitted_line[-2][0:-1])
                                total_scoop += l
                                current_volume -= int(splitted_line[-2][0:-1])
                            else:
                                l = int(splitted_line[-2][0:-1])
                                total_failed_scoop += l
                                scoop_mistake += 1
                        elif 'top' in splitted_line:
                            top_attempt += 1
                            total_attempt += 1
                            if 'успех' in splitted_line:
                                l = int(splitted_line[-2][0:-1])
                                total_top += l
                                current_volume += int(splitted_line[-2][0:-1])
                            else:
                                l = int(splitted_line[-2][0:-1])
                                total_failed_top += l
                                top_mistake += 1
                    else:
                        if "текущий" in splitted_line and started_volume == 0:
                            started_volume = int(splitted_line[0])
                            current_volume = started_volume
                        if "бочки" in splitted_line and cask_volume == 0:
                            cask_volume = splitted_line[0]
        except FileNotFoundError:
            print("Не существует файла по такому пути")

        if scoop_mistake == 0:
            total_scoop_mistake = 0
        else:
            total_scoop_mistake = scoop_mistake * 100 / scoop_attempt
        if top_mistake == 0:
            total_top_mistake = 0
        else:
            total_top_mistake = top_mistake * 100 / top_attempt

        if total_attempt != 0:
            try:
                with open("result_table.csv", 'w') as csv_file:
                    file_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
                    file_writer.writerow(["Всего попыток", "Попыток зачерпнуть", "Всего зачерпнули",
                                          "Всего не удалось зачерпнуть", "Процент неудавшихся зачерпываний",
                                          "Попыток налить", "Всего налили", "Всего не удалось налить",
                                          "Процент неудавшихся налитий", "Воды в начале", "Сейчас воды в бочке"])
                    file_writer.writerow([total_attempt, scoop_attempt, total_scoop,
                                          total_failed_scoop,  total_scoop_mistake,
                                          top_attempt, total_top, total_failed_top,
                                          total_top_mistake, started_volume, current_volume])
            except Exception:
                None

        else:
            with open("result_table.csv", 'w') as csv_file:
                file_writer = csv.writer(csv_file)
                file_writer.writerow("В логе отсутствует искомый временной интервал или сам лог не был сформирован")

    else:
        print("Введите через пробел следующие данные:\n"
              "Путь к логу, время с которого начинать анализ выборки, время конца выборки\n"
              "Пример формата времени: 2020-01-01T12:00:00")
