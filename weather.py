import os
from typing import List

import httpx
from pydantic import BaseModel

WEATHER_API_URL = os.environ["WEATHER_API_URL"]
WEATHER_API_CLIENT_TOKEN = os.environ["WEATHER_API_CLIENT_TOKEN"]


class PhraseModel(BaseModel):
    reduced: str
    morning: str
    afternoon: str
    night: str
    dawn: str


class PeriodModel(BaseModel):
    min: int
    max: int


class DawnModel(PeriodModel):
    pass


class MorningModel(PeriodModel):
    pass


class AfternoonModel(PeriodModel):
    pass


class NightModel(PeriodModel):
    pass


class TemperatureModel(PeriodModel):
    min: int
    max: int
    dawn: DawnModel
    morning: MorningModel
    afternoon: AfternoonModel
    night: NightModel


class TextModel(BaseModel):
    pt: str
    en: str
    es: str
    phrase: PhraseModel


class IconModel(BaseModel):
    dawn: str
    morning: str
    afternoon: str
    night: str
    day: str


class WeatherTextIconModel(BaseModel):
    icon: IconModel
    text: TextModel


class RainModel(BaseModel):
    probability: int
    precipitation: int


class WeatherData(BaseModel):
    date_br: str
    rain: RainModel
    text_icon: WeatherTextIconModel
    temperature: TemperatureModel


class ForecastWeather(BaseModel):
    name: str
    state: str
    country: str
    data: List[WeatherData]


async def forecast_by_city_id(city_id: str) -> ForecastWeather:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{WEATHER_API_URL}/api/v1/forecast/locale/{city_id}/days/15?token={WEATHER_API_CLIENT_TOKEN}")

        if response.status_code == httpx.codes.OK:
            return ForecastWeather.parse_obj(response.json())
