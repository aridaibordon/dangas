ISO_KEYS = ["Be-7", "K-40", "Pb-210", "Pb-212", "RA-226", "TH-234", "U-235", "CS-137"]
ID_KEYS = [
    ("TL-208", "583.19"),
    ("BI-214", "609.31"),
    ("PB-214", "351.92"),
    ("AC-228", "911.60"),
]

ORDER_KEYS = "Be-7 K-40 TL-208 Pb-210 Pb-212 BI-214 PB-214 RA-226 AC-228 TH-234 U-235 CS-137"


def nuc_info(name: str, mda: float, a: float | str = "-", u: float | str = "-") -> dict:
    return {"name": name, "a": a, "u": u, "mda": mda}


def get_tab_pos(path: str) -> tuple[list]:
    """Return report data and the position of tables"""
    fdata = []
    tab_ind = []

    with open(path, "r") as f:
        for nline, line in enumerate(f):
            fdata.append(line.rstrip())
            if line[0] == "*":
                tab_ind.append(nline)

        tab_ind = tab_ind[1::3]
    return fdata, tab_ind
