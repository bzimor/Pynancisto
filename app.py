from flask import Flask
from flask import render_template
import sqlite3
app = Flask(__name__)


@app.route("/")
def chart():
    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    values = [12, 19, 3, 5, 2, 3]
    query = 'SELECT * FROM v_report_payee ORDER BY name'
    conn = sqlite3.connect('databases/financisto.db', check_same_thread=False)
    c = conn.cursor()
    c.execute(query)
    payees = list(c.fetchall())
    return render_template('chart.html', values=values, labels=labels, payees=payees)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
