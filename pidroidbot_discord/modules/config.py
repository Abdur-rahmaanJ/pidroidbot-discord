import logging
import logging.config
import os
import pprint
from pathlib import Path
from sys import argv, exit

import yaml

from dotenv import find_dotenv, load_dotenv


_CONFIG_FILENAME = "config.yaml"
_DEFAULT_CONFIG = """
---

log:
  version: 1
  disable_existing_loggers: false
  handlers:
    stderr:
      class: logging.StreamHandler
      stream: ext://sys.stderr
      level: DEBUG

  loggers:
    main:
      level: DEBUG
      handlers: [stderr]
    cogs:
      level: INFO
      handlers: [stderr]


"""


def get_config():
    """get configuration from config.yml (created if not exists, upgraded when needed"""

    try:
        config_file = os.getenv(
            "BOT_MARKDOWN_DISCORD__CONFIG_FILE",
            find_dotenv(filename=_CONFIG_FILENAME, raise_error_if_not_found=True),
        )
        print("found", config_file)
    except IOError as e:
        config_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(argv[0]))), _CONFIG_FILENAME
        )

        with open(config_file, "w") as f:
            f.write(_DEFAULT_CONFIG)
            f.close()
        print(f"Didn't find conf file, autoregenerated into {config_file}")
        exit(1)

    # load default conf and override with config_file
    config_content = yaml.safe_load(_DEFAULT_CONFIG)
    config_content.update(yaml.safe_load(Path(config_file).read_text()))

    logging.config.dictConfig(config_content["log"])
    return config_content
