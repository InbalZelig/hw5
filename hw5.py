import pathlib
import re
from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        if isinstance(data_fname, str):
            data_fname = pathlib.Path(data_fname)
        if not isinstance(data_fname, pathlib.Path):
            raise TypeError
        if not pathlib.Path.exists(data_fname):
            raise ValueError
        self.data_fname = data_fname
        self.data = None

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.

        Returns
        -------
        hist : np.ndarray
          Number of people in a given bin
        bins : np.ndarray
          Bin edges
            """
        ages = self.data['age']
        bins_list = np.arange(start=0, stop=101, step=10)
        hist, bins, _ = plt.hist(ages, bins=bins_list)
        # plt.show()
        return hist, bins

    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

        Returns
        -------
        df : pd.DataFrame
          A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
          the (ordinal) index after a reset.
        """
        indexes = self.data[self.data['email'].apply(self.__is_invalid_email)].index
        df = self.data.drop(indexes).reset_index(drop=True)
        return df

    def __is_invalid_email(self, email: str) -> bool:
        # TODO: improve function
        if str.find(email, '@') == -1 or str.find(email, '.') == -1:
            return True
        if email[0] in ['@', '.'] or email[-1] == ['@', '.']:
            return True
        match_at_indices = [m.start() for m in re.finditer('@', email)]
        if len(match_at_indices) != 1:
            return True
        if email[match_at_indices[0] + 1] == '.':
            return True
        return False
        # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # if re.search(regex, email):
        #     return False
        # return True
