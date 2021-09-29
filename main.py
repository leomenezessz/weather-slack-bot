import uvicorn
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles

import weather
from cities import get_city_id_by_name
from slackclient import mount_forecast_slack_message, SlackApi, searching_forecast_message_template
from worker import do_in_background

app = FastAPI()

app.mount("/icons", StaticFiles(directory="icons"), name="icons")


@app.post("/weather/forecast")
async def weather_by_city(city: str = Form(default="Santos", alias="text")):
    city_id = get_city_id_by_name(city)
    forecast_weather = await weather.forecast_by_city_id(city_id)
    do_in_background(SlackApi().send_message, [mount_forecast_slack_message(forecast_weather),
                                               f"Segue sua previsão de 15 dias para cidade de {forecast_weather.name}."])
    return searching_forecast_message_template(forecast_weather.name)


if __name__ == '__main__':
    uvicorn.run(app, debug=True, host="0.0.0.0", port=8085)
