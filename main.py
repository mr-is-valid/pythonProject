from flask import Flask, render_template , url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3

app = Flask('pythonProject')
# print("Database opened successfully")
# con.execute("create table Elements(id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL)")
# con.execute("create table Events(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,description TEXT,cordX REAL NOT NULL ,cordY REAL NOT NULL ,dateCreate TEXT, timeCreate TEXT ,type INTEGER, FOREIGN KEY(type) REFERENCES Elements(id))")
# print("Tables created successfully")

@app.route("/insertEvent",methods = ['POST', 'GET'])
def insertEvent():
    eventName = request.form.get('eventName')
    selectValueType = request.form.get('elements')
    description = request.form.get('description')
    cordX = request.form.get('cordX')
    cordY = request.form.get('cordY')
    dateCreate = datetime.now().strftime("%d/%m/%Y")
    timeCreate = datetime.now().strftime("%H:%M:%S")

    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute(f"INSERT INTO Events(name, description, cordX, cordY,dateCreate,timeCreate ,typeID) VALUES ('{eventName}',"
                          f"'{description}', {cordX},{cordY},'{dateCreate}', '{timeCreate}',{selectValueType});")
    con.commit()
    return redirect('/')

@app.route("/addEvent")
def addEvent():
    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute("select * from Elements")
    data = pointer_to_db.fetchall()
    return render_template('addEvent.html',data=data)

@app.route("/updateEvent/<int:itemId>", methods=['GET', 'POST'])
def updateEvent(itemId):
    print(itemId)
    eventName = request.form.get('eventName')
    selectValueType = request.form.get('elements')
    description = request.form.get('description')
    cordX = request.form.get('cordX')
    cordY = request.form.get('cordY')

    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute(f"UPDATE Events SET name='{eventName}',description='{description}' ,cordX={cordX},cordY={cordY},typeID={selectValueType} WHERE id = " + str(itemId))
    con.commit()
    pointer_to_db.execute("select * from Events INNER JOIN Elements ON Events.typeID = Elements.id;")
    data = pointer_to_db.fetchall()
    return render_template('listView.html',data=data)


@app.route("/updateEventFromMap/<int:itemId>", methods=['GET', 'POST'])
def updateEventFromMap(itemId):
    print(itemId)
    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute("SELECT * FROM Events INNER JOIN Elements ON Events.typeID = Elements.id WHERE Events.id = " + str(itemId))
    dataItem = pointer_to_db.fetchall()[0]
    con.commit()
    pointer_to_db.execute("select * from Elements")
    data = pointer_to_db.fetchall()
    con.commit()
    return render_template('update.html',dataItem=dataItem,data=data)

@app.route('/editEvent/<int:itemId>', methods=['GET', 'POST'])
def editEvent(itemId):
    print(itemId)
    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute("SELECT * FROM Events INNER JOIN Elements ON Events.typeID = Elements.id WHERE Events.id = " + str(itemId))
    dataItem = pointer_to_db.fetchall()[0]
    con.commit()
    pointer_to_db.execute("select * from Elements")
    data = pointer_to_db.fetchall()
    con.commit()
    return render_template('update.html',dataItem=dataItem,data=data)

@app.route("/deleteEvent/<int:itemId>",methods = ['POST', 'GET'])
def delete(itemId):
    print(itemId)
    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute("DELETE FROM Events WHERE id = " + str(itemId))
    pointer_to_db.execute("select * from Events INNER JOIN Elements ON Events.typeID = Elements.id;")
    data = pointer_to_db.fetchall()
    con.commit()
    return render_template('listView.html', data=data)


@app.route("/deleteEventFromMap/<int:itemId>",methods = ['POST', 'GET'])
def deleteEventFromMap(itemId):
    print(itemId)
    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute("DELETE FROM Events WHERE id = " + str(itemId))
    pointer_to_db.execute("select Events.typeID,Elements.type as element, COUNT(*) as amount from Events INNER JOIN Elements ON Events.typeID = Elements.id GROUP BY typeID;")
    satistices = pointer_to_db.fetchall()
    pointer_to_db.execute("select * from Events INNER JOIN Elements ON Events.typeID = Elements.id;")
    data = pointer_to_db.fetchall()
    con.commit()
    return render_template('index.html', data=data, satistices=satistices)

@app.route("/listView",methods = ['POST', 'GET'])
def listView():
    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute("select * from Events INNER JOIN Elements ON Events.typeID = Elements.id;")
    data = pointer_to_db.fetchall()
    return render_template('listView.html', data=data)

#how much i have from each event type:
#need to do apexcharts
#select Events.typeID,Elements.type, COUNT(*) as amount from Events INNER JOIN Elements ON Events.typeID = Elements.id GROUP BY typeID;

@app.route("/",methods = ['POST', 'GET'])
def index():
    con = sqlite3.connect("eventmap.db")
    con.row_factory = sqlite3.Row
    pointer_to_db = con.cursor()
    pointer_to_db.execute("select Events.typeID,Elements.type as element, COUNT(*) as amount from Events INNER JOIN Elements ON Events.typeID = Elements.id GROUP BY typeID;")
    satisticesPieChart = pointer_to_db.fetchall()
    # for row in satisticesPieChart:
    #     print(f"{row['element']}, {row['amount']}.")
    pointer_to_db.execute("select dateCreate, COUNT(*) as amount from Events INNER JOIN Elements ON Events.typeID = Elements.id GROUP BY dateCreate;")
    satisticesBarChart = pointer_to_db.fetchall()
    # for row in satisticesBarChart:
    #     print(f"{row['dateCreate']}, {row['amount']}.")
    pointer_to_db.execute("select * from Events INNER JOIN Elements ON Events.typeID = Elements.id;")
    data = pointer_to_db.fetchall()
    # for row in data:
    #     print(f"{row['name']}, {row['type']}.")
    return render_template('index.html', data=data, satisticesPieChart=satisticesPieChart,satisticesBarChart=satisticesBarChart)

if __name__ == "__main__":
    app.run()