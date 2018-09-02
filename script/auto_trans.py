"""
该脚本是为标准化后的article数据，进行Latex转换
"""
from script.auto_stand import deal_one_article
import os
import csv
import re


class AutoTrans:
    def __init__(self):
        # 文件夹相关
        self.rawTextFolder = os.path.split(os.getcwd())[0] + '/rawText'
        self.dictFilePath = os.path.split(os.getcwd())[0] + '/doc/dict.csv'
        self.resultFolder = os.path.split(os.getcwd())[0] + '/result'

        # 获取所有txt
        self.rawTextList = []
        self.get_all_raw_files()

        # 加载字典
        self.DICT = {}
        self._loading_dict()

    def _loading_dict(self):
        # 读取csv至字典
        csvFile = open(self.dictFilePath, "r")
        reader = csv.reader(csvFile)

        # 建立空字典
        for item in reader:
            self.DICT[item[0]] = item[1]
        csvFile.close()

    def get_all_raw_files(self) -> list:
        for _root, _dirs, files in os.walk(self.rawTextFolder):
            for file in files:
                fileType = os.path.splitext(file)[1]
                if fileType in ['.txt', '.TXT'] and (_root + '/' + file) not in self.rawTextList:
                    self.rawTextList.append(_root + '/' + file)
        return self.rawTextList

    def transform_one_article(self, file_path):
        articleList = deal_one_article(file_path)
        resultFile = open(self.resultFolder + '/' + os.path.split(file_path)[-1], 'a')


        for sentence in articleList:
            length = len(sentence[0])
            latexText = '\\begin{table}[!htbp]\n' + '\t\\scriptsize\n'
            latexText += '\\begin{tabular}{%s}\n\t' % ('l' * length)
            # 国际音标
            print(sentence[0])
            for Index, ipa in enumerate(sentence[0]):
                latexText += '\\textipa{'

                #交换变音字符
                for index in range(len(ipa)):
                    char = ipa[index]
                    if char.encode('utf-8') == b'\xcc\x83':
                        temp = list(ipa)
                        temp[index], temp[index - 1] = temp[index - 1], temp[index]
                        ipa = ''.join(temp)

                index = 0
                while index < len(ipa):
                    char = ipa[index]
                    if char in '⁵³¹²' and ipa[index + 1] in '⁵³¹²':
                        latexText += self.DICT[ipa[index] + ipa[index + 1]]
                        index += 1

                    elif char in self.DICT.keys():
                        latexText += self.DICT[char]
                    else:
                        latexText += char
                    index += 1

                latexText += '}'

                if Index != length -1:
                    latexText += ' & '
                else:
                    latexText += ' \\\\ \n \t'


            # 汉语对译
            for index, word in enumerate(sentence[1]):
                latexText += word
                if index != len(sentence[1]) - 1:
                    latexText += ' & '
                else:
                    latexText += ' \\\\ \n \t'

            # 汉语翻译
            latexText += '\\multicolumn{%d}{l}{%s} \\\\ \n' %(length, sentence[2])

            latexText += '\\end{tabular}\n'
            latexText +='\\end{table}\n\n\n'
            resultFile.write(latexText)

if __name__ == '__main__':
    AutoTransTest = AutoTrans()
    for fileStr in AutoTransTest.rawTextList:
        print(fileStr)
        AutoTransTest.transform_one_article(fileStr)

