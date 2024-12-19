from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.orm import SyncORM, AsyncORM



app = Flask(__name__)
CORS(app)

@app.route('/get_cards', methods=['GET'])
def home():
    data = request.args.get('key').split(';')
    print(f"Received data: {data}")
    filter_cake = [int(data[0]), dict(map(lambda x: (x.split(':')[0], x.split(':')[1].split(',')), data[1:]))]
    print(filter_cake)
    
    SyncORM.create_table()
    SyncORM.insert_data()


    res = SyncORM.get_result(filter_cake)
    print(res)

    return jsonify(res)


@app.route('/get_conditer_info')
def cond_info():
    conditer_id = request.args.get('id')
    return jsonify(SyncORM.get_conditer_info(conditer_id))


if __name__ == '__main__':
    app.run(port=5001)