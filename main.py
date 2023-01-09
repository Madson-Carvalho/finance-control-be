from flask import Flask, jsonify, request
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def save_finances(data_for_save):
    if not os.path.exists('finances.json'):
        finance_file = open('finances.json', 'w')
        json.dump(data_for_save, finance_file, indent=6)
        finance_file.close()
    else:
        finance_file = open('finances.json', 'r')

        with open("finances.json", encoding='utf-8') as finance_json:
            data = json.load(finance_json)
            data_saved = []

            if type(data) == dict:
                data_saved.append(data)
            elif type(data) == list:
                data_saved = data

            if len(data_for_save) > 0:
                for dt in data_for_save:
                    data_saved.append(dt)

            if len(data_saved) > 0:
                finance_file = open('finances.json', 'w')
                json.dump(data_saved, finance_file, indent=6)
                finance_file.close()


def create_id():
    finance_file = open('finances.json', 'r')

    with open("finances.json", encoding='utf-8') as finance_json:
        data = json.load(finance_json)

        if len(data) > 0:
            last_id = data[-1]['id']
            new_id = last_id + 1

        return new_id


@app.route('/api/v1/finances/<int:start_year>/<int:start_month>/<int:end_year>/<int:end_month>', methods=['GET'])
def show_historic_per_month(start_year, start_month, end_year, end_month):
    try:
        finance_file = open('finances.json', 'r')
        with open("finances.json", encoding='utf-8') as finance_json:
            data = json.load(finance_json)

            filtered_historic = []

            for dt in data:
                if not dt['Ano'] < int(start_year) and not dt['Mes'] < start_month and not dt['Ano'] > int(end_year) and not dt['Mes'] > end_month:
                    filtered_historic.append(dt)

        return filtered_historic

    except:
        print('Ooops, nada encontrado!')


@app.route('/api/v1/finances/<int:id>/', methods=['GET'])
def show_historic_per_id(id):
    try:
        finance_file = open('finances.json', 'r')
        with open("finances.json", encoding='utf-8') as finance_json:
            data = json.load(finance_json)

            filtered_historic = []

            for dt in data:
                if dt['id'] == int(id):
                    filtered_historic.append(dt)

        return filtered_historic

    except:
        print('Ooops, nada encontrado!')


@app.route('/api/v1/finances', methods=['GET'])
def show_historic():
    finance_file = open('finances.json', 'r')
    with open("finances.json", encoding='utf-8') as finance_json:
        data = json.load(finance_json)

    return data


@app.route('/api/v1/finances/<int:finance_id>', methods=['PUT'])
def edit_finances(finance_id):
    finance_file = open('finances.json', 'r')
    alteration = request.get_json()

    with open("finances.json", encoding='utf-8') as finance_json:
        data = json.load(finance_json)
        data_saved = []

        if type(data) == dict:
            data_saved.append(data)
        elif type(data) == list:
            data_saved = data

            for dele in data_saved:
                if dele['id'] == finance_id:
                    dele.update(alteration)
                    break

        if len(data_saved) > 0:
            finance_file = open('finances.json', 'w')
            json.dump(data_saved, finance_file, indent=6)
            finance_file.close()

        return data


@app.route('/api/v1/finances', methods=['POST'])
def include_data():
    finance_file = open('finances.json', 'r')
    new_data = request.get_json()
    new_data.update({'id': create_id()})

    with open("finances.json", encoding='utf-8') as finance_json:
        data = json.load(finance_json)
        data_saved = []

        if type(data) == dict:
            data_saved.append(data)
        elif type(data) == list:
            data_saved = data

        data_saved.append(new_data)

        if len(data_saved) > 0:
            finance_file = open('finances.json', 'w')
            json.dump(data_saved, finance_file, indent=6)
            finance_file.close()

        return data


@app.route('/api/v1/finances/<int:finance_id>', methods=['DELETE'])
def delete_finances(finance_id):
    finance_file = open('finances.json', 'r')

    with open("finances.json", encoding='utf-8') as finance_json:
        data = json.load(finance_json)
        data_saved = []

        if type(data) == dict:
            data_saved.append(data)
        elif type(data) == list:
            data_saved = data

        if len(data_saved) > 0:
            for dele in data_saved:
                if dele['id'] == finance_id:
                    finance_index = data_saved.index(dele)
                    data_saved.pop(finance_index)
                    break

        if len(data_saved) > 0:
            finance_file = open('finances.json', 'w')
            json.dump(data_saved, finance_file, indent=6)
            finance_file.close()

        return data


app.run(port=8080, host='localhost', debug=True)
