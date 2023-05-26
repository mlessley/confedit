from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Set up CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the database connection
cnx = mysql.connector.connect(user="root", password="password", host="localhost", database="app")


# Define the threshold_config model
class ThresholdConfig(BaseModel):
    app: str
    env: str
    component: str
    sub_component: str
    threshold: int


# Define the endpoints for CRUD operations
@app.get("/config/{app}/{env}/{component}/{sub_component}")
async def get_config(app: str, env: str, component: str, sub_component: str):
    cursor = cnx.cursor()
    query = "SELECT threshold FROM threshold_config " "WHERE app = %s AND env = %s AND component = %s AND sub_component = %s"
    params = (app, env, component, sub_component)
    cursor.execute(query, params)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return {"app": app, "env": env, "component": component, "sub_component": sub_component, "threshold": row[0]}


@app.get("/config")
async def get_all_config():
    cursor = cnx.cursor()
    query = "SELECT app, env, component, sub_component, threshold FROM threshold_config"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    configs = []
    for row in rows:
        app, env, component, sub_component, threshold = row
        config = {"app": app, "env": env, "component": component, "sub_component": sub_component, "threshold": threshold}
        configs.append(config)
    return configs


@app.post("/config")
async def create_config(config: ThresholdConfig):
    cursor = cnx.cursor()
    query = "INSERT INTO threshold_config " "(app, env, component, sub_component, threshold) " "VALUES (%s, %s, %s, %s, %s)"
    params = (config.app, config.env, config.component, config.sub_component, config.threshold)
    cursor.execute(query, params)
    cnx.commit()
    cursor.close()
    return {"message": "Config created"}


@app.put("/config/{app}/{env}/{component}/{sub_component}")
async def update_config(app: str, env: str, component: str, sub_component: str, config: ThresholdConfig):
    cursor = cnx.cursor()
    query = "UPDATE threshold_config " "SET threshold = %s " "WHERE app = %s AND env = %s AND component = %s AND sub_component = %s"
    params = (config.threshold, app, env, component, sub_component)
    cursor.execute(query, params)
    cnx.commit()
    cursor.close()
    return {"message": "Config updated"}


@app.delete("/config/{app}/{env}/{component}/{sub_component}")
async def delete_config(app: str, env: str, component: str, sub_component: str):
    cursor = cnx.cursor()
    query = "DELETE FROM threshold_config " "WHERE app = %s AND env = %s AND component = %s AND sub_component = %s"
    params = (app, env, component, sub_component)
    cursor.execute(query, params)
    cnx.commit()
    cursor.close()
    return {"message": "Config deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)




