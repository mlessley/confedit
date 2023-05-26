from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from pydantic import BaseModel

app = Flask(__name__)
cnx = mysql.connector.connect(user="root", password="password", host="127.0.0.1", database="app")


class ThresholdConfig(BaseModel):
    app: str
    env: str
    component: str
    sub_component: str
    threshold: int


@app.route("/")
def index():
    edited_id = request.args.get("edited_id", 0)  # Get edited_id parameter
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM threshold_config")
    configs = cursor.fetchall()
    cursor.close()
    return render_template("index.html", configs=configs, edited_id=int(edited_id))  # Pass edited_id parameter


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        app = request.form["app"]
        env = request.form["env"]
        component = request.form["component"]
        sub_component = request.form["sub_component"]
        threshold = request.form["threshold"]
        cursor = cnx.cursor()
        query = "INSERT INTO threshold_config (app, env, component, sub_component, threshold) VALUES (%s, %s, %s, %s, %s)"
        params = (app, env, component, sub_component, threshold)
        cursor.execute(query, params)
        cnx.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return redirect(url_for("index", edited_id=new_id))
    else:
        return render_template("create.html")


@app.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        app = request.form["app"]
        env = request.form["env"]
        component = request.form["component"]
        sub_component = request.form["sub_component"]
        threshold = request.form["threshold"]
        active = request.form.get("active", False) == "on"

        cursor = cnx.cursor()
        # query = "UPDATE threshold_config SET app = %s, env = %s, component = %s, sub_component = %s, threshold = %s WHERE id = %s"
        query = (
            "UPDATE threshold_config SET app = %s, env = %s, component = %s, sub_component = %s, threshold = %s, active = %s WHERE id = %s"
        )
        # params = (app, env, component, sub_component, threshold, id)
        params = (app, env, component, sub_component, threshold, active, id)
        try:
            cursor.execute(query, params)
        except Exception as e:
            print(e)
        cnx.commit()
        cursor.close()
        return redirect(url_for("index", edited_id=id))  # Add edited_id parameter

    else:
        cursor = cnx.cursor()
        query = "SELECT * FROM threshold_config WHERE id = %s"
        params = (id,)
        cursor.execute(query, params)
        config = cursor.fetchone()
        cursor.close()
        return render_template("update.html", config=config)


@app.route("/delete/<string:id>", methods=["POST"])
def delete(id):
    cursor = cnx.cursor()
    query = "DELETE FROM threshold_config WHERE id = %s"
    params = (id,)
    cursor.execute(query, params)
    cnx.commit()
    cursor.close()
    return redirect(url_for("index"))


@app.route("/create_config", methods=["GET"])
def create_config():
    cursor = cnx.cursor()

    # Insert 5 sample rows into the configs table
    for i in range(5):
        app = f"App-{i+1}"
        env = f"Env-{i+1}"
        comp = f"Comp-{i+1}"
        subcomp = f"Sub-Comp-{i+1}"
        threshold = i + 1
        try:
            cursor.execute(
                "INSERT INTO threshold_config (app, env, component, sub_component, threshold) VALUES (%s, %s, %s, %s, %s)",
                (app, env, comp, subcomp, threshold),
            )
        except Exception as e:
            print(e)

    cnx.commit()
    cnx.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
