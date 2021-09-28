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
            "image_url": f"https://sharp-mayfly-42.loca.lt/icons/128px/{icon}.png",
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


def make_forecast_slack_message(forecasts: ForecastWeather):
    message_blocks = {"blocks": []}
    forecasts_header_template = _forecast_header_template()
    message_blocks["blocks"].append(forecasts_header_template)

    for forecast in forecasts.data:
        forecast_date_section = _forecast_date_template(forecast.date_br)
        forecast_dawn_section = _forecast_period_section_template(forecast, "dawn")
        forecast_morning_section = _forecast_period_section_template(forecast, "morning")
        forecast_afternoon_section = _forecast_period_section_template(forecast, "afternoon")
        forecast_night_section = _forecast_period_section_template(forecast, "night")

        message_blocks["blocks"].append(forecast_date_section)
        message_blocks["blocks"].append(forecast_dawn_section)
        message_blocks["blocks"].append(forecast_morning_section)
        message_blocks["blocks"].append(forecast_afternoon_section)
        message_blocks["blocks"].append(forecast_night_section)

        message_blocks["blocks"].append(_TEMPLATE_DIVIDER)

    return message_blocks
