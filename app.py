from flask import Flask
from flask import render_template
import sqlite3
# from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)


@app.route("/")
def dashboard():
    query = '''
        SELECT account.title, total_amount, symbol, is_active, account.type
        FROM account
        LEFT JOIN currency ON currency._id = account.currency_id
        ORDER BY is_active DESC, sort_order DESC
    '''
    conn = sqlite3.connect('databases/financisto.db', check_same_thread=False)
    c = conn.cursor()
    c.execute(query)
    accounts = c.fetchall()
    tab = {'active': 'home'}
    return render_template('dashboard.html', tab=tab, accounts=accounts)


@app.route("/monthly")
def monthly():
    # dt_obj = datetime.strptime('01.01.2018', '%d.%m.%Y')
    # millisec = int(dt_obj.timestamp() * 1000)
    query = '''
        SELECT parent_id, v_report_category._id, v_report_category.name,
            SUM(CASE WHEN from_account_currency_id = 2 THEN from_amount * 8200 ELSE from_amount END) as amount,
            CASE WHEN from_amount < 0 THEN 1 ELSE 0 END as is_expense,
            symbol, strftime('%m/%Y', datetime(datetime/1000, 'unixepoch', 'localtime')) as month, MIN(category_left) as cat
        FROM v_report_category
        LEFT JOIN currency ON currency._id = v_report_category.from_account_currency_id
        GROUP BY v_report_category.name, month
        ORDER BY is_expense, cat, parent_id, v_report_category.name
    '''
    conn = sqlite3.connect('databases/financisto.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()

    query = '''
        SELECT strftime('%m/%Y', datetime(datetime/1000, 'unixepoch', 'localtime')) as month
        FROM v_report_category
        GROUP BY month
        ORDER BY `datetime`
    '''
    conn = sqlite3.connect('databases/financisto.db', check_same_thread=False)
    c = conn.cursor()
    c.execute(query)
    months = [i[0] for i in c.fetchall()]
    empty_dict = dict()
    for i in months:
        empty_dict[i] = {}
    categories = OrderedDict()
    for item in result:
        if item['_id'] not in categories.keys():
            category_item = empty_dict.copy()
            categories[item['_id']] = {'name': item['name'], 'parent_id': item['parent_id'], 'id': item['_id'], 'data': category_item}
        categories[item['_id']]['data'][item['month']] = item
    result = categories
    tab = {'active': 'monthly'}
    return render_template('monthly.html', tab=tab, result=result, months=months)


@app.route("/payee")
def payee():
    # dt_obj = datetime.strptime('01.01.2018', '%d.%m.%Y')
    # millisec = int(dt_obj.timestamp() * 1000)
    query = '''
        SELECT v_report_payee._id, v_report_payee.name,
            SUM(CASE WHEN from_account_currency_id = 2 THEN from_amount * 8200 ELSE from_amount END) as amount
        FROM v_report_payee
        LEFT JOIN currency ON currency._id = v_report_payee.from_account_currency_id
        WHERE from_amount > 0
        GROUP BY v_report_payee.name
        ORDER BY amount DESC, v_report_payee.name
    '''
    conn = sqlite3.connect('databases/financisto.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    income_amounts = ', '.join([str(item['amount']/100) for item in result])
    income_payees = ', '.join(['"' + item['name'] + '"' for item in result])

    query = '''
        SELECT v_report_payee._id, v_report_payee.name,
            SUM(CASE WHEN from_account_currency_id = 2 THEN from_amount * 8200 ELSE from_amount END) as amount
        FROM v_report_payee
        LEFT JOIN currency ON currency._id = v_report_payee.from_account_currency_id
        WHERE from_amount < 0
        GROUP BY v_report_payee.name
        ORDER BY amount, v_report_payee.name
    '''
    c.execute(query)
    result = c.fetchall()
    expense_amounts = ', '.join([str(item['amount']/100*-1) for item in result])
    expense_payees = ', '.join(['"' + item['name'] + '"' for item in result])

    query = '''
        SELECT v_report_payee._id, v_report_payee.name,
            SUM(CASE WHEN from_account_currency_id = 2 THEN from_amount * 8200 ELSE from_amount END) as amount
        FROM v_report_payee
        LEFT JOIN currency ON currency._id = v_report_payee.from_account_currency_id
        GROUP BY v_report_payee.name
        HAVING SUM(CASE WHEN from_account_currency_id = 2 THEN from_amount * 8200 ELSE from_amount END) <> 0
        ORDER BY amount, v_report_payee.name
    '''
    c.execute(query)
    result = c.fetchall()
    total_amounts = ', '.join([str(item['amount']/100) for item in result])
    total_payees = ', '.join(['"' + item['name'] + '"' for item in result])

    tab = {'active': 'payee'}
    return render_template('payee.html', tab=tab, income_amounts=income_amounts, income_payees=income_payees,
                           expense_amounts=expense_amounts, expense_payees=expense_payees,
                           total_amounts=total_amounts, total_payees=total_payees)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
