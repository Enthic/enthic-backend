# -*- coding: utf-8 -*-
"""
=====================================================================
Sum all the bundle of the year for one company from a CSV sorted file
=====================================================================

PROGRAM BY PAPIT SASU, 2019

Coding Rules:

- Snake case for variables.
- Only argument is configuration file.
- No output or bundle_file.write, just log and files.
"""
from csv import reader
from json import load
from logging import basicConfig
from os.path import isdir, join, dirname

################################################################################
# CHECKING THE INPUT AND OUTPUT AND DIRECTORY PATH
# INPUT
with open(join(dirname(__file__), "configuration.json")) as json_configuration_file:
    CONFIG = load(json_configuration_file)
# OUTPUT
if isdir(CONFIG['outputPath']) is False:
    raise NotADirectoryError(
        "Configuration output path {} does not exist".format(
            CONFIG['outputPath'])
    )

################################################################################
# SET LOG LEVEL
basicConfig(level=CONFIG['debugLevel'],
            format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)")


def main():
    """
    Based on the configuration storing the input file path. Sum all the bundle
    of the year for one company.
    """
    ############################################################################
    # RESULT FILE
    bundle_file = open(join(CONFIG['outputPath'], CONFIG['bundleFile']), "w")
    csv_separator = CONFIG['csvSeparator']
    ############################################################################
    # READ THE INPUT FILE AND bundle_file.write THE OUTPUT
    with open(join(CONFIG['outputPath'], CONFIG['sortTmpBundleFile']), mode='r') as infile:
        _reader = reader(infile, delimiter=csv_separator)  # READER OF THE INPUT CSV FILE
        key, bundle_sum, gain, distribution = (None,) * 4
        for rows in _reader:  # ITERATE EACH LINE
            if key is not None and key < rows[0:4]:  # KEY BREAK ON BUNDLE CODE
                bundle_file.write(csv_separator.join((key[0], key[1], key[2], key[3],
                                            str(bundle_sum), "\n"))
                                  )
            if key == rows[0:4]:  # SAME KEY, SUM THE BUNDLE AMOUNT
                bundle_sum += int(rows[4])
            else:
                key = rows[0:4]  # NEW KEY INITIATE BUNDLE AMOUNT
                bundle_sum = int(rows[4])
    bundle_file.close()


if __name__ == '__main__':
    main()  # ONLY IF EXECUTED NOT WHEN IMPORTED
