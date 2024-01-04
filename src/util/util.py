# -*- coding: utf-8 -*-


class LoadData:
    """Class that loads data from different file formats."""

    @staticmethod
    def isvalid(fp) -> bool:
        """Checks whether a file path is valid and supported.
        The supported formats are: CSV and JSON kk.

          Arguments:
              fp (str): The path of the file to be checked.

          Returns:
              bool: True if the file path is valid and has a supported format; False otherwise.
        """
        from os.path import isfile
        from pathlib import Path

        fp = str(Path(fp))

        if not isfile(fp):
            return False

        match fp[len(fp) - 4 :]:

            case '.csv':
                return True

            case 'json':
                return True

            case _:
                return False

    @staticmethod
    def load_csv(fp: str) -> dict:
        """Loads data from a CSV file.

        Args:
            fp (str): The file path of the CSV file.

        Returns:
            dict: A dictionary containing the data from the CSV file.
        """
        from csv import DictReader

        with open(fp, mode='r', encoding='utf-8') as file:
            dict_csv = DictReader(file)
            return dict_csv

    @staticmethod
    def load_json(fp: str) -> dict:
        """Loads data from a JSON file.

        Args:
            fp (str): The file path of the JSON file.

        Returns:
            dict: A dictionary containing the data from the JSON file.
        """
        from json import load

        dict_json = load(fp)

        return dict_json
