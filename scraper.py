from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
import csv
import pytz
from datetime import datetime as d, timedelta
import requests

est = pytz.timezone("US/Eastern")
NUMBER_OF_ENTRIES: int = 7476  # 596
eventCourseId = 1723361  # 1763149
eventId = 891887  # 901227
fieldnames = []
result_file = open(f"{eventId}_{eventCourseId}.csv", "a+", newline="")
writer = csv.DictWriter(result_file, fieldnames=fieldnames)


def from_millis_to_hms(millis: int) -> str:
    if millis > 0:
        return str(timedelta(milliseconds=millis))
    else:
        return "--:--:--"


def page_request(page):
    params = {"eventCourseId": eventCourseId,
              "from": page,
              "limit": 100
              }
    while True:
        r = requests.get(f"https://results.athlinks.com/event/{eventId}", params=params)

        if r.status_code == 200:
            print(r.url, "--------> ", "succeeded with code:", r.status_code)
            return r.json()[0]["interval"]["intervalResults"]
        else:
            pass
            print(r.url, "--------> ", "failed with code:", r.status_code)


def get_bibs():
    pages = range(0, NUMBER_OF_ENTRIES, 100)
    with ThreadPoolExecutor() as e:
        futures_list = [e.submit(page_request, page) for page in pages]
        json_list = [y for x in [x.result() for x in as_completed(futures_list)] for y in x]

    return [x["bib"] for x in json_list]


def get_participant_data(bib):
    global fieldnames
    global writer

    params = {"bib": bib,
              "eventId": eventId,
              "eventCourseId": eventCourseId,
              }

    while True:
        data = requests.get("https://results.athlinks.com/individual", params=params)
        if data.status_code == 200:
            print(data.url, "--------> ", "succeeded with code:", data.status_code)
            r = data.json()
            break
        else:
            print(data.url, "--------> ", "failed with code:", data.status_code)

    name = r.get("displayName", "")
    gender = r.get("gender", "")
    city_state = f"{r.get('region', '')} {r.get('regionId', '')}"
    chip_start_time_int = int(r.get("racerStartTime", {}).get("timeInMillis", "0"))
    chip_start_time = f"{d.fromtimestamp(chip_start_time_int / 1000.0, est):%-I:%M:%S %p EST}"

    row = {"Bib": bib,
           "Name": name,
           "Gender": gender,
           "City/State": city_state,
           "Chip Start Time": chip_start_time,
           "Gun Time": ""}

    for interval in r.get("intervals", []):
        name = f'{interval.get("intervalName", "")} Time'
        value = int(interval.get("chipTime", {}).get("timeInMillis"))
        if name[:-5] == "Full Course":
            row["Gun Time"] = from_millis_to_hms(int(interval.get("gunTime", {}).get("timeInMillis")))

        row[name] = from_millis_to_hms(value)

    if not fieldnames:
        fieldnames = list(row.keys())
    writer = csv.DictWriter(result_file, fieldnames=fieldnames)
    writer.writerow(row)


print("Collecting Bibs ...")

bibs = get_bibs()

print("Bibs Collection Finished")

print("Getting participant data ...")

#  Added concurrency for performance boost
with ThreadPoolExecutor() as executor:
    [executor.submit(get_participant_data, bib) for bib in bibs]

writer.writeheader()
result_file.close()
print("Process Completed Successfully")
