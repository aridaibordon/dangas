import pandas as pd


def get_header_data(fname: str):
    raw_header = fname.split("_")
    sample, w1, w2, h, d, m, y, time = raw_header[1:9]
    return {
        "sample": sample,
        "mass": f"{w1}.{w2}",
        "height": h,
        "time": time,
        "date": f"{m}/{d}/{y}",
    }


def get_mda_report(fdata, mda_ind):
    hsize = 13

    start_index = mda_ind + hsize if fdata[mda_ind + hsize] else mda_ind + hsize + 1

    tab_data = []
    for line in fdata[start_index :]:
        if not line or line[0] == "":
            break

        if line[4] == "?":
            continue
        line = line[10:]  # remove indent

        data = line.split()

        if data[3] == "Failed":
            continue
        if len(data) < 7:
            data.insert(0, pdata[0])
            data.insert(4, pdata[4])

        data[1] = "".join(e for e in data[1] if e != "*")

        tab_data.append(data)
        pdata = data

    columns = [
        "name",
        "E",
        "yield",
        "mda",
        "nmda",
        "activity",
        "dec. thresh",
    ]
    return pd.DataFrame(tab_data, columns=columns)


def get_iso_report(fdata, iso_ind):
    hsize = 7

    tab_data = []
    for line in fdata[iso_ind + hsize :]:
        if not line:
            break

        line = line[3:]  # remove indent
        data = line.split()

        if len(data) == 9:
            data = [data[i] for i in [0, 1, 2, 3, 4, 7, 8]]

        if len(data) == 8:
            data = data[1:]

        if len(data) < 7:
            data.insert(0, pdata[0])
            data.insert(2, pdata[2])
            data.insert(3, pdata[3])
            data.insert(4, pdata[4])
            data.insert(5, pdata[5])
            data.insert(6, pdata[6])

        data[1] = "".join(e for e in data[1] if e != "*")

        tab_data.append(data)
        pdata = data

    columns = [
        "name",
        "mda",
        "dl",
        "cf lower",
        "cf upper",
        "be activity",
        "be error",
    ]
    return pd.DataFrame(tab_data, columns=columns)


def get_id_report(fdata, id_ind):
    hsize = 11

    tab_data = []
    for line in fdata[id_ind + hsize :]:
        if not line:
            break

        data = line.split()
        if len(data) < 6:
            data.insert(0, pdata[0])
            data.insert(1, pdata[1])
        if len(data) < 6:
            continue

        data[2] = "".join(e for e in data[2] if e != "*")

        tab_data.append(data)
        pdata = data

    columns = [
        "name",
        "id conf",
        "E",
        "yield",
        "act",
        "act error",
    ]
    return pd.DataFrame(tab_data, columns=columns)
