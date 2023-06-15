from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

driver = '{ODBC Driver 17 for SQL Server}'
server = 'sqlserver-1002119262-saarthakmudigeregirish.database.windows.net'
database = 'DataBase-1002119262-SaarthakMudigereGirish'
username = 'saarthakmudigeregirish'
password = 'Hello123'

# Establish the connection
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Create a cursor object
cursor = conn.cursor()
print(cursor)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/count/", methods=['GET', 'POST'])
def picture():
    salpics = []
    count = ""
    if request.method == "POST":
        count = request.form.get('count')

        query = "SELECT * FROM dbo.all_month WHERE mag>?"
        cursor.execute(query, count)

        rows = cursor.fetchall()
        for i in rows:
            salpics.append(i)
    return render_template("count.html", count=count, salpics=salpics)


@app.route("/range/", methods=['GET', 'POST'])
def range():
    min = ""
    max = ""
    system = ""
    salpics = []
    days = ""
    if request.method == "POST":
        min = request.form['min']
        max = request.form['max']
        days = request.form['days']
        print(days)
        # Execute a simple select query
        query = f"SELECT TOP ({days}) * FROM dbo.all_month WHERE mag BETWEEN ? AND ?"
        cursor.execute(query, min, max)
        row = cursor.fetchall()
        if row is None:
            system = None
        else:
            for i in row:
                salpics.append(i)
    return render_template("range.html", range=range, salpics=salpics, system=system)


@app.route("/distance/", methods=['GET', 'POST'])
def distance():
    salpics = []
    distance = ""
    long = ""
    if request.method == "POST":
        lat = request.form['lat']
        long = request.form['long']
        distance = request.form['distance']

        query = "SELECT * FROM dbo.all_month WHERE ( 6371 * ACOS(COS(RADIANS(latitude)) * COS(RADIANS(?)) * COS(" \
                "RADIANS(longitude) - RADIANS(?)) + SIN(RADIANS(latitude)) * SIN(RADIANS(?)) )) <=? ; "
        cursor.execute(query, lat, long, lat, distance)
        row = cursor.fetchall()
        for i in row:
            salpics.append(i)
    return render_template("distance.html", salpics=salpics, distance=distance)



@app.route("/time/", methods=['GET', 'POST'])
def time():
    query1 = "SELECT COUNT(id) FROM dbo.all_month WHERE mag>4.0 AND CAST(time AS TIME) > '18:00:00'"
    cursor.execute(query1)
    night_count = cursor.fetchone()
    query2 = "SELECT COUNT(id) FROM dbo.all_month WHERE mag>4.0 AND CAST(time AS TIME) < '18:00:00'"
    cursor.execute(query2)
    day_count = cursor.fetchone()

    return render_template("time.html", night_count=night_count[0], day_count=day_count[0])


if __name__ == "__main__":
    app.run(debug=True)
