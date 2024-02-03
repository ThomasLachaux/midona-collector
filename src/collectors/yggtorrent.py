import requests
from os import environ
from bs4 import BeautifulSoup

base_url = environ.get("YGG_BASE_URL")


def collect():
    session = requests.session()

    login = environ.get("YGG_USERNAME")
    password = environ.get("YGG_PASSWORD")

    loginResponse = session.post(
        f"{base_url}/user/login", data={"id": login, "pass": password}
    )
    loginResponse.raise_for_status()

    userRequest = session.get(f"{base_url}/user/ajax_usermenu")
    userRequest.raise_for_status()


    html = userRequest.json()["html"]

    soup = BeautifulSoup(html, "html.parser")

    # Prepare the measure
    metric = "yggtorrent "

    for type in ("upload", "download"):
        # expects to have 1.00Go
        measure = soup.select_one(f"span.ico_{type}").parent.text.strip()

        # Get the unit (either Go or To)
        unit = measure[-2:]
        power = 9

        # If To, change the power to 12
        if unit == "To":
            power = 12

        # Get the value and converts it to bytes
        value = int(float(measure[:-2]) * 10 ** power)

        # Add the measure
        metric += f"{type}={value}u,"

    ratio = soup.select_one('div.ct ul li:nth-child(2)').text.split(' ')[-1]
    metric += f"ratio={ratio}"

    yield metric


if __name__ == "__main__":
    for i in collect():
        print(i)
