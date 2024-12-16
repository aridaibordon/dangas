import os
import pandas as pd

from read import get_header_data
from data import get_data
from utils import ORDER_KEYS


def get_col(data: list[dict]) -> list:
    order_keys = ORDER_KEYS.split()

    data_dict = {item["name"]: item for item in data}

    col = []
    for key in order_keys:
        sample = data_dict.get(key)

        if sample == None:
            col.extend(["-", "-", "-"])
            continue

        a, u, mda = sample["a"], sample["u"], sample["mda"]
        col.extend([a, u, mda])

    return col


def create_excel(path_to_folder: str, fname: str) -> None:
    files = os.listdir(path_to_folder)

    cols = []
    headers = []
    for file in files:
        cfname, ext = file.split(".")

        if not (ext == "RPT"):
            continue

        header = get_header_data(cfname)
        headers.append(header)

        sample_col = [header["height"], header["mass"], header["time"], header["date"]]

        raw_data = get_data(os.path.join(path_to_folder, file))
        sample_col.extend(get_col(raw_data))

        cols.append(sample_col)

    index = [header["sample"] for header in headers]
    columns = []
    columns.extend("height mass time date".split())
    for key in ORDER_KEYS.split():
        columns.extend([f"a ({key})", f"u ({key})", f"mda ({key})"])

    df = pd.DataFrame(cols, index=index, columns=columns)
    df.to_excel(fname)


def main():
    print("DANGAS - Data automation for Neus gamma spectrometry.")
    print()

    path_to_data = input("Path to folder data: ")
    fname = input("New file name: ")
    print()

    create_excel(path_to_data, f"{fname}.xlsx")
    print("File created!")


if __name__ == "__main__":
    main()
