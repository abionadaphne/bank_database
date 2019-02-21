import flask

from flask import render_template, url_for, flash, redirect, request
from flask import request, jsonify
import sqlite3
import os.path
from forms import ifsc_filter
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bank.db")
DATABASE = 'C:\\Users\Win 10\projects\bank\api\bank.db'
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Rest Service</h1><p>REST APIs are created for fetching from Sqlite Database .</p><br><br><a href="http://127.0.0.1:5000/api/v1/resources/bank/all">To display every bank detail !!</a><br><br><a href="http://127.0.0.1:5000/api/v1/resources/bank?ifsc=ABHY0065001">To get branch details by replacing required IFSC code in the url!!</a><br><br><a href="http://127.0.0.1:5000/api/v1/resources/bank?bank_name=ABHYUDAYA+COOPERATIVE+BANK+LIMITED&city=MUMBAI"> Replace Bank Name and City in the url to get all corresponding branch details</a>'''
			    
		    
    #return render_template("home.html",title="home")
#def get_name():
    #form=ifsc_filter()
    #ifsc_data=form.ifsc.data
    #query = "SELECT *  FROM bank WHERE ifsc='" + ifsc_data + "';"

    #connection = sqlite3.connect(database_file)
    #cursor = connection.cursor()
    #cursor.execute(query)
    #results = cursor.fetchall()
    #cursor.close()
    #connection.close()

    #return results[0][0]


@app.route('/api/v1/resources/bank/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('C:\\Users\\Win 10\\projects\\bank\\api\\bank.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM bank;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/bank', methods=['GET'])
def api_filter():
    query_parameters = request.args

    ifsc = query_parameters.get('ifsc')
    bank_id = query_parameters.get('bank_id')
    branch = query_parameters.get('branch')
    address = query_parameters.get('address')
    city = query_parameters.get('city')
    bank_name = query_parameters.get('bank_name')

    query = "SELECT * FROM bank WHERE"
    to_filter = []

    if ifsc:
        query += ' ifsc=? AND'
        to_filter.append(ifsc)
    if bank_id:
        query += ' bank_id=? AND'
        to_filter.append(bank_id)
    if branch:
        query += ' branch=? AND'
        to_filter.append(branch)
    if address:
        query += ' address=? AND'
        to_filter.append(address)
    if city:
        query += ' city=? AND'
        to_filter.append(city)
    if bank_name:
        query += ' bank_name=? AND'
        to_filter.append(bank_name)
    if not (ifsc or bank_id or branch or address or city or bank_name):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('bank.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()