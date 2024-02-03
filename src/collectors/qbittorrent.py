from os import environ
import qbittorrentapi
from re import sub
import unicodedata
import json

qbt_login = environ.get('QBITTORRENT_LOGIN');
qbt_password = environ.get('QBITTORRENT_PASSWORD');
qbt_host = environ.get('QBITTORRENT_HOST');

qbt_client = qbittorrentapi.Client(host=qbt_host, username=qbt_login, password=qbt_password)

def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )

def collect():
    qbt_client.auth_log_in()
    for torrent in qbt_client.torrents_info():
        name = torrent["name"].lower()  # To lowercase
        name = sub("\([^\)]*\)", "", name)  # Remove the ()
        name = sub("\[[^\]]*\]", "", name)  # Remove the []
        name = sub("\..{,3}$", "", name)  # Remove the extension
        # name = sub(
        #     "(.26[4-5]|\d{3,4}p|webr?i?p?|multi|vostf?r?|\d+bits?|-[^ ]+$)|s?u?b?french|blueray|aac-[^-]+$|",
        #     "",
        #     name,
        # )

        name = sub("[\.\+_,]", " ", name)  # Replace the . or + by a dash
        # name = sub("-.{3,}$", "", name) # Remove uploader
        for banned in (r'HDR', r'.26[45]', r'webr?i?p?', r'multi', r'vostf?r?', r'\d+bits?', r's?u?b?french', r'bluray', r' aac ', r'ac3', r'5[ \.-]1', r'hdlight', r'1080.?', r'720.?', r'vff', r'bdrip'):
            name = sub(banned, "", name)

        
        name = sub(" +", " ", name)  # Replace multiple spaces to one
        name = strip_accents(name)
        name = name.strip()
        name = name.replace(" ", "-")
        name = sub("-+", "-", name)
        name = json.dumps(name)
        uploaded = torrent["uploaded"]
        downloaded = torrent["downloaded"]
        added = torrent["added_on"]
        ratio = torrent["ratio"]
        category = torrent["category"]
        size = torrent["size"]

        yield f"qbittorrent,category={category},name={name} uploaded={uploaded}u,downloaded={downloaded}u,added={added}u,ratio={ratio},size={size}u"

if __name__ == "__main__":
    for i in collect():
        print(i)




# Qbittorrent dump example
"""
{
   "added_on":1654964880,
   "amount_left":0,
   "auto_tmm":true,
   "availability":-1,
   "category":"radarr",
   "completed":1682939125,
   "completion_on":1654964917,
   "content_path":"/data/downloads/radarr/Ratatouille.2007.MULTi.1080p.BluRay.HDLight.x265-H4S5S.mkv",
   "dl_limit":-1,
   "dlspeed":0,
   "download_path":"",
   "downloaded":0,
   "downloaded_session":0,
   "eta":8640000,
   "f_l_piece_prio":false,
   "force_start":false,
   "hash":"38c48be51ebb0eae8062a85a61744dab96f0b467",
   "infohash_v1":"38c48be51ebb0eae8062a85a61744dab96f0b467",
   "infohash_v2":"",
   "last_activity":1656456161,
   "magnet_uri":"magnet:?xt=urn:btih:38c48be51ebb0eae8062a85a61744dab96f0b467&dn=Ratatouille.2007.MULTi.1080p.BluRay.HDLight.x265-H4S5S.mkv&tr=http%3a%2f%2ftracker.p2p-protocol.org%3a8080%2f7JjEj0ziB8VBu4HgRSk7LB3o9wp1laR0%2fannounce",
   "max_ratio":-1,
   "max_seeding_time":-1,
   "name":"Ratatouille.2007.MULTi.1080p.BluRay.HDLight.x265-H4S5S.mkv",
   "num_complete":296,
   "num_incomplete":33,
   "num_leechs":0,
   "num_seeds":0,
   "priority":0,
   "progress":1,
   "ratio":0.4617458340924839,
   "ratio_limit":-2,
   "save_path":"/data/downloads/radarr",
   "seeding_time":1489758,
   "seeding_time_limit":-2,
   "seen_complete":1656286225,
   "seq_dl":false,
   "size":1682939125,
   "state":"stalledUP",
   "super_seeding":false,
   "tags":"",
   "time_active":1489754,
   "total_size":1682939125,
   "tracker":"http://tracker.p2p-protocol.org:8080/7JjEj0ziB8VBu4HgRSk7LB3o9wp1laR0/announce",
   "trackers_count":1,
   "up_limit":-1,
   "uploaded":777090130,
   "uploaded_session":324082097,
   "upspeed":0
}
"""