import numpy as np


def to_celcius(temp):
    kelvin_temp = temp
    celcius_temp = kelvin_temp - 273.15
    return celcius_temp


def to_farenheit(temp):
    kelvin_temp = temp
    celcius_temp = to_celcius(kelvin_temp)
    farenheit_temp = celcius_temp * 9/5 + 32
    return farenheit_temp


def convert_to_unit(temp, unit):
    t = int(temp)
    if (not unit):
        return t
    if (unit.lower() == "farenheit" or
            unit.lower() == "f"):
        t = to_farenheit(t)
    if (unit.lower() == "celcius" or
            unit.lower() == "c"):
        t = to_celcius(t)
    return t


def calculate_temp_fluctuation(weather):
    t_max = weather["main"]["temp_max"]
    t_min = weather["main"]["temp_min"]
    fluct = t_max - t_min
    return fluct


def get_combo(heuristics):
    # Define the actions for each range
    actions = {
        "heat_ranges": {
            "vCold": "Carry a jacket",
            "cold": "Wear a sweater",
            "comfortable": "Wear comfortable clothing",
            "hot": "Wear light clothing",
            "vHot": "Stay indoors or in shade"
        },
        "wetness_ranges": {
            "heavy": "Carry an umbrella",
            "wet": "Wear waterproof shoes",
            "light": "Carry a light raincoat",
            "dry": None
        },
        "snow_ranges": {
            "heavy": "Avoid driving, use snow chains if necessary",
            "moderate": "Be cautious while driving, carry snow chains",
            "light": "Carry a snow shovel in your car",
            "none": None
        },
        "wind_ranges": {
            "vWindy": "Wear windproof clothing",
            "windy": "Enjoy the breeze",
            "calm": None,
        },
        "temp_fluctuation_ranges": {
            "extreme": "Be prepared for sudden temperature changes",
            "mild": "Carry layers of clothing",
            "negligible": None
        }
    }

    # Define the ranges
    heat_ranges = ["vCold", "cold", "comfortable", "hot", "vHot"]
    wetness_ranges = ["heavy", "wet", "light", "dry"]
    snow_ranges = ["heavy", "moderate", "light", "none"]
    wind_ranges = ["vWindy", "windy", "calm"]
    temp_fluctuation_ranges = ["extreme", "mild", "negligible"]

    # Generate the combinations and assign actions
    combinations_actions = [(heat, wetness, snow, wind, temp_fluctuation,
                            actions["heat_ranges"][heat],
                            actions["wetness_ranges"][wetness],
                            actions["snow_ranges"][snow],
                            actions["wind_ranges"][wind],
                            actions["temp_fluctuation_ranges"][temp_fluctuation])
                            for heat in heat_ranges
                            for wetness in wetness_ranges
                            for snow in snow_ranges
                            for wind in wind_ranges
                            for temp_fluctuation in temp_fluctuation_ranges]

    c = []
    for key in heuristics:
        c.append(heuristics[key])
    for combination in combinations_actions:
        if ((np.array(combination[0:5]) == c).all()):
            return np.array(combination)


def calculate_heuristics(weather):
    t = convert_to_unit(weather["main"]["feels_like"], "c")
    tf = calculate_temp_fluctuation(weather)
    r = 0 if "rain" not in weather else weather["rain"]["1h"] if "3h" not in weather["rain"] else weather["rain"]["3h"]
    s = 0 if "snow" not in weather else weather["snow"]["1h"] if "3h" not in weather["snow"] else weather["snow"]["3h"]
    w = weather["wind"]["speed"]
    heat_ranges = {
        "vCold": "t < 10",
        "cold": "10 < t < 16",
        "comfortable": "16 < t < 26",
        "hot": "26 < t < 32",
        "vHot": "t > 32"
    }
    wetness_ranges = {
        "heavy": "r > 5",
        "wet": "3 < r < 5",
        "light": "1 < r < 3",
        "dry": "r < 1"
    }
    snow_ranges = {
        "heavy": "s > 5",
        "moderate": "3 < s < 5",
        "light": "1 < s < 3",
        "none": "s < 1"
    }
    wind_ranges = {
        "vWindy": "w > 10",
        "windy": "5 < w < 10",
        "calm": "w < 5",
    }
    temp_fluctuation_ranges = {
        "extreme": "tf > 15",
        "mild": "5 < tf < 15",
        "negligible": "tf < 5"
    }
    heuristics = {"heat": "", "wetness": "",
                  "snow": "", "wind": "", "temp_fluctuation": ""}
    for key in heuristics:
        for x, y in eval(key + "_ranges.items()"):
            if (eval(y)):
                heuristics[key] = x
                break
    return heuristics
