import mysql.connector
import json

# Connect to the MySQL database
cnx = mysql.connector.connect(user="root", password="password", host="localhost", database="app")

# Query the threshold_config table and fetch the results
cursor = cnx.cursor()
query = "SELECT app, env, component, sub_component, threshold " "FROM threshold_config"
cursor.execute(query)
rows = cursor.fetchall()

# Convert the results to a dictionary
threshold_config = {}
for row in rows:
    app, env, comp, sub_comp, value = row
    if app not in threshold_config:
        threshold_config[app] = {}
    if env not in threshold_config[app]:
        threshold_config[app][env] = {}
    if comp not in threshold_config[app][env]:
        threshold_config[app][env][comp] = {}
    threshold_config[app][env][comp][sub_comp] = value

# Close the database connection
cursor.close()
cnx.close()

# Print the resulting dictionary
print(json.dumps(threshold_config, indent=4))


def get_severity(threshold_config, keys, severity_level, threshold):
    value = threshold_config
    for key in keys:
        if key in value:
            value = value[key]
        else:
            return None
    if value >= threshold:
        return severity_level
    else:
        return "CLEAR"


default_severity = "Critical"
value = 90
result = get_severity(threshold_config, ("app1", "env1", "comp1", "sub_comp1"), default_severity, value)
print(result)
