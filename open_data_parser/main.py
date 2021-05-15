"""main"""
import json
import os
import shutil
from typing import Iterable
from typing import Dict
from typing import List
from typing import Callable

from open_data_parser.downloader import fetch_csv
from open_data_parser.transformer import add_city_name
from open_data_parser.transformer import query_coordinate_from_address
from open_data_parser.formatter.points import format_to_point

TARGETS = [
    {
        "url": "https://www.city.funabashi.lg.jp/opendata/002/p059795_d/fil/syokibohoikuichiran.csv",
        "input_schema": [
            "name",
            "address",
            "phone_number",
            "capacity",
            "established_at",
        ],
        "transformer": [
            add_city_name,
            query_coordinate_from_address,
        ],
        "formatter": format_to_point,
        "output": {
            "path": "data/kosodate-map/",
            "filename": "syokibohoikuichiran.json",
        },
    }
]


def transform(
    transformers: List[Callable[[Iterable[Dict]], Iterable[Dict]]], data: Iterable[Dict]
) -> Iterable[Dict]:

    for transformer in transformers:
        data = transformer(data)

    return data


def write(filepath: str, data):
    with open(filepath, "w") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def main():
    for target in TARGETS:
        shutil.rmtree(target["output"]["path"])
        os.makedirs(target["output"]["path"])
        raw_data = fetch_csv(target["url"], target["input_schema"])

        transformed = transform(target["transformer"], raw_data)

        write(
            f'{target["output"]["path"]}/{target["output"]["filename"]}',
            list(transformed),
        )


if __name__ == "__main__":
    main()
