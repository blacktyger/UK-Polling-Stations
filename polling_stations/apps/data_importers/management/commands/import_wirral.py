from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRL"
    addresses_name = (
        "2023-05-04/2023-02-22T10:54:17.531032/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-22T10:54:17.531032/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "42068483",  # 4 LORNE ROAD, PRENTON
            "42205588",  # 105 GROVE ROAD, WALLASEY
            "42005155",  # TOP FLOOR FLAT 9 ATHERTON STREET, NEW BRIGHTON"# ,
            "42192662",  # FRANKBY HALL FRANKBY CEMETERY MONTGOMERY HILL, FRANKBY
        ]:
            return None

        if record.addressline6 in [
            "CH49 3PG",
            "CH49 2SE",
            "CH62 8AB",
            "CH42 9PD",
        ]:
            return None

        return super().address_record_to_dict(record)
