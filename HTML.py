from bs4 import BeautifulSoup as bs
import Parsing, os

typeDict = dict()
typeDict['R'] = 'резистор'
typeDict['L'] = 'индуктивность'
typeDict['C'] = 'конденсатор'
typeDict['MC'] = 'микроконтроллеры'
typeDict['MSH'] = 'микросxемы'
typeDict['TR'] = 'транзисторы'
typeDict['D'] = 'ДИОДЫ'
typeDict['O'] = 'ПРОЧЕЕ'

def createTable(input, numCh, foundOK, reqestInfo):
    Req=list();
    t = 0;
    for captain in input:
        Req.append(captain.split('+'))
        print(captain)
    #Добавление шапки таблицы
    replyPage=bs(open('templates/result.html', encoding='utf-8'),'html.parser')
    for tg in replyPage.find_all('table'):
        newCaption=replyPage.new_tag('caption')
        newCaption.string=('ТАБЛИЦА КОМПОНЕНТОВ ПО ЗАПРОСУ: ' + str(reqestInfo))
        tg.append(newCaption)
        newHander=replyPage.new_tag('tr')
        tg.append(newHander)
        for tr in replyPage.find_all('tr'):
            newHanderName=replyPage.new_tag('th')
            newHanderName.string=('ТИП')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('НАИМЕНОВАНИЕ')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('КОРПУС')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('КОЛИЧЕСТВО')
            tr.append(newHanderName)
            # newHanderName = replyPage.new_tag('th')
            # newHanderName.string = ('Списать')
            # tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('Списано/Внесено')
            tr.append(newHanderName)
            # newHanderName = replyPage.new_tag('th')
            # newHanderName.string = ('Внести')
            # tr.append(newHanderName)
        while t<len(Req):
            inputData = replyPage.new_tag('tr')
            inputData.insert(2, replyPage.new_tag('inputData'+str(t)))
            tg.append(inputData)
            for tg in replyPage.find_all('inputData'+str(t)):
                newData=replyPage.new_tag('td')
                newData.string=str(Req[t][1])
                tg.append(newData)
                newData = replyPage.new_tag('td')
                newData.string = str(Req[t][2])
                tg.append(newData)
                newData = replyPage.new_tag('td')
                newData.string = str(Req[t][3])
                tg.append(newData)
                newData = replyPage.new_tag('td')
                newData.string = str(Req[t][4])
                tg.append(newData)
                if foundOK:
                    curCh = numCh.split('+')
                    newData = replyPage.new_tag('td')
                    newFormIn = replyPage.new_tag('form')
                    if curCh[0]==str(t):
                        newFormIn['action'] = ('http://192.168.0.103:3000/output/' + str(Req[t][2]) +
                                               '+' + str(Req[t][3]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(int(curCh[1])-1))
                    else:
                        newFormIn['action'] = ('http://192.168.0.103:3000/output/' + str(Req[t][2]) +
                                '+' + str(Req[t][3]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(-1))

                    newFormIn['method']='action'
                    newBotIn = replyPage.new_tag('button')
                    newBotIn.string = 'Списать'
                    newFormIn.insert(2, newBotIn)
                    newData.insert(2, newFormIn)
                    numCompEdit = replyPage.new_tag('p')
                    if curCh[0]==str(t):
                            if not Req[t][4]=='0':
                                numCompEdit.string = curCh[1]
                    else:
                            numCompEdit.string = '0'
                    newData.insert(3, numCompEdit)
                    # tg.append(newData)
                    # newData = replyPage.new_tag('td')
                    newFormOut = replyPage.new_tag('form')
                    if curCh[0] == str(t):
                        newFormOut['action'] = ('http://192.168.0.103:3000/input/' + str(Req[t][2]) +
                                               '+' + str(Req[t][3]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(
                                    int(curCh[1]) + 1))
                    else:
                        newFormOut['action'] = ('http://192.168.0.103:3000/input/' + str(Req[t][2]) +
                                               '+' + str(Req[t][3]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(1))

                    newFormOut['method'] = 'action'
                    newBotOut = replyPage.new_tag('button')
                    newBotOut.string = 'Внести'
                    newFormOut.insert(2,newBotOut)
                    newData.insert(2, newFormOut)
                    tg.append(newData)

            t+=1
    replyPage.prettify(formatter="html")
    f = open('templates/reply.html', 'w', encoding='utf-8')
    f.write(str(replyPage))
    f.close()
    return

def createTableSQL(input, numCh, foundOK, reqestInfo):
    #os.remove(path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'templates/reply.html'))
    t=0;
    Req=input
    replyPage=bs(open('templates/result.html', encoding='utf-8'),'html.parser')
    for tg in replyPage.find_all('table'):
        newCaption=replyPage.new_tag('caption')
        newCaption.string=('ТАБЛИЦА КОМПОНЕНТОВ ПО ЗАПРОСУ: ' + str(reqestInfo))
        tg.append(newCaption)
        newHander=replyPage.new_tag('tr')
        tg.append(newHander)
        for tr in replyPage.find_all('tr'):
            newHanderName=replyPage.new_tag('th')
            newHanderName.string=('Код')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('НАИМЕНОВАНИЕ')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('КОРПУС')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('КОЛИЧЕСТВО')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('МЕСТО ХРАНЕНИЯ')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('PART-НОМЕР')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('НАПРЯЖЕНИЕ')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('Списать/Внести')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('Списание')
            tr.append(newHanderName)
            newHanderName = replyPage.new_tag('th')
            newHanderName.string = ('Примечания')
            tr.append(newHanderName)
        while t<len(Req):
            inputData = replyPage.new_tag('tr')
            inputData.insert(2, replyPage.new_tag('inputData'+str(t)))
            tg.append(inputData)
            for tg in replyPage.find_all('inputData'+str(t)):
                newData=replyPage.new_tag('td')
                newData.string=str(Req[t][0])
                tg.append(newData)
                newData = replyPage.new_tag('td')
                newData.string = str(Req[t][1])
                tg.append(newData)
                newData = replyPage.new_tag('td')
                newData.string = str(Req[t][2])
                tg.append(newData)
                newData = replyPage.new_tag('td')
                if not str(Req[t][3])=='None' or '':
                    newData.string = str(Req[t][3])
                    tg.append(newData)
                else:
                    newData.string = '-'
                    tg.append(newData)
                newData = replyPage.new_tag('td')
                if not str(Req[t][4]) == 'None' or '':
                    newData.string = str(Req[t][4])
                    tg.append(newData)
                else:
                    newData.string = '-'
                    tg.append(newData)
                newData = replyPage.new_tag('td')
                if not str(Req[t][6]) == 'None' or '':
                    newData.string = str(Req[t][6])
                    tg.append(newData)
                else:
                    newData.string = '-'
                    tg.append(newData)
                newData = replyPage.new_tag('td')
                if not str(Req[t][7]) == 'None' or '':
                    newData.string = str(Req[t][7])
                    tg.append(newData)
                else:
                    newData.string = '-'
                    tg.append(newData)
                if foundOK:
                    curCh = numCh.split('+')
                    newData = replyPage.new_tag('td')
                    newFormIn = replyPage.new_tag('form')
                    if curCh[0]==str(t):
                        newFormIn['action'] = ('http://192.168.0.103:3000/output/' + str(Req[t][1]) +
                                               '+' + str(Req[t][2]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(int(curCh[1])-1))
                    else:
                        newFormIn['action'] = ('http://192.168.0.103:3000/output/' + str(Req[t][1]) +
                                '+' + str(Req[t][2]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(-1))

                    newFormIn['method']='action'
                    newBotIn = replyPage.new_tag('button')
                    newBotIn.string = 'Списать'
                    newFormIn.insert(2, newBotIn)
                    newData.insert(2, newFormIn)
                    numCompEdit = replyPage.new_tag('p')
                    if curCh[0]==str(t):
                            if not Req[t][4]=='0':
                                numCompEdit.string = curCh[1]
                    else:
                            numCompEdit.string = '0'
                    newData.insert(3, numCompEdit)
                    # tg.append(newData)
                    # newData = replyPage.new_tag('td') encoding='utf-8'
                    newFormOut = replyPage.new_tag('form')
                    if curCh[0] == str(t):
                        newFormOut['action'] = ('http://192.168.0.103:3000/input/' + str(Req[t][1]) +
                                '+' + str(Req[t][2]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(int(curCh[1])+1))
                    else:
                        newFormOut['action'] = ('http://192.168.0.103:3000/input/' + str(Req[t][1]) +
                                '+' + str(Req[t][2]) + '+' + str(reqestInfo) + '+' + str(t) + '+' + str(+1))

                    newFormOut['method'] = 'action'
                    newBotOut = replyPage.new_tag('button')
                    newBotOut.string = 'Внести'
                    newFormOut.insert(2,newBotOut)
                    newData.insert(2, newFormOut)
                    tg.append(newData)
                    newData = replyPage.new_tag('td')
                    newFormFew = replyPage.new_tag('form')
                    newFormFew['method']='action'
                    newFormFew['action']=('http://192.168.0.103:3000/output/' + str(Req[t][1]) +
                                '+' + str(Req[t][2]) + '+' + str(reqestInfo))
                    newField=replyPage.new_tag('input')
                    newField['name']='pcs'
                    newField['type']='search'
                    newField['pattern']='^[ 0-9]+$'
                    newField['placeholder']='Списать'
                    newField['required']=''
                    newFormFew.insert(2,newField)
                    newField = replyPage.new_tag('input')
                    newField['type'] = 'submit'
                    newFormFew.insert(2, newField)
                    newData.insert(2,newFormFew)
                    tg.append(newData)
                    newFormFew = replyPage.new_tag('form')
                    newFormFew['method'] = 'action'
                    newFormFew['action'] = ('http://192.168.0.103:3000/input/' + str(Req[t][1]) +
                                            '+' + str(Req[t][2]) + '+' + str(reqestInfo))
                    newField = replyPage.new_tag('input')
                    newField['name'] = 'pcs'
                    newField['type'] = 'search'
                    newField['pattern'] = '^[ 0-9]+$'
                    newField['placeholder'] = 'Внести'
                    newField['required'] = ''
                    newFormFew.insert(2, newField)
                    newField = replyPage.new_tag('input')
                    newField['type'] = 'submit'
                    newFormFew.insert(2, newField)
                    newData.insert(2, newFormFew)
                    tg.append(newData)
                    newData = replyPage.new_tag('td')
                    if not str(Req[t][8]) == 'None' or '':
                        newData.string = str(Req[t][8])
                        tg.append(newData)
                    else:
                        newData.string = '-'
                        tg.append(newData)

            t+=1
    replyPage.prettify(formatter="html")
    f = open('templates/reply.html', 'w', encoding='utf-8')
    
    f.write(str(replyPage))
    f.close()
    return

