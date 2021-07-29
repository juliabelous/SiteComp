import sqlite3 as sql

#Списать+МСХ+TPS 560430+SOT-23-6+21
tables = 'R', 'L', 'C', 'MC', 'MSH', 'TR', 'D', 'O'


def allTable(type):
    sqlBD=sql.connect('mainBase.db')
    with sqlBD:
        elements=sqlBD.cursor()
        elements.execute("CREATE TABLE IF NOT EXISTS `"+str(type)+"` (`barcode` STRING, `name` STRING, `body` STRING, `pcs` INT, `place` STRING, `res` STRING)")
        elements.execute("SELECT * FROM `"+str(type)+"`")
        elements=elements.fetchall()
        return elements


def searchComp(nameComp):
    result=list()
    sqlBD = sql.connect('mainBase.db')
    with sqlBD:
        for captain in tables:
            elements = sqlBD.cursor()
            #elements.execute("CREATE TABLE IF NOT EXISTS `" + str(captain) + "` (`barcode` STRING, `name` STRING, `body` STRING, `pcs` INT, `place` STRING, `res` STRING)")
            elements.execute("SELECT * FROM '"+str(captain)+"' WHERE `name` LIKE '%"+str(nameComp)+"%'")
            elements=elements.fetchall()
            for r in elements:
                result.append(r)

        return result


def outputComp(name,body,pcsUser,req):
    result=list()
    sqlBD = sql.connect('mainBase.db')
    with sqlBD:
        for captain in tables:
            elements = sqlBD.cursor()
            elements.execute("UPDATE "+str(captain)+" SET pcs=pcs+("+str(pcsUser)+") WHERE (`name`= '"+str(name)+"' AND `body` = '"+str(body)+"')")
            elements.execute("SELECT * FROM `"+str(captain)+"` WHERE `name` LIKE '%" + req + "%'")
            elements=elements.fetchall()
            for r in elements:
                result.append(r)
        return result



# def inputComp(name,body,pcsUser,req):
#     result=list()
#     sqlBD = sql.connect('test.db')
#     with sqlBD:
#         for captain in tables:
#             elements = sqlBD.cursor()
#             # elements.execute("UPDATE "+str(captain)+" SET pcs=pcs+("+str(pcsUser)+") WHERE `name`= '"+str(name)+"' AND body="+str(body))
#             # elements.execute("SELECT * FROM `"+str(captain)+"` WHERE `name` LIKE '%" + req + "%'")
#             elements=elements.fetchall()
#             for r in elements:
#                 result.append(r)
#         return result


def inputComp(newComp):
    sqlBD = sql.connect('mainBase.db')
    with sqlBD:
        elements=sqlBD.cursor()
        elements.execute("INSERT INTO `"+str(newComp[5])+
                         "` VALUES ('"+str(newComp[0])+"', '"+
                         str(newComp[1])+"','"+str(newComp[2])+"','"+
                         str(newComp[3])+"','"+str(newComp[4])+"','0','"+str(newComp[6])+"', "+"' "+str(newComp[7])+"', '"+str(newComp[8])+"' )")
        elements.fetchall()
    return


def newBarcode():
    sqlBD = sql.connect('mainBase.db')
    results = list()
    with sqlBD:
        for i in tables:
            elements = sqlBD.cursor()
            elements.execute("SELECT barcode FROM " + str(i))
            elements = elements.fetchall()

        for n in elements:
            results.append(int(n[0]))
            lostbc = (sorted(results))[-1]+1
    return lostbc

