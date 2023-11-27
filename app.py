from flask import Flask, jsonify, abort, make_response, request
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "qwerty"


@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(todos.all())

@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'expense' in request.json:
        abort(400)
    todo = {
        'id': todos.all()[-1]['id'] + 1,
        'expense': request.json['expense'],
        'cost': request.json.get('cost', ""),
        'paid': request.json.get('paid', False)
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'expense' in data and not isinstance(data.get('expense'), str),
        'cost' in data and not isinstance(data.get('cost'), (int, float)),
        'paid' in data and not isinstance(data.get('paid'), bool)
    ]):
        abort(400)
    todo = {
        'id': todo_id,
        'expense': data.get('expense', todo['expense']),
        'cost': data.get('cost', todo['cost']),
        'paid': data.get('paid', todo['paid'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})

if __name__ == "__main__":
    app.run(debug=True)
