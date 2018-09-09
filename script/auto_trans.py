"""
该脚本是为标准化后的article数据，进行Latex转换
"""
from script.auto_stand import deal_one_article, deal_one_article_breakline
import os
import csv
import re
from doc.Ipa_to_pinyin_match import INITIAL_RULER, FINAL_RULER



class AutoTrans:
    # 文件夹相关
    rawTextFolder = os.path.split(os.getcwd())[0] + '/rawText'
    resultFolder = os.path.split(os.getcwd())[0] + '/result'
    dictFilePath = os.path.split(os.getcwd())[0] + '/doc/dict.csv'
    DICT = {}

    def __init__(self):

        # 获取所有txt
        self.rawTextList = []
        self.get_all_raw_files()

        # 加载字典

        self.loading_dict()
        self.INITIAL_RULER = INITIAL_RULER
        self.FINAL_RULER = FINAL_RULER

        # 删除可能存在的生成结果
        for dir, folder, files in os.walk(self.resultFolder):
            for file in files:
                os.remove(dir + '/' + file)


    @classmethod
    def loading_dict(self):
        # 读取csv至字典
        csvFile = open(self.dictFilePath, "r")
        reader = csv.reader(csvFile)
        # 建立空字典
        for item in reader:
            self.DICT[item[0]] = item[1]
        csvFile.close()
        return self.DICT

    def get_all_raw_files(self) -> list:
        for _root, _dirs, files in os.walk(self.rawTextFolder):
            for file in files:
                fileType = os.path.splitext(file)[1]
                if fileType in ['.txt', '.TXT'] and (_root + '/' + file) not in self.rawTextList:
                    self.rawTextList.append(_root + '/' + file)
        return self.rawTextList

    def transform_one_article(self, file_path):
        articleList = deal_one_article_breakline(file_path)
        print(articleList)
        resultFile = open(self.resultFolder + '/' + os.path.split(file_path)[-1], 'a')

        for sentence in articleList:
            length = len(sentence[0])
            latexText = '\\begin{table}\n' \
                        #+ '\t\\scriptsize\n'
            latexText += '\\begin{tabular}{%s}\n\t' % ('l' * length)

            # 拼写符号
            for Index, word in enumerate(sentence[0]):

                index = 0
                while index < len(word):
                    char = word[index]
                    if char in '⁵³¹²' and word[index + 1] in '⁵³¹²':
                        latexText += self.DICT[word[index] + word[index + 1]]
                        index += 1
                    else:
                        latexText += char
                    index += 1
                # 处理最后一行问题
                if Index != len(sentence[0]) - 1:
                    latexText += ' & '
            latexText += '\\\\\n\t'

            # 国际音标
            for Index, ipa in enumerate(sentence[1]):
                latexText += '\\textipa{'

                # 交换变音字符
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

                    # 存标点符号
                    elif char not in '，。？、！……“”（）：；～×+-=【】[]*/\' ,.?!\"\^():':
                        latexText += char
                    index += 1

                latexText += '}'

                if Index != length -1:
                    latexText += ' & '
                else:
                    latexText += ' \\\\ \n \t'

            # 汉语对译
            for index, word in enumerate(sentence[2]):
                latexText += word
                if index != len(sentence[1]) - 1:
                    latexText += ' & '
                else:
                    latexText += ' \\\\ \n \t'

            # 汉语翻译
            '''
            if len(sentence[2]) <= 1:
                latexText += '\\multicolumn{%d}{l}{%s} ' % (length, sentence[3][0][0])
            else:
                lengthList = []
                for index in range(1, len(sentence[3])):
                    lengthList.append(sentence[3][index] - sentence[3][index - 1])
                lengthList.append(length - sentence[3][-1])

                for index, transZh in enumerate(sentence[3]):
                    latexText += '\\multicolumn{%d}{l}{%s} ' % (lengthList[index], sentence[3][index][0])

                    if index != len(sentence[3]) - 1:
                        latexText += ' & '
            latexText += '\\\\ \n'
            '''
            # 末尾部分
            latexText += '\\end{tabular}\n'


            latexText +='\\end{table}\n\n\n'
            resultFile.write(latexText)

if __name__ == '__main__':
    AutoTransTest = AutoTrans()
    #print(AutoTransTest.INITIAL_RULER, AutoTransTest.FINAL_RULER, sep='\n')
    for fileStr in AutoTransTest.rawTextList:
        print(fileStr)
        AutoTransTest.transform_one_article(fileStr)

