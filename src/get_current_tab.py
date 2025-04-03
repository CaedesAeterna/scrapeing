import pathlib, requests, json, lz4.block


# /home/caedes/.mozilla/firefox/fsaqzro1.default-esr/sessionstore-backups/recovery.jsonlz4

# Adjust the path to your Firefox profile's sessionstore file:
# profile = pathlib.Path.home() / ".mozilla/firefox" / "yourprofile.default-release" / "sessionstore-backups" / "recovery.jsonlz4"

# Adjust the path to your Firefox profile's sessionstore file:
profile = (
    pathlib.Path.home()
    / ".mozilla/firefox"
    / "fsaqzro1.default-esr"
    / "sessionstore-backups"
    / "recovery.jsonlz4"
)

with open(profile, "rb") as f:
    f.read(8)  # skip the header
    data = json.loads(
        lz4.block.decompress(f.read()).decode("utf-8")
    )  # decode the jsonlz4 data

# Get the active tab from the first window
window = data["windows"][0]
# The active tab is at index 0
active_index = window["selected"] - 1  # Firefox uses 1-indexed value
# Get the active tab
active_tab = window["tabs"][active_index]
# The current URL is in the latest entry of this tab's history:
url = active_tab["entries"][active_tab["index"] - 1]["url"]
print(url)

# Get the HTML of the current page
# url = "https://www.google.co.uk/"
response = requests.get(url)
html = response.text
