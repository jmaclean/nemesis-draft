import urllib.request
import json
import os

with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as version_json:
    versions = json.load(version_json)

current_version = versions[0]
print(f"Loading champions from {current_version}")

with urllib.request.urlopen(f"https://ddragon.leagueoflegends.com/cdn/{current_version}/data/en_US/champion.json") as champion_json:
  champions = json.load(champion_json)

champion_names = [c["name"] for id, c in champions["data"].items()]

target_file = os.path.abspath("../static/champions.txt")
print(f"Writing champions to {target_file}")

with open(target_file, "wt") as champion_file:
  champion_file.write("\n".join(champion_names))


