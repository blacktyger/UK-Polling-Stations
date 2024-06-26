from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "SEG"
    addresses_name = "2024-05-02/2024-02-22T12:07:00.756391/Polling station data Somerset(Sedgemoor).csv"
    stations_name = "2024-05-02/2024-02-22T12:07:00.756391/Polling station data Somerset(Sedgemoor).csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()

        if uprn in [
            "10090855892",  # PUT HOUSE, FIDDINGTON, BRIDGWATER, TA51JW
            "100040899479",  # 135A TAUNTON ROAD, BRIDGWATER, TA6 6BD
            "10009322907",  # CHESTNUT HOUSE, EASTERTOWN, LYMPSHAM, WESTON-SUPER-MARE
            "10009320475",  # RIVERSIDE FARM, BIDDISHAM LANE, BIDDISHAM, AXBRIDGE
            "200000444031",  # POOLBRIDGE FARM HOUSE POOLBRIDGE ROAD, BLACKFORD, WEDMORE
            "200000449171",  # HILLFURLONG, CHILTON POLDEN HILL, BRIDGWATER
            "10090856797",  # OWERY BARN OWERY FARM OWERY FARM LANE, MIDDLEZOY, BRIDGWATER
            "10009328298",  # OWERY FARM, MIDDLEZOY, BRIDGWATER
            "200001842896",  # OLD COTTAGE, PIGHTLEY, SPAXTON, BRIDGWATER
            "200000439799",  # THE SLADES, BROOMYLAND HILL, SPAXTON, BRIDGWATER
            "200000451064",  # WRENMORE ELMS, FIDDINGTON, BRIDGWATER
            "10009318823",  # CHESTNUT HOUSE, DOWNEND ROAD, PURITON, BRIDGWATER
            "10009327419",  # PEDWA BARNS, HUNTSPILL ROAD, HIGHBRIDGE
            "100040907181",  # PRIORY COURT CARE HOME, 19 OXFORD STREET, BURNHAM-ON-SEA
            "10009323643",  # FLAT 1, 20 COLLEGE STREET, BURNHAM-ON-SEA
            "10090856573",  # 6 THE GABLES, ALLANDALE ROAD, BURNHAM-ON-SEA
            "10023415613",  # 15A ALLANDALE ROAD, BURNHAM-ON-SEA
            "200000448816",  # RIVERSIDE FARM, LOWER WEARE, AXBRIDGE
            "200000450711",  # GOLD CORNER BUNGALOW, EAST HUNTSPILL, HIGHBRIDGE
            "100040887755",  # CROSSING COTTAGE, GOOSE LANE, CHILTON POLDEN, BRIDGWATER
            "100041114944",  # HOMESTILL BUNGALOW, BLAKEWAY, WEDMORE
            "10009328207",  # LITTLE ORCHARD FARM, WASHBROOK, WEDMORE
            "10009328197",  # NEW TYNING, STONE ALLERTON, AXBRIDGE
            "200000446874",  # LAMBRIDGE HOUSE, SPAXTON, BRIDGWATER
            "10009323237",  # HALLICKS FARM, CHILTON TRINITY, BRIDGWATER
            "200000445815",  # NORTHOVER, FIDDINGTON, BRIDGWATER
        ]:
            return None

        if record.housepostcode in [
            # splits
            "BS27 3EP",
            "TA6 4HB",
            "TA6 6RZ",
            "TA5 2PF",
            "TA6 6QH",
            "TA6 5NL",
            "TA6 6LJ",
            "TA6 7BS",
            "TA6 6LR",
            "TA6 6GD",
            "BS24 0HD",  # BREAN ROAD, LYMPSHAM, WESTON-SUPER-MARE
            "TA7 9AG",  # FORD LODGE, STAWELL, BRIDGWATER
            "TA9 4HP",  # SOUTH VIEW, BRIDGWATER ROAD, EAST BRENT, HIGHBRIDGE
            "TA9 4HL",  # BRISTOL ROAD, BRENT KNOLL, HIGHBRIDGE
            "BS24 0HD",  # BREAN ROAD, LYMPSHAM, WESTON-SUPER-MARE
            "TA8 2RW",  # THE PILLARS RED ROAD, BERROW, BURNHAM-ON-SEA
            "TA6 4DF",  # CASTLEFIELDS COTTAGES, CASTLEFIELDS, BRIDGWATER
            "TA94RB",  # WATCHFIELD, HIGHBRIDGE
        ]:
            return None

        return super().address_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)
