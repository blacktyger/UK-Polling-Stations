from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUC"
    addresses_name = (
        "2025-05-01/2025-03-04T12:01:56.775425/Democracy_Club__01May2025 3.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-04T12:01:56.775425/Democracy_Club__01May2025 3.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000796229",  # MOORGATE COTTAGE, MOOR END, FRIETH, HENLEY-ON-THAMES
            "10090192931",  # MOBILE HOME AT STABLES AND PADDOCK WILLETTS LANE, DENHAM
            "766297724",  # RYE HOUSE THE HOLLOWAY, DRAYTON BEAUCHAMP
        ]:
            return None

        if record.addressline6 in [
            # split
            "SL9 9JH",
            "HP8 4QT",
            "HP23 6NG",
            "HP8 4DF",
            "SL0 0DB",
            "SL9 9FH",
            "HP5 3BD",
            "HP18 0RU",
            "RG9 6JH",
            "HP18 9UJ",
            # suspect
            "HP12 3HP",  # MCLELLAN PLACE
            "SL3 6QH",  # CROMWELLS COURT
        ]:
            return None

        return super().address_record_to_dict(record)
