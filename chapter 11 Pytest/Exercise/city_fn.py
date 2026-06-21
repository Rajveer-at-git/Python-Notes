def get_formatted_city_country(city, country, population = ""):
    if population:
        formatted_city_country = f"{city}, {country} - Population {population}"
        return formatted_city_country.title()
    else:
        formatted_city_country = f"{city}, {country}"
        return formatted_city_country.title()