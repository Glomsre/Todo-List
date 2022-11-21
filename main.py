from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
import os
import csv

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    try:
        with open('my-list-data.csv', encoding="utf8") as csv_file:
            csv.reader(csv_file)
    except:
        with open('my-list-data.csv', encoding='utf8', mode='w') as file:
            file.write('')

    return redirect('/mylist')


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        thing_to_do = request.form.get('todo')
        with open('my-list-data.csv', encoding='utf8', mode='a') as file:
            file.write(f'{thing_to_do}\n')
        return redirect('/mylist')

    return render_template("index.html")


@app.route('/mylist', methods=["GET", "POST"])
def mylist():
    with open('my-list-data.csv', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file)

        lists = []
        for row in csv_data:
            lists.append(row)
    return render_template("index.html", lists=lists)


@app.route('/delete')
def delete():
    current_l = request.args.get('current_l')
    with open('my-list-data.csv', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file)

        lists = []
        for row in csv_data:
            lists.append(row)

        lists_b = []
        for item in lists:
            lists_b.append(item[0])

        for item in lists_b:
            if item == current_l:
                lists_b.remove(current_l)

    lists = lists_b

    file = 'my-list-data.csv'
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)

    with open('my-list-data.csv', encoding='utf8', mode='a') as file:
        for item in lists:
            file.write(f'{item}\n')

    return redirect('/mylist')


@app.route('/restart')
def restart():
    file = 'my-list-data.csv'
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        print("file deleted")

    with open('my-list-data.csv', encoding='utf8', mode='w') as file:
        file.write('')

    return redirect('/mylist')


if __name__ == '__main__':
    app.run(debug=True)
