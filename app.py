from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


# TODO: Implement the rest of the API here!
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        team = request.args.get("team")
        if isinstance(team, str):
            userList = []
            for user in db.get("users"):
                if user["team"] == team:
                    userList.append(user)
            data = {"users": userList}
        else:
            data = {"users": db.get("users")}
        return create_response(data)
    elif request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        age = data.get("age")
        team = data.get("team")
        if not (
            isinstance(name, str) and isinstance(age, int) and isinstance(team, str)
        ):
            return create_response(status=422, message="Not all fields provided!")
        info = {"id": -1, "name": name, "age": age, "team:": team}
        return create_response(status=201, data=db.create("users", info))


@app.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
def userid(id):
    found = False
    for user in db.get("users"):
        if user["id"] == int(id):
            found = True
            if request.method == "GET":
                return create_response({"user": db.getById("users", int(id))})
            elif request.method == "PUT":
                info = request.get_json()
                return create_response(data=db.updateById("users", int(id), info))
            elif request.method == "DELETE":
                return create_response(data=db.deleteById("users", int(id)))
    if not found:
        return create_response(status=404, message="User not found!")


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
