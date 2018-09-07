"""
该脚本的目的在于自动标准化文本
1 去除首位无意义字符
2 中间多余字符
3 行间多余换行
4 开头无意义文本
"""
from typing import List, Any


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


    # 处理汉语对译

    transOne2One = sentenceList[1].split(' ')
    transOne2One = [item for item in transOne2One if item != '']

    # 处理汉语翻译
    transZh = sentenceList[2].replace(' ', '')

    if len(ipaList) != len(transOne2One):
        print(f'对译无法对齐：{preLine}行')
        print('国际音标', ipaList)
        print('汉语对译', transOne2One)
        print('汉语翻译', transZh)
        print('\n')


    return [ipaList, transOne2One, transZh]

if __name__ == '__main__':
    print(deal_one_article('/home/smile/PycharmProjects/ELAN_to_LaTeX/rawText/赶野猪.txt'))
