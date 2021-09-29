import os

from slack import WebClient

from weather import ForecastWeather, WeatherData

_TEMPLATE_DIVIDER = {
    "type": "divider"
}


def _translate_period(period):
    return {
        "morning": "Manhã",
        "afternoon": "Tarde",
        "night": "Noite",
        "dawn": "Madrugada"
    }.get(period)


def _forecast_period_section_template(weather_data: WeatherData, period: str):
    temperature = getattr(weather_data.temperature, period)
    phrase = getattr(weather_data.text_icon.text.phrase, period)
    icon = getattr(weather_data.text_icon.icon, period)

    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{_translate_period(period)}*\n\n"
                    f" *Min*: {temperature.min}\n"
                    f" *Max*: {temperature.max}\n\n"
                    f" {phrase}."
        },
        "accessory": {
            "type": "image",
            "image_url": f"https://calm-puma-6.loca.lt/icons/128px/{icon}.png",
            "alt_text": f"forecast {period} icon"
        }
    }


def _forecast_date_template(date: str):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"`{date}`"
        }
    }


def _forecast_header_template(days: str = "15"):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Previsão do tempo no periodo de *{days}* dias para cidade de `Santos/SP`."
        }
    }


def searching_forecast_message_template(city : str):
    return {"blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Buscando a previsão do tempo para sua cidade *{city}*."
            }
        }
    ]
    }


def mount_forecast_slack_message(forecasts: ForecastWeather):
    message_blocks = []
    forecasts_header_template = _forecast_header_template()
    message_blocks.append(forecasts_header_template)

    for forecast in forecasts.data:
        forecast_date_section = _forecast_date_template(forecast.date_br)
        forecast_dawn_section = _forecast_period_section_template(forecast, "dawn")
        forecast_morning_section = _forecast_period_section_template(forecast, "morning")
        forecast_afternoon_section = _forecast_period_section_template(forecast, "afternoon")
        forecast_night_section = _forecast_period_section_template(forecast, "night")

        message_blocks.append(forecast_date_section)
        message_blocks.append(forecast_dawn_section)
        message_blocks.append(forecast_morning_section)
        message_blocks.append(forecast_afternoon_section)
        message_blocks.append(forecast_night_section)

        message_blocks.append(_TEMPLATE_DIVIDER)

    return message_blocks


class SlackApi:

    def __init__(self, channel_id=None, client_token=None):
        self._channel_id = channel_id if channel_id else os.environ["CHANNEL_ID"]
        self._client = WebClient(token=client_token) if client_token else WebClient(
            token=os.environ["SLACK_CLIENT_TOKEN"])

    def send_message(self, blocks=None, text=None):
        return self._client.chat_postMessage(
            channel=self._channel_id,
            text=text,
            blocks=blocks,
        )
