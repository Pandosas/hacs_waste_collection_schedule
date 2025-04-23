import json
from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Ekonovus"
DESCRIPTION = 'Source for UAB "Ekonovus".'
URL = "https://grafikai.svara.lt"
TEST_CASES = {
    "Demokratų g. 7, Kaunas": {
        "region": "Kauno m. sav.",
        "street": "Demokratų g.",
        "house_number": "7",
        "waste_object_ids": [101358, 100858, 100860],
    },
    "Alytaus g. 2, Išlaužo k., Išlaužo sen. Prienų r. sav.": {
        "region": "Prienų r. sav.",
        "street": "Alytaus g.",
        "house_number": "2",
        "district": "Išlaužo sen.",
    },
}

ICON_MAP = {
    "mišrių atliekų": "mdi:trash-can",
    "antrinių žaliavų (popierius/plastikas)": "mdi:recycle",
    "antrinių žaliavų (stiklas)": "mdi:glass-fragile",
    "žaliųjų atliekų": "mdi:leaf",
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8',
    'ActivityId': '87d287ea-3a5f-e45b-d040-132389997968',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://app.powerbi.com',
    'Referer': 'https://app.powerbi.com/',
    'RequestId': '057406d7-ce10-26c6-005e-18a749d53f05',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-PowerBI-ResourceKey': 'd86dc3d4-e915-4460-b12e-c925d3ae6c75',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'synchronous': 'true',
}

class Source:
    API_URL = "https://wabi-west-europe-d-primary-api.analysis.windows.net/"

    def __init__(
        self, region, street, house_number, district=None, waste_object_ids=None
    ):
        if waste_object_ids is None:
            waste_object_ids = []
        self._region = region
        self._street = street
        self._house_number = house_number
        self._waste_object_ids = waste_object_ids
        self._district = district

    def fetch(self):
        response = requests.post(
            'https://wabi-west-europe-d-primary-api.analysis.windows.net/public/reports/querydata',
            params=params,
            headers=headers,
            json={"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"s","Entity":"ScheduleDates","Type":0},{"Name":"w","Entity":"WasteObject","Type":0},{"Name":"a","Entity":"AllAddresses","Type":0},{"Name":"t","Entity":"Teritorijos konteinerių tvarkaraščiams","Type":0},{"Name":"s1","Entity":"Schedule","Type":0}],"Select":[{"Measure":{"Expression":{"SourceRef":{"Source":"s"}},"Property":"Datos"},"Name":"ScheduleDates.Datos"}],"Where":[{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"w"}},"Property":"Adresas"}}],"Values":[[{"Literal":{"Value":"'Miriniškių k. Laurų g. 12-1'"}}]]}}},{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"w"}},"Property":"Inventorinis nr."}}],"Values":[[{"Literal":{"Value":"'52-P-41136 (Pakuotė)'"}}]]}}},{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"a"}},"Property":"District"}}],"Values":[[{"Literal":{"Value":"'Kauno r. sav.'"}}]]}}},{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"s"}},"Property":"Future"}}],"Values":[[{"Literal":{"Value":"'true'"}}]]}}},{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Rodomas tvarkaraštis"}}],"Values":[[{"Literal":{"Value":"'1'"}}]]}}},{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"s"}},"Property":"OverNextRun"}}],"Values":[[{"Literal":{"Value":"true"}}]]}}},{"Condition":{"Not":{"Expression":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"s1"}},"Property":"ScheduleId"}}],"Values":[[{"Literal":{"Value":"7127L"}}],[{"Literal":{"Value":"7128L"}}],[{"Literal":{"Value":"7129L"}}],[{"Literal":{"Value":"7131L"}}],[{"Literal":{"Value":"7132L"}}],[{"Literal":{"Value":"7133L"}}],[{"Literal":{"Value":"7134L"}}],[{"Literal":{"Value":"7135L"}}],[{"Literal":{"Value":"7136L"}}],[{"Literal":{"Value":"7137L"}}],[{"Literal":{"Value":"7138L"}}],[{"Literal":{"Value":"7139L"}}],[{"Literal":{"Value":"7140L"}}],[{"Literal":{"Value":"7141L"}}]]}}}}},{"Condition":{"And":{"Left":{"Not":{"Expression":{"Contains":{"Left":{"Column":{"Expression":{"SourceRef":{"Source":"w"}},"Property":"Inventorinis nr."}},"Right":{"Literal":{"Value":"'siuk'"}}}}}},"Right":{"Not":{"Expression":{"Contains":{"Left":{"Column":{"Expression":{"SourceRef":{"Source":"w"}},"Property":"Inventorinis nr."}},"Right":{"Literal":{"Value":"'šiuk'"}}}}}}}}}]},"Binding":{"Primary":{"Groupings":[{"Projections":[0]}]},"DataReduction":{"DataVolume":3,"Primary":{"Top":{}}},"Version":1},"ExecutionMetricsKind":1}}]},"QueryId":"","ApplicationContext":{"DatasetId":"90015897-045e-4f68-8f83-c40d1fc3bfc2","Sources":[{"ReportId":"06fc8043-9afa-43d6-88cc-3a1e73aaf964","VisualId":"161c6ed98b10564c91b7"}]}}],"cancelQueries":[],"modelId":1026609},
        )

        data = json.loads(response.text)

        entries = []

        entriesString = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"][0]["M0"]
        dateEntries = entriesString.replace('.','').split(", ")

        for collection_waste_object in dateEntries:
            entries.append(
                Collection(
                    date=datetime.strptime(
                        collection_waste_object, "%Y-%m-%d"
                    ).date(),
                    t="antrinių žaliavų (popierius/plastikas)",
                    icon="mdi:recycle",
                )
            )

        return entries