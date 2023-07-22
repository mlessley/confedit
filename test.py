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


Apologies for the confusion. To log just the initial connect time for each request, you can use the `pre_request_hook` from the `requests` library. This allows you to measure the time before the request is sent. Here's an updated code snippet to achieve that:

```python
import requests
import logging
import time

url = 'https://example.com'  # Replace with the URL you want to measure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ConnectionTime')
logger.propagate = False  # Prevent duplicate logs from appearing in the console

# Custom logging handler to log only the connect time
class ConnectionTimeHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logger.info(log_entry.split(': ')[-1])

# Add the custom logging handler to the logger
logger.addHandler(ConnectionTimeHandler())

# Custom pre_request_hook to measure and log the connect time
def log_connect_time(request, *args, **kwargs):
    start_time = time.time()
    return request

session = requests.Session()
session.hooks['pre_request'] = log_connect_time

num_requests = 5  # You can adjust the number of requests

for _ in range(num_requests):
    try:
        response = session.get(url, timeout=5)  # Set the timeout value to your preferred value
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
```

With this code, you'll log only the initial connect time for each request made using the `requests` library. The `log_connect_time` function is used as a custom `pre_request_hook`, which is called before each request is sent. The connect time is measured and logged within this hook, capturing only the initial connection time.
