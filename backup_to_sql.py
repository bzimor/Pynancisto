import gzip
from Databases import *
from collections import OrderedDict

def readFile():
    myfile = gzip.open('20161210_172806_453.backup', 'rt').read()
    myfile = myfile.splitlines()
    return myfile

def getTableList():
    myfile = readFile()
    tableList = sorted(list(set([word.replace('$ENTITY:','') for word in myfile if word.startswith('$ENTITY')])))
    return tableList

def getTableItems(n):
    myfile = readFile()
    tables = getTableList()
    txt = '$ENTITY:' + tables[n-1]
    chk = False
    chk2 = False
    itemDict = OrderedDict()
    for word in myfile:
        if word == txt:
            chk = True
            if word == '$ENTITY:category_attribute':
                chk2 = True
            continue
        if word != '$$' and chk and not word.startswith('resolved_address:') and not word.startswith('card_issuer:'):
            if word.startswith('_id:'):
                idnum = word[4:]
                temdpdict = OrderedDict()
            elif word.startswith('transaction_id:'):
                idnum = word[15:]
                temdpdict = OrderedDict()
            elif word.startswith('from_currency_id:'):
                idnum = word[17:]
                temdpdict = OrderedDict()
            elif word.startswith('category_id:') and chk2:
                idnum = word[12:]
                temdpdict = OrderedDict()
            else:
                templist = word.split(':')
                temdpdict[templist[0]] = templist[1]
                itemDict[idnum]=temdpdict
        elif word.startswith('resolved_address:') or word.startswith('card_issuer:'):
            continue
        else:
            chk = False
            chk2 = False
    return itemDict

def getDictItems(s, item):
    itemList = []
    mydict = getTableItems(s)
    for k, v in mydict.items():
        for k2, v2 in mydict[k].items():
            if k2 == item:
                itemList.append(v2)
    print (itemList)



def writeData():
    createTables()
    tbl = getTableList()
    tbllen = len(tbl)
    for j in range(tbllen):
        print (tbl[j])
        mydict = getTableItems(j+1)
        for k, v in mydict.items():
            itemList = [k]
            for k2, v2 in mydict[k].items():
                itemList.append(v2)
            
            if tbl[j] == 'transactions' and len(itemList) == 21:
                itemList = itemList[:6] + [""] + itemList[6:]
                itemtuple = tuple(itemList)
                lnth = len(itemtuple)
            elif tbl[j] == 'transactions' and len(itemList) == 23:
                itemList = itemList[:10] + itemList[11:]
                itemtuple = tuple(itemList)
                lnth = len(itemtuple)
            else:
                itemtuple = tuple(itemList)
                lnth = len(itemtuple)
            qrytxt = "?"
            for i in range (lnth-1):
                qrytxt = qrytxt + "," + "?"
            
            query = "INSERT INTO " + tbl[j] +" VALUES " + "(" + qrytxt + ")"
            #print (qrytxt)
            #print (itemtuple)
            writeQuery(itemtuple, query)

def writeData1():
    #createTables()
    tbllen = len(getTableList())
    mydict = getTableItems(11)
    for k, v in mydict.items():
        itemList = [k]
        for k2, v2 in mydict[k].items():
             itemList.append(k2)
                
        itemtuple = tuple(itemList)
        lnth = len(itemtuple)
        if lnth == 24:
            print (itemtuple)
        qrytxt = "?"
        for i in range (lnth-2):
            qrytxt = qrytxt + "," + "?"
                
        query = "INSERT INTO payee VALUES (" + qrytxt + ")"
        #print (itemtuple)
        #writeQuery(itemtuple, query)
        


