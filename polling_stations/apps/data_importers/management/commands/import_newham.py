from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = (
        "2024-05-02/2024-02-13T12:39:14.813267/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-13T12:39:14.813267/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
