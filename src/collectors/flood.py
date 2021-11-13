from os import environ
import requests
import json
from re import sub
import unicodedata

base_url = environ.get("FLOOD_API_URL")


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def connect():
    username = environ.get("FLOOD_USERNAME")
    password = environ.get("FLOOD_PASSWORD")

    response = requests.post(
        f"{base_url}/auth/authenticate",
        data={"username": username, "password": password},
    )
    response.raise_for_status()

    return response.cookies["jwt"]


def retreive_data(token):
    jar = requests.cookies.RequestsCookieJar()
    jar.set("jwt", token)

    # Retreive response as a Server Event
    response = requests.get(f"{base_url}/activity-stream", cookies=jar, stream=True)
    generator = response.iter_lines()

    while True:
        line = next(generator).decode("utf-8")

        # Wait to get the event TORRENT_LIST_FULL_UPDATE
        if line == "event:TORRENT_LIST_FULL_UPDATE":
            # Retreive the data
            data = next(generator).decode("utf-8")
            # Remove the data: header
            data = data[5:]

            # Close the response as we don't need it
            response.close()

            return json.loads(data)


def collect():
    token = connect()
    json_data = retreive_data(token)

    for torrent in json_data.values():
        tags_list = torrent["tags"]

        # Set the tag to untagged as default
        tag = "untagged"
        # If a tag exists, use first
        if len(tags_list) > 0:
            tag = tags_list[0]

        name = torrent["name"].lower()  # To lowercase
        name = sub("\([^\)]*\)", "", name)  # Remove the ()
        name = sub("\[[^\]]*\]", "", name)  # Remove the []
        name = sub("\..{,3}$", "", name)  # Remove the extension
        name = sub(
            "(.26[4-5]|\d{3,4}p|webr?i?p?|multi|vostf?r?|\d+bits?|-[^ ]+$)|s?u?b?french|blueray|-[^-]+$|",
            "",
            name,
        )  # Remove common words
        name = sub("[\.\+_]", " ", name)  # Replace the . or + by a dash
        name = sub(" +", " ", name)  # Replace multiple spaces to one
        name = strip_accents(name)
        name = name.strip()
        name = name.replace(" ", "-")
        name = sub("-+", "-", name)
        name = json.dumps(name)
        upload = torrent["upTotal"]
        download = torrent["bytesDone"]
        added = torrent["dateAdded"]

        yield f"flood,tag={tag},name={name} upload={upload}u,download={download}u,added={added}u"


if __name__ == "__main__":
    for i in collect():
        print(i)
