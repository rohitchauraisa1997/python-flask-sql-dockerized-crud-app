import json
from datetime import datetime as dt
from pprint import pprint

import pymysql
from flask import Flask, request

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

@app.route("/recipes", methods=["POST"])
def add_recipe():
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    # print(request.json)
    inputs = request.json
    title = inputs.get("title")
    serves = inputs.get("serves")
    making_time = inputs.get("making_time")
    ingredients = inputs.get("ingredients")
    cost = inputs.get("cost")

    with connection:
        cur = connection.cursor()
        # cur.execute("INSERT INTO recipes (title, making_time, serves, ingredients, cost) VALUES ({},{},{},{})".format(title, making_time, serves, ingredients, cost))
        execute_command = "INSERT INTO recipes (title, making_time, serves, ingredients, cost) VALUES ('{}', '{}', '{}', '{}', '{}') ".format(
            title, making_time, serves, ingredients, cost
        )
        print("&" * 30)
        print(execute_command)
        print("&" * 30)
        cur.execute(execute_command)
        last_id = cur.lastrowid
        print("lastrowid", last_id)
        connection.commit()
        cur.execute(
            "SELECT id,title, making_time, serves, ingredients, cost, created_at, updated_at FROM recipes"
        )
        added_recipe = cur.fetchall()[-1]
        print(added_recipe)
        print(type(added_recipe))
        current_date = added_recipe.get("created_at")
        current_date = dt.strftime(current_date, "%Y-%m-%d %H:%M:%S")
        print("current_date", current_date)
        update_date = added_recipe.get("updated_at")
        update_date = dt.strftime(update_date, "%Y-%m-%d %H:%M:%S")
        print("update_date", update_date)

        added_recipe["created_at"] = current_date
        added_recipe["updated_at"] = update_date
        # del added_recipe["updated_at"]
    return_dict = dict()

    return_dict["message"] = "Recipe successfully created!"
    return_dict["recipe"] = added_recipe

    pprint(return_dict)
    return {"statusCode": 200, "body": json.dumps(return_dict)}


@app.route("/recipe/<string:id>")
def get_recipe_by_id(id):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    print("id to get", id)
    id_to_fetch = id
    with connection:
        cur = connection.cursor()
        cur.execute(
            "SELECT id,title, making_time, serves, ingredients, cost FROM recipes WHERE id = {}".format(
                id_to_fetch
            )
        )
        data = cur.fetchone()
        print(data)
        print(type(data))

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Recipe Details by id", "recipe": data}),
    }


@app.route("/recipes/<string:id>", methods=["DELETE"])
def delete_recipe_by_id(id):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    print("id_to_delete", id)
    id_to_delete = id
    with connection:
        cur = connection.cursor()
        cur.execute(
            "SELECT id,title, making_time, serves, ingredients, cost FROM recipes WHERE id = {}".format(
                id_to_delete
            )
        )
        print(cur)
        data = cur.fetchone()
        print(data)
        print(type(data))

        if data:
            cur = connection.cursor()
            cur.execute("DELETE FROM recipes WHERE id = {}".format(id_to_delete))
            print(cur)
            connection.commit()

            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Recipe successfully removed!"}),
            }

        else:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No Recipe found"}),
            }


@app.route("/recipes/<string:id>", methods=["PATCH"])
def update_recipe_by_id(id):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    inputs = request.json
    title = inputs.get("title")
    serves = inputs.get("serves")
    making_time = inputs.get("making_time")
    ingredients = inputs.get("ingredients")
    cost = inputs.get("cost")

    with connection:
        cur = connection.cursor()
        execute_command = "UPDATE recipes set title = '{}', making_time = '{}', serves = '{}', ingredients = '{}', cost = '{}' WHERE id = '{}'".format(
            title, making_time, serves, ingredients, cost, id
        )
        print("+" * 30)
        print(execute_command)
        print("+" * 30)
        cur.execute(execute_command)
        print(cur)
        connection.commit()
        last_id = cur.lastrowid
        print("lastrowid", last_id)
        connection.commit()
        cur.execute(
            "SELECT id,title, making_time, serves, ingredients, cost, created_at, updated_at FROM recipes WHERE id = '{}'".format(
                id
            ) 
        )
        added_recipe = cur.fetchall()[-1]
        print(added_recipe)
        print(type(added_recipe))
        current_date = added_recipe.get("created_at")
        current_date = dt.strftime(current_date, "%Y-%m-%d %H:%M:%S")
        print("current_date", current_date)
        update_date = added_recipe.get("updated_at")
        update_date = dt.strftime(update_date, "%Y-%m-%d %H:%M:%S")
        print("update_date", update_date)

        added_recipe["created_at"] = current_date
        added_recipe["updated_at"] = update_date
        # del added_recipe["updated_at"]
    return_dict = dict()

    return_dict["message"] = "Recipe successfully updated!"
    return_dict["recipe"] = added_recipe

    pprint(return_dict)
    return {"statusCode": 200, "body": json.dumps(return_dict)}
