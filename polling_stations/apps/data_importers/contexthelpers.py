import requests
from addressbase.models import Address


def get_stat_from_nomis(dataset, measure, gss_code):
    """
    Obtains the number of 'dwellings' in a local authority from the:
    'KS401EW - Dwellings, household spaces and accommodation type' dataset.
    This is based on 2011 data, so is getting pretty out of date, but is
    a good sanity check.
    """
    url = "http://www.nomisweb.co.uk/api/v01/dataset/{dataset}.data.json?date=latest&geography={gss_code}&measures={measures}&c2021_dwell_1=0".format(
        dataset=dataset, gss_code=gss_code, measures=measure
    )
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        return 0
    if r.status_code != 200:
        return 0
    data = r.json()
    if "error" in data:
        return 0
    return data["obs"][0]["obs_value"]["value"]


class Dwellings:
    def from_census(self, gss_code):
        return get_stat_from_nomis("NM_2304_1", "20100", gss_code)

    def from_addressbase(self, polygon):
        return Address.objects.filter(location__within=polygon).count()
