from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def chart():
    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    values = [12, 19, 3, 5, 2, 3]
    return render_template('chart.html', values=values, labels=labels)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
