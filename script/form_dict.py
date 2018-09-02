"""
脚本的原理是根据存在在rawText文件下的所有txt文本，针对在国际音标下 非（ASCII编码和汉字）编码的字符
生成LaTeX tipa宏包的转译，文件存储在doc\dict.csv

若字符已经在dict.csv文件中中存在转译，则跳过、否则需手动输入
smile
2018-09-01
"""

import os
import csv


class FormDict:
    def __init__(self):
        # 文件路径相关
        self.rawTextFolder = os.path.split(os.getcwd())[0] + '/rawText'
        self.dictFilePath = os.path.split(os.getcwd())[0] + '/doc/dict.csv'

        self.dict = {}
        self.rawTextList = []

        # 数据文件
        with open(self.dictFilePath) as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                # print(f'字符：{row[0]}  转译：{row[1]}')
                self.dict[row[0]] = row[1]

        self.dell_all_raw_files()

    def get_all_raw_files(self) -> list:
        for _root, _dirs, files in os.walk(self.rawTextFolder):
            for file in files:
                fileType = os.path.splitext(file)[1]
                if fileType in ['.txt', '.TXT'] and (_root + '/' + file) not in self.rawTextList:
                    self.rawTextList.append(_root + '/' + file)
        return self.rawTextList

    def dell_all_raw_files(self):
        self.get_all_raw_files()
        for textFile in self.rawTextList:
            self.dell_one_raw_file(textFile)

    def dell_one_raw_file(self, file: str):
        print(f'正在处理：{file}')
        textString = open(file, 'r').read()
        for char in textString:
            if '\u4e00' <= char <= '\u9fff':    # 中文判断
                continue
            if char in '1234567890':
                continue
            if char in 'abcdefghijklmnopqrstuvwxyz' + \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                continue
            if char in '，。？、！……“”（）：；～×+-=【】[]*/\' ,.?!\"\^():\t\n':
                continue
            if char not in self.dict:
                print('字符：', char)
                charTrans = input()
                self.dict[char] = charTrans
                csvfile = open(self.dictFilePath, 'w', newline='')
                csvWrite = csv.writer(csvfile)
                for key, value in self.dict.items():
                    csvWrite.writerow([key, value])

if __name__ == '__main__':
    AutoTransTest = FormDict()
    print(AutoTransTest.get_all_raw_files())