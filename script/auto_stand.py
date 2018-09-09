"""
该脚本的目的在于自动标准化文本
1 去除首位无意义字符
2 中间多余字符
3 行间多余换行
4 开头无意义文本
5 生成拼音
"""

from doc.Ipa_to_pinyin_match import INITIAL_RULER, FINAL_RULER
from typing import List
from script.line_break import font as Font
import re, csv, os

dictFilePath = os.path.split(os.getcwd())[0] + '/doc/dict.csv'


def loading_dict():
    # 读取csv至字典
    DICT = {}
    csvFile = open(dictFilePath, "r")
    reader = csv.reader(csvFile)
    # 建立空字典
    for item in reader:
        DICT[item[0]] = item[1]
    csvFile.close()
    return DICT


# 不带自动换行
def deal_one_article(path) -> list:
    textList = open(path, 'r').readlines()

    preLine = 1

    # 去除开头无意义文本
    if 'file' in textList[0]:
        textList = textList[2:]
        preLine += 2

    isNewSentence = False
    newSentence = []
    ariticle = []
    for row in textList:
        preLine += 1
        if row.strip() == '':
            if newSentence != []:
                textList = deal_one_sentence(newSentence, preLine - 3)
                ariticle.append(textList)
            if isNewSentence is True:
                isNewSentence = False
                newSentence = []

            continue

        else:
            isNewSentence = True
            newSentence.append(row)

    return ariticle


# 带自动补换行
def deal_one_article_breakline(path):
    standList = deal_one_article(path)
    #print(standList)

    # 记录数据 单位px
    totalLength = 768               # 总长度
    #1pt  = 0.35146m
    colsep = totalLength / 32       #　列间隔
    fontSize = 14                   # 字体大小
    rg = 5                          # 允许波动
    maxRemainLength = totalLength * 0.4     # 允许最大剩余
    transZhPercent = totalLength / 815


    newArticle = []
    curLength = 0
    newSentence = [[], [], [], []]
    lastRemain = [[], [], [], []]
    sentence: newSentence.__class__
    for sentence_index ,sentence in enumerate(standList):
        #print('当前处理', sentence, '\n')
        # 单句
        length = len(sentence[0])

        while lastRemain != [[], [], [], []]:
            for index in range(len(lastRemain[0])):
                wordMax = max(
                    Font.get_size(lastRemain[0][index], ('Times New Roman"', fontSize)),
                    Font.get_size(lastRemain[1][index], ('Times New Roman"', fontSize)),
                    Font.get_size(lastRemain[2][index], ('SimSun', fontSize)) * transZhPercent
                              )

                # 剩余长度可容纳
                if curLength + wordMax <= totalLength * (1+rg/100):
                    newSentence[0].append(lastRemain[0][index])
                    newSentence[1].append(lastRemain[1][index])
                    newSentence[2].append(lastRemain[2][index])
                    curLength += wordMax + colsep

                    # 长度超 maxRemainLength
                    if index == len(lastRemain[0]) - 1 and curLength > maxRemainLength:
                        #print('长度超 maxRemainLength')
                        newArticle.append(newSentence)
                        _display(newSentence)
                        newSentence = [[], [], [], []]
                        lastRemain = [[], [], [], []]
                        curLength = 0
                        break

                    # 剩余已处理
                    if index == len(lastRemain[0]) - 1:
                        #_display(newSentence)
                        lastRemain = [[], [], [], []]
                        break

                # 行已满
                if curLength + wordMax > totalLength * (1+rg/100):
                    newArticle.append(newSentence)
                    _display(newSentence)
                    newSentence = [[], [], [], []]
                    curLength = 0
                    lastRemain = [lastRemain[0][index + 1:], lastRemain[1][index + 1:], lastRemain[2][index + 1:], []]
                    #print('行已满')
                    #print('剩余：', lastRemain)
                    break


        # 计算新来行
        for index in range(length):
            wordMax = max(
                Font.get_size(sentence[0][index], ('Times New Roman"', fontSize)),
                Font.get_size(sentence[1][index], ('Times New Roman"', fontSize)),
                Font.get_size(sentence[2][index], ('SimSun', fontSize)) * transZhPercent
                          )

            if curLength + wordMax <= totalLength * (1+rg/100):         # 行内可添加
                curLength += colsep + wordMax
                newSentence[0].append(sentence[0][index])
                newSentence[1].append(sentence[1][index])
                newSentence[2].append(sentence[2][index])

            if curLength + wordMax > totalLength * (1+rg/100):        # 刚好分行
                #print('刚好分行')
                curLength = 0
                newArticle.append(newSentence)
                _display(newSentence)
                newSentence = [[], [], [], []]
                lastRemain = [sentence[0][index + 1:], sentence[1][index + 1:], sentence[2][index + 1:],[]]
                break

        if sentence_index == len(standList) - 1 and newSentence != [[], [], [], []]:
            _display(newSentence)
            newArticle.append(newSentence)
    return newArticle


