from manganelo.common.constants import HOME_TOOLTIPS_URL
from manganelo.models import HomeStoryTooltip
from manganelo.errors import RequestError
from manganelo.httpclient import _default_http_client


def get_home_page() -> list[HomeStoryTooltip]:
    r = _default_http_client.request("GET", HOME_TOOLTIPS_URL)

    if r.status_code != 200:
        raise RequestError(f"Home page request failed with status code {r.status_code}")

    try:
        return [HomeStoryTooltip(ele) for ele in r.json()]
    except KeyError as e:
        raise RequestError("Home page response differs from expected response") from e
    except Exception as e:
        raise RequestError("An unexpected error occurred") from e
