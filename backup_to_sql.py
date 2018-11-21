import os
import glob
import gzip
import database as db
from collections import OrderedDict


# Opens backup file in backups folder and creates row list
def readFile():
    backup_files = glob.glob('backups/*.backup')
    # get latest backup file
    latest_backup_file = max(backup_files, key=os.path.getctime)
    if latest_backup_file:
        myfile = gzip.open(latest_backup_file, 'rt').read()
        rows = myfile.splitlines()
        return rows
    return False


# get all Entity names
def getEntities():
    rows = readFile()
    if rows:
        entity_list = sorted(list(set([row.replace('$ENTITY:', '') for row in rows if row.startswith('$ENTITY')])))
        return entity_list
    return False


# get Entity attributes and values
def getEntityItems(n):
    rows = readFile()
    tables = getEntities()
    entity_start = '$ENTITY:' + tables[n-1]
    is_current = False
    start = False
    itemDict = OrderedDict()
    for row in rows:
        if row == entity_start:
            is_current = True
            if row == '$ENTITY:category_attribute':
                start = True
            continue
        if row != '$$' and is_current and not row.startswith('resolved_address:') and not row.startswith('card_issuer:'):
            # transaction id
            if row.startswith('_id:'):
                idnum = row[4:]
                temdpdict = OrderedDict()
            # transaction attribute
            elif row.startswith('transaction_id:'):
                idnum = row[15:]
                temdpdict = OrderedDict()
            # currency_exchange_rate
            elif row.startswith('from_currency_id:'):
                idnum = row[17:]
                temdpdict = OrderedDict()
            elif row.startswith('category_id:') and start:
                idnum = row[12:]
                temdpdict = OrderedDict()
            else:
                templist = row.split(':')
                temdpdict[templist[0]] = templist[1]
                itemDict[idnum] = temdpdict
        elif row.startswith('resolved_address:') or row.startswith('card_issuer:'):
            continue
        else:
            is_current = False
            start = False
    return itemDict


# writes extracted data to database
def writeData():
    if not os.path.isfile('databases/financisto.db'):
        db.createTables()
    tbl = getEntities()
    tbllen = len(tbl)
    for j in range(tbllen):
        print(tbl[j])
        mydict = getEntityItems(j+1)
        for k, v in mydict.items():
            itemList = [k]
            fieldlist = []
            if tbl[j] == 'category_attribute':
                fieldlist.append('"category_id"')
            elif tbl[j] == 'transaction_attribute':
                fieldlist.append('"transaction_id"')
            elif tbl[j] == 'currency_exchange_rate':
                fieldlist.append('"from_currency_id"')
            else:
                fieldlist.append('"_id"')
            for k2, v2 in mydict[k].items():
                itemList.append(v2)
                fieldlist.append('"'+k2+'"')
            fields = ', '.join(fieldlist)

            values = tuple(itemList)
            lnth = len(values)
            qrytxt = "?"
            for i in range(lnth-1):
                qrytxt = qrytxt + "," + "?"

            query = "INSERT OR IGNORE INTO " + tbl[j] + "(" + fields + ")" + " VALUES " + "(" + qrytxt + ")"
            db.writeQuery(values, query)


writeData()
