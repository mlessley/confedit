from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from pydantic import BaseModel
import yaml
import os

# get cwd
cwd = os.getcwd()
# make full path to env.yaml
env_path = os.path.join(cwd, 'env.yaml')

with open(env_path) as f:
    config = yaml.safe_load(f)
    
app = Flask(__name__)
cnx = mysql.connector.connect(
    user=os.environ.get('MYSQL_USER', config['MYSQL_USER']),
    password=os.environ.get('MYSQL_PASSWORD', config['MYSQL_PASSWORD']),
    host=os.environ.get('MYSQL_HOST', config['MYSQL_HOST']),
    database=os.environ.get('MYSQL_DATABASE', config['MYSQL_DATABASE'])
)


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


# create a config file with regexes and coresponding integer value. each regex should also have a name field
# create code to load that file
# create code to load an optional file in same format, that will override entries in the default file or add new entries
# automatically load the config file and then the optional file if it exists
import os
import re
import yaml

def load_regex():
    regex = {}
    for filename in ['config.yaml', 'config_override.yaml']:
        if os.path.exists(filename):
            with open(filename) as f:
                config = yaml.safe_load(f)
            for entry in config:
                regex[entry['pattern']] = {'name': entry['name'], 'value': entry['value']}
    return regex

def match_token(token):
    regex = load_regex()
    for pattern, data in regex.items():
        if re.match(pattern, token):
            return data['value']
    return None

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