def deal_one_sentence(sentenceList: list, preLine) -> list:

    # 去行首位无效字符,替换行内可能的\t
    sentenceList: List[str] = [row.strip().replace('\t', ' ') for row in sentenceList]

    if sentenceList.__len__() != 3:
        print(f'层缺失：{preLine}行')
        print(sentenceList)
        for item in sentenceList:
            print(item)
        print('\n')
        return []


    # 处理国际音标
    ipaList = sentenceList[0].split(' ')
    ipaList = [item for item in ipaList if item != '']


    # 处理拼音
    DICT = loading_dict()
    # 处理拼写符号
    charList = []
    for Index, ipa in enumerate(ipaList):
        splitResultList = re.split('(⁵⁵|⁵³|³⁵|³³|²¹|¹²|⁵²|²⁵)', ipa)
        if splitResultList[-1] == '':
            splitResultList.pop()

        newWord = ''
        for char in splitResultList:
            if char == '':
                pass
            Char = char.replace('-', '')  # 去除-符号

            newChar = ''
            isMatch = False

            # 声母 + 韵母
            for initial in INITIAL_RULER:
                for final in FINAL_RULER:
                    if initial[0] + final[0] == Char:
                        newChar = initial[1] + final[1]
                        isMatch = True
                        break
                if isMatch is True:
                    break
            # 单韵母
            for final in FINAL_RULER:
                if final[0] == Char:
                    newChar = final[1]
                    isMatch = True
                    break

            if isMatch is True:
                newWord += newChar
            elif Char.isalpha():
                print(Char)
                pass

            # 处理音调和符号
            if Char in DICT.keys():
                newWord += Char
            if Char in '，。？、！……“”（）：；～×+-=【】[]*/\' ,.?!\"\^():':
                newWord += Char

        charList.append(newWord)

    # 处理汉语对译

    transOne2One = sentenceList[1].split(' ')
    transOne2One = [item for item in transOne2One if item != '']

    # 处理汉语翻译
    transZh = [(sentenceList[2].replace(' ', ''), 0)]     # 0代表标注位置

    if len(ipaList) != len(transOne2One):
        print(f'对译无法对齐：{preLine}行')
        print('标准拼音', charList)
        print('国际音标', ipaList)
        print('汉语对译', transOne2One)
        print('汉语翻译', transZh)
        print('\n')


    return [charList, ipaList, transOne2One, transZh]


def _display(sentence):

    print('')
    for pinyin in sentence[0]:
        print(pinyin, end=' ')
    print('')
    for ipa in sentence[1]:
        print(ipa, end=' ')
    print('')
    for Zh in sentence[2]:
        print(Zh, end=' ')

    print('\n')



if __name__ == '__main__':
    result = deal_one_article_breakline('/home/smile/Documents/土家语LaTeX排版/ELAN_to_LaTeX/rawText/赶野猪.txt')
    print(result)
