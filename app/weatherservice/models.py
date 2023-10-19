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

class Weather(EmbeddedJsonModel):
    temperature: Optional[Temperature]
    wind: Optional[Wind]
    precipitation: Optional[Precipitation]
    summary: Optional[str] = Field(index=False)
    description: Optional[str] = Field(index=False)

class WeatherItem(JsonModel):
    timestamp: int = Field(index=False)
    city: str = Field(index=True)
    recommendation: str = Field(index=False)
    weather: Weather

