from flask import Flask
from flask import render_template
import sqlite3
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
    return render_template('dashboard.html', accounts=accounts)


@app.route("/monthly")
def monthly():
    query = '''
        SELECT parent_id, v_report_category._id, v_report_category.name, SUM(from_amount), symbol, strftime('%m.%Y', datetime(datetime/1000, 'unixepoch', 'localtime')) as Month
        FROM v_report_category
        LEFT JOIN currency ON currency._id = v_report_category.from_account_currency_id
        GROUP BY v_report_category.name, Month
        ORDER BY v_report_category.name
    '''
    conn = sqlite3.connect('databases/financisto.db', check_same_thread=False)
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()

    # categories = OrderedDict()
    # for item in result:
    #     children = OrderedDict()
    #     children[item[1]] = item
    #     if item[0] in categories.keys():
    #         categories[item[0]].append(children)
    #     else:
    #         categories[item[0]] = [children]
    #
    # result = categories
    return render_template('monthly.html', result=result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
