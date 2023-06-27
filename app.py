from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os

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
    n = ""
    if request.method == "POST":
        count = request.form.get('count')

        query = "SELECT * FROM dbo.all_month WHERE mag>?"
        cursor.execute(query, count)

        rows = cursor.fetchall()
        for i in rows:
            salpics.append(i)

        query2 = "SELECT COUNT(id) FROM dbo.all_month WHERE mag>?"
        cursor.execute(query2, count)
        num = cursor.fetchone()
        n = num[0]
    return render_template("1)count.html", count=count, salpics=salpics, n=n)


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
        query = f"SELECT * FROM dbo.all_month WHERE mag BETWEEN ? AND ? AND CAST(time AS DATE) BETWEEN '2023-06-01' AND '2023-06-{days}'"
        cursor.execute(query, min, max)
        row = cursor.fetchall()
        if row is None:
            system = None
        else:
            for i in row:
                salpics.append(i)
    return render_template("2)range.html", range=range, salpics=salpics, system=system)


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
    return render_template("3)distance.html", salpics=salpics, distance=distance)


@app.route("/cluster/", methods=['GET', 'POST'])
def cluster():
    salpics = []
    count = ""
    n = ""
    if request.method == "POST":
        count = request.form.get('count')

        query = "SELECT * FROM dbo.all_month WHERE mag=?"
        cursor.execute(query, count)

        rows = cursor.fetchall()
        for i in rows:
            salpics.append(i)

        query2 = "SELECT COUNT(id) FROM dbo.all_month WHERE mag=?"
        cursor.execute(query2, count)
        num = cursor.fetchone()
        n = num[0]
    return render_template("4)cluster.html", count=count, salpics=salpics, n=n)


@app.route("/time/", methods=['GET', 'POST'])
def time():
    query = "SELECT CASE WHEN DATEPART(HOUR, [time]) >= 18 OR DATEPART(HOUR, [time]) < 6 THEN 'Night-time (6 PM - 6 AM)' ELSE 'Day-time (6 AM - 6 PM)' END AS time_range, COUNT(*) AS earthquake_count FROM [dbo].[all_month] WHERE mag > 4 GROUP BY CASE WHEN DATEPART(HOUR, [time]) >= 18 OR DATEPART(HOUR, [time]) < 6 THEN 'Night-time (6 PM - 6 AM)' ELSE 'Day-time (6 AM - 6 PM)' END"
    cursor.execute(query)
    count = cursor.fetchall()
    night_count=count[1]
    day_count = count[0]
    return render_template("5)time.html", night_count=night_count[1], day_count=day_count[1])


if __name__ == "__main__":
    app.run(debug=True)
