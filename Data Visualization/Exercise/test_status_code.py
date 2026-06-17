def test_status_code_is_200():
    from operator import itemgetter
    import plotly.express as px
    import requests

    # Make an API call and check the response.
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url)
    assert r.status_code == 200