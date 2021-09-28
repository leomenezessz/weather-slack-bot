import uvicorn
from fastapi import FastAPI, Form

import weather
from cities import get_city_id_by_name
from slackclient import make_forecast_slack_message
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/icons", StaticFiles(directory="icons"), name="icons")


@app.post("/weather/forecast")
async def weather_by_city(city: str = Form(default="Santos", alias="text")):
    city_id = get_city_id_by_name(city)
    forecast_weather = await weather.forecast_by_city_id(city_id)
    return make_forecast_slack_message(forecast_weather)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8085)
