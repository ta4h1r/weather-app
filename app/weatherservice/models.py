from redis_om import (EmbeddedJsonModel, Field, JsonModel)
from pydantic import PositiveInt
from typing import Optional

class Temperature(EmbeddedJsonModel):
    value: int = Field(index=False)
    unit: str = Field(index=False)

class Wind(EmbeddedJsonModel):
    speed: int = Field(index=False)
    direction: str = Field(index=False)

class Precipitation(EmbeddedJsonModel):
    rain: int = Field(index=False)
    snow: str = Field(index=False)
    snow: str = Field(index=False)

# class WeatherDescription(EmbeddedJsonModel):
#     rain: int = Field(index=False)

class WeatherItem(EmbeddedJsonModel):
    temperature: Optional[Temperature]
    wind: Optional[Wind]
    precipitation: Optional[Precipitation]
    description: Optional[str] = Field(index=False)


class Weather(JsonModel):
    city: str = Field(index=True)
    weather: WeatherItem


