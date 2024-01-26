import re
import os


def modify_function():
    with open('F:\\Pycharm\\PycharmProjects\\Scrape_lib\\project4\\m3u8_lst\\index.m3u8', mode='r') as file:
        row_lst = file.readlines()
        with open('F:\\Pycharm\\PycharmProjects\\Scrape_lib\\project4\\m3u8_lst\\index.m3u8', mode='w') as files:
            n = 0
            for row in row_lst:
                if row:
                    if re.match('https://.*?\.ts', row):
                        modify = re.sub('https://.*?\.ts', 'F:/Pycharm/PycharmProjects/Scrape_lib/project4/m3u8_lst/{}.ts'.format(n), row)
                        n += 1
                        files.write(modify)
                    else:
                        files.write(row)


def clear_file():
    path = 'F:/Pycharm/PycharmProjects/Scrape_lib/project4/m3u8_lst/{}'
    file_lst = os.listdir('F:/Pycharm/PycharmProjects/Scrape_lib/project4/m3u8_lst')
    for file in file_lst:
        os.remove(path.format(file))


if __name__ == '__main__':
    clear_file()