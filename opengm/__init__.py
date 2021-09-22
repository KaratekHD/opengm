import logging
import sys
import os
import configparser
import json
VERSION = "3.0"
# Module name
__MOD_NAME__ = "init"


# Setup logging
LOGGER = logging.getLogger(__name__)
DEBUG = True
LOGFORMAT = "[%(asctime)s | %(levelname)s] %(message)s"
if DEBUG:
    logging.basicConfig(
        format=LOGFORMAT,
        level=logging.DEBUG)
else:
    logging.basicConfig(
        format=LOGFORMAT,
        level=logging.INFO)

LOGGER.info(
    f"OpenGM v{VERSION}\n"
    f"This program is free software: you can redistribute it and/or modify\n"
    f"it under the terms of the GNU General Public License as published by\n"
    f"the Free Software Foundation, either version 3 of the License, or\n"
    f"(at your option) any later version.")

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.fatal(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    sys.exit(1)

ENV = bool(os.environ.get('ENV', False))
if ENV:
    pass
else:
    if not os.path.exists("config.ini"):
        LOGGER.fatal(
            "The README is there to be read! Create a configuration file first!")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read("config.ini")
    TELEGRAM_TOKEN = config["TELEGRAM"]["API_KEY"]
    try:
        OWNER_ID = int(config["OWNER"]["OWNER_ID"])
    except ValueError:
        raise Exception("Invalid OWNER_ID") # ERR_CONFIG_INVALID_OWNER_ID
    BOT_NAME = config["BOT"]["NAME"]
    OWNER_USERNAME = config["OWNER"]["OWNER_USERNAME"]
    NO_LOAD = json.loads(config["MODULES"]["NO_LOAD"])
    LOAD = json.loads(config["MODULES"]["LOAD"])
