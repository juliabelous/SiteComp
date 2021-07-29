#!/bin/python3
from flask import Flask, render_template
import HTML, logging, logging.handlers, SQL_HANDLER, json
from flask import request

typeDict = dict()
typeDict['R'] = 'резистор'
typeDict['L'] = 'индуктивность'
typeDict['C'] = 'конденсатор'
typeDict['MC'] = 'микроконтроллеры'
typeDict['MSH'] = 'микросxемы'
typeDict['TR'] = 'транзисторы'
typeDict['D'] = 'диоды'
typeDict['O'] = 'прочее'

typeDictKey=dict()
typeDictKey['резистор'] = 'R'
typeDictKey['индуктивность'] = 'L'
typeDictKey['конденсатор'] = 'C'
typeDictKey['микроконтроллеры'] = 'MC'
typeDictKey['микросxемы'] = 'MSH'
typeDictKey['транзисторы'] = 'TR'
typeDictKey['диоды'] = 'D'
typeDictKey['прочее'] = 'O'



f = open('log.txt', 'w')
f.close()
app = Flask(__name__, static_folder='/home/pi/SiteComp/table_comp/static')

handler = logging.handlers.RotatingFileHandler(
        'log.txt',
        maxBytes=1024 * 1024)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.WARNING)
app.logger.addHandler(handler)
app.logger.addHandler(handler)




@app.route('/log')
def logPage():
    log=open('log.txt','r').readlines()
    return "<html> <body>"+ ('\n<p>'.join(log)) + "</body> </html>"


@app.route('/search/', methods=['GET', 'POST'])
def parse_request():
    if request.args.get("comp")=='':
        return render_template('index.html')
    infoOut=SQL_HANDLER.searchComp(request.args.get("comp"))
    HTML.createTableSQL(infoOut, '0+0', True, request.args.get('comp'))
    return render_template('reply.html')


@app.route('/')
def startPage():
    return render_template('index.html')


@app.route('/output/<compName>')
def outputComOut(compName):
    compName = compName.split('+')
    if not len(compName) == 3:
        check = typeDictKey.get(str(compName[2]).lower(), 'None')
        if check == 'None':
            infoOut = SQL_HANDLER.outputComp(compName[0], compName[1], -1, compName[2])
        else:
            SQL_HANDLER.outputComp(compName[0], compName[1], -1, compName[2])
            infoOut = SQL_HANDLER.allTable(typeDictKey[str(compName[2]).lower()])
        HTML.createTableSQL(infoOut, (str(compName[3]) + '+' + str(compName[4])), True, compName[2])
        return render_template('reply.html')
    else:
        check = typeDictKey.get(str(compName[2]).lower(), 'None')
        if check == 'None':
            infoOut = SQL_HANDLER.outputComp(compName[0], compName[1], 0-int(request.args.get("pcs")), compName[2])
        else:
            SQL_HANDLER.outputComp(compName[0], compName[1], 0-int(request.args.get("pcs")), compName[2])
            infoOut = SQL_HANDLER.allTable(typeDictKey[str(compName[2]).lower()])
        HTML.createTableSQL(infoOut, '0+0', True, compName[2])
        return render_template('reply.html')




@app.route('/input/<compName>',methods=['GET', 'POST'])
def outputComIn(compName):
    compName = compName.split('+')
    if not len(compName) == 3:
        check = typeDictKey.get(str(compName[2]).lower(), 'None')
        if check == 'None':
            infoOut = SQL_HANDLER.outputComp(compName[0], compName[1], 1, compName[2])
        else:
            SQL_HANDLER.outputComp(compName[0], compName[1], 1, compName[2])
            infoOut = SQL_HANDLER.allTable(typeDictKey[str(compName[2]).lower()])
        HTML.createTableSQL(infoOut, (str(compName[3]) + '+' + str(compName[4])), True, compName[2])
        return render_template('reply.html')
    else:
        check = typeDictKey.get(str(compName[2]).lower(), 'None')
        if check == 'None':
            infoOut = SQL_HANDLER.outputComp(compName[0], compName[1], request.args.get("pcs"), compName[2])
        else:
            SQL_HANDLER.outputComp(compName[0], compName[1], request.args.get("pcs"), compName[2])
            infoOut = SQL_HANDLER.allTable(typeDictKey[str(compName[2]).lower()])
        HTML.createTableSQL(infoOut, '0+0', True, compName[2])
        return render_template('reply.html')




@app.route('/all/<type>')
def typeALL(type):
    infoOut=SQL_HANDLER.allTable(type)
    HTML.createTableSQL(infoOut,'0+0', True, typeDict[type].upper())
    return render_template('reply.html')

# печаные платы запуск

@app.route('/all/PCB')
def pCb():
    return render_template('pcb.html')


@app.route('/new')
def newPages():
    return render_template('newComp.html')


@app.route('/new/', methods=['GET', 'POST'])
def newPagesAdd():
    newComp=list()
    newComp.append(request.args.get("barcode"))
    newComp.append(request.args.get("name"))
    newComp.append(request.args.get("body"))
    newComp.append(request.args.get("pcs"))
    newComp.append(request.args.get("place"))
    newComp.append(request.args.get("type"))
    newComp.append(request.args.get("part"))
    newComp.append(request.args.get("volt"))
    newComp.append(request.args.get("prim"))
    
    newComp.append(request.args.get("version"))
    newComp.append(request.args.get("git"))
    newComp.append(request.args.get("date"))
    
    
    SQL_HANDLER.inputComp(newComp)
    return render_template('newComp.html')



@app.route('/barCode')
def barcodePage():
    lastbc=SQL_HANDLER.newBarcode()
    return str(lastbc)



@app.errorhandler(404)
def errorReply(error):
    return render_template('error.html')


@app.errorhandler(500)
def errorReply(error):
    return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True, port=3000, host='0.0.0.0')
