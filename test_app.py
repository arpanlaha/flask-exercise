
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"

    res = client.get("/users?team=fake")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 0


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19

    res = client.get("/users/5")
    assert res.status_code == 404


def test_post_users(client):
    # try a valid POST request
    res = client.post("/users", json=dict(name="Arpan", age=19, team="LWB"))
    assert res.status_code == 201

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Arpan"
    assert res_user["age"] == 19
    assert res_user["team"] == "LWB"
    res = client.get("/users")
    res_users = res.json["result"]["users"]
    assert len(res_users) == 5  # we should have added one user

    # now an invalid POST request
    res = client.post("/users", json=dict(name="Arpan", age=19))
    assert res.status_code == 422
    res = client.get("/users")
    res_users = res.json["result"]["users"]
    assert len(res_users) == 5  # number of users should not have changed


def test_put_user_id(client):
    # try a valid PUT request
    res = client.put("/users/3", json=dict(age=24, team="LWB"))
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Varun"
    assert res_user["age"] == 24
    assert res_user["team"] == "LWB"
    res = client.get("/users")
    res_users = res.json["result"]["users"]
    assert len(res_users) == 5  # number of users should not have changed

    # now an invalid PUT request
    res = client.put("/users/6", json=dict(age=24, team="LWB"))
    assert res.status_code == 404


def test_delete_user_id(client):
    # try a valid DELETE request
    res = client.delete("users/1")
    assert res.status_code == 200
    res = client.get("/users")
    res_users = res.json["result"]["users"]
    assert len(res_users) == 4  # number of users should hhve decreased by one

    # now an invalid DELETE request
    res = client.delete("users/6")
    assert res.status_code == 404
