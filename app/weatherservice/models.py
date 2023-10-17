from redis_om import (EmbeddedJsonModel, Field, JsonModel)
from pydantic import PositiveInt
from typing import List

class Person(JsonModel):
    # Indexed for exact text matching
    location: str = Field(index=True)
