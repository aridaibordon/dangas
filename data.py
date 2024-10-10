from read import get_mda_report, get_iso_report, get_id_report
from utils import ISO_KEYS, ID_KEYS, get_tab_pos, nuc_info


def get_iso_data(rpt_path: str) -> list[dict]:
    fdata, tab_ind = get_tab_pos(rpt_path)

    mda_data = get_mda_report(fdata, tab_ind[0])
    iso_data = get_iso_report(fdata, tab_ind[1])

    data = []
    for key in ISO_KEYS:
        index = iso_data.index[iso_data["name"] == key].to_list()

        if len(index) == 0:
            index = mda_data.index[mda_data["name"] == key].to_list()
            if len(index) == 0:
                continue
            mda = mda_data.loc[index[0]]["mda"]
            data.append(nuc_info(key, float(mda)))
            continue

        row = iso_data.loc[index[0]]
        if float(row["mda"]) == 0.0:
            nuc_data = nuc_info(key, "-", float(row["be activity"]), float(row["be error"]))
        else:
            nuc_data = nuc_info(key, float(row["mda"]), float(row["be activity"]), float(row["be error"]))
            
        data.append(nuc_data)

    return data


def get_id_data(rpt_path: str) -> list[dict]:
    fdata, tab_ind = get_tab_pos(rpt_path)

    mda_data = get_mda_report(fdata, tab_ind[0])
    id_data = get_id_report(fdata, tab_ind[3])

    data = []

    for key, energy in ID_KEYS:
        index_id = id_data.index[id_data["E"] == str(energy)].to_list()
        index_mda = mda_data.index[mda_data["E"] == str(energy)].to_list()

        row_id = id_data.loc[index_id[0]]

        if index_mda:
            row_mda = mda_data.loc[index_mda[0]]
            a, u, mda = float(row_id["act"]), float(row_id["act error"]), float(row_mda["mda"])
        else:
            a, u, mda = float(row_id["act"]), float(row_id["act error"]), "-"

        data.append(nuc_info(key, mda, a, u))

    return data


def get_data(rpt_path: str):
    iso_data = get_iso_data(rpt_path)
    id_data = get_id_data(rpt_path)

    return iso_data + id_data
