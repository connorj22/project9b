from peewee import *
from flask import Flask
from flask import request
from flask import jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from flask import render_template


db = PostgresqlDatabase('contactbook', user='connorharris', password='12345',
                        host='localhost', port=5432)


def Connect():
    db.connect()
    print("Connected to database")
    return 0


Connect()


class BaseModel(Model):
    class Meta:
        database = db


class Contacts(BaseModel):
    name = CharField()
    phoneNumber = CharField()
    note = CharField()


db.create_tables([Contacts])
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/contacts/', methods=['GET', 'POST'])
@app.route('/contacts/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Contacts.get(Contacts.id == id)))
        else:
            people_list = []
            for person in Contacts.select():
                people_list.append(model_to_dict(person))
            return jsonify(people_list)

    if request.method == 'PUT':
        body = request.get_json()
        Contacts.update(body).where(Contacts.id == id).execute()
        return "Contact " + str(id) + " has been updated."

    if request.method == 'POST':
        new_contact = dict_to_model(Contacts, request.get_json())
        new_contact.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Contacts.delete().where(Contacts.id == id).execute()
        return "Contact " + str(id) + " deleted."


app.run(port=3000, debug=True)
