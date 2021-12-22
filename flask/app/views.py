import json
from pprint import pprint

import pymysql

from app import app

with open("config.json") as f:
    config = json.load(f)
    host = config["host"]
    user = config["user"]
    password = config["password"]
    database = config["database"]
    print("*"*50)
    print("config", config)
    print("host", host)
    print("user", user)
    print("password", password)
    print("database", database)
    print("*"*50)

@app.route("/")
def index():
    return "Hello, World! from the nginx-docker-flask-app created"

@app.route("/recipes")
def get_recipes():
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        # port=3307
    )

    with connection:
        cur = connection.cursor()
        cur.execute(
            "SELECT id,title, making_time, serves, ingredients, cost FROM recipes"
        )
        print(cur)
        data = cur.fetchall()
        print(data)

    recipes = {"recipes": data}
    pprint(recipes)
    return {"statusCode": 200, "body": json.dumps(recipes)}