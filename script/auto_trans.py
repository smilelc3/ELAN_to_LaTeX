"""
该脚本是为标准化后的article数据，进行Latex转换
"""
from script.auto_stand import deal_one_article
import os
import csv
import re
from doc.Ipa_to_pinyin_match import INITIAL_RULER, FINAL_RULER

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
        self.INITIAL_RULER = INITIAL_RULER
        self.FINAL_RULER = FINAL_RULER

        # 删除可能存在的生成结果
        for dir, folder, files in os.walk(self.resultFolder):
            for file in files:
                os.remove(dir + '/' + file)

        #按照第一个长度排序，然后逆序
        self.INITIAL_RULER.sort(key=lambda x: len(x[0]))
        self.INITIAL_RULER.reverse()

        self.FINAL_RULER.sort(key=lambda x: len(x[0]))
        self.FINAL_RULER.reverse()

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
            latexText = '\\begin{table}[ht]\n' + '\t\\scriptsize\n'
            latexText += '\\begin{tabular}{%s}\n\t' % ('l' * length)

            # 拼写符号
            for Index, ipa in enumerate(sentence[0]):
                splitResultList = re.split('(⁵⁵|⁵³|³⁵|³³|²¹|¹²|⁵²|²⁵)', ipa)
                if splitResultList[-1] == '':
                    splitResultList.pop()
                # print(splitResultList)
                for char in splitResultList:
                    if char == '':
                        pass
                    Char = char.replace('-', '')     # 去除-符号


                    newChar = ''
                    isMatch = False

                    # 声母 + 韵母
                    for initial in self.INITIAL_RULER:
                        for final in self.FINAL_RULER:
                            if initial[0] + final[0] == Char:
                                newChar = initial[1] + final[1]
                                isMatch = True
                                break
                        if isMatch is True:
                            break
                    # 单韵母
                    for final in self.FINAL_RULER:
                        if final[0] == Char:
                            newChar = final[1]
                            isMatch = True
                            break

                    if isMatch is True:
                        latexText += newChar
                    elif Char.isalpha():
                        print(Char)
                        pass

                    # 处理音调和符号
                    if Char in self.DICT.keys():
                        latexText += self.DICT[Char]

                    if Char in '，。？、！……“”（）：；～×+-=【】[]*/\' ,.?!\"\^():':
                        latexText += Char

                # 处理最后一行问题
                if Index != len(sentence[0]) - 1:
                    latexText += ' & '
            latexText += '\\\\\n\t'

            # 国际音标
            for Index, ipa in enumerate(sentence[0]):
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
    print(AutoTransTest.INITIAL_RULER, AutoTransTest.FINAL_RULER, sep='\n')
    for fileStr in AutoTransTest.rawTextList:
        print(fileStr)
        AutoTransTest.transform_one_article(fileStr)

