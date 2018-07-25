import requests
from memoize import memoize


@memoize(timeout=120)
def get_currency_rate(org_currency, final_currency):
    url = "https://free.currencyconverterapi.com/api/v6/convert?q=" + org_currency + "_" + final_currency + "&compact=ultra"

    r = requests.get(url)
    result = r.json()
    return result
