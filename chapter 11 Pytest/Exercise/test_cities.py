from city_fn import get_formatted_city_country
def test_city_country():
    formatted_cities = get_formatted_city_country("mumbai","india","1670000000")
    assert formatted_cities == "Mumbai, India - Population 1670000000"
