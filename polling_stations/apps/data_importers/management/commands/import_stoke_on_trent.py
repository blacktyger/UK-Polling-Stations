from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STE"
    addresses_name = (
        "2023-05-04/2023-02-09T14:44:06.144885/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-09T14:44:06.144885/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "3455154988",  # RAILWAY COTTAGE, WEDGWOOD DRIVE, BARLASTON, STOKE-ON-TRENT
            "3455107917",  # IVY COTTAGE, WOODPARK LANE, STOKE-ON-TRENT
            "3455010479",  # ABBEY FARM, BIRCHES HEAD ROAD, STOKE-ON-TRENT
            "3455040966",  # 192 STAR & GARTER ROAD, STOKE-ON-TRENT
            "3455031193",  # 602 DIVIDY ROAD, STOKE-ON-TRENT
            "3455069351",  # 152 MOORLAND ROAD, STOKE-ON-TRENT
            "3455097202",  # 676 TRENTHAM ROAD, STOKE-ON-TRENT
            "3455097203",  # 678 TRENTHAM ROAD, STOKE-ON-TRENT
            "3455082463",  # THE BUNGALOW, ST. JOSEPHS PLAYING FIELDS, HANFORD, STOKE-ON-TRENT
            "3455121942",  # BURSLEM GOLF CLUB, HIGH LANE, STOKE-ON-TRENT
        ]:
            return None

        if record.addressline6 in [
            "ST4 2JY",
            "ST3 7RX",
            "ST4 2LE",
            "ST3 4DH",
            "ST4 8ND",
            "ST6 3BF",
            "ST4 3HH",
            "ST3 5HU",
            "ST3 2QX",
            "ST3 6DU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Cuckoo Barleston Road Stoke On Trent (ST3 3LD)
        if record.polling_place_id == "15958":
            record = record._replace(polling_place_postcode="ST4 4DH")

        return super().station_record_to_dict(record)
