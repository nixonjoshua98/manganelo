import requests
from manganelo.common.constants import HOME_TOOLTIPS_URL

from manganelo.models import HomeStoryTooltip
from manganelo.errors import ManganeloRequestError


def get_home_page() -> list[HomeStoryTooltip]:
    r = requests.get(HOME_TOOLTIPS_URL)

    if r.status_code != 200:
        raise ManganeloRequestError(f"Home page request failed with status code {r.status_code}")

    try:
        return [HomeStoryTooltip(ele) for ele in r.json()]
    except KeyError as e:
        raise ManganeloRequestError(f"Home page response differs from expected response") from e
    except Exception as e:
        raise ManganeloRequestError(f"An unexpected error occurred") from e
