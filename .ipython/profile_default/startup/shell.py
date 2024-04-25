# This is a pre-script for ipython
# It provides better experience and
# implements and analog
# for Django shell_plus:
# https://django-extensions.readthedocs.io/en/latest/shell_plus.html

import sys
sys.path = ["", ".."] + sys.path[1:]

from core import logger, BaseImportService # noqa E402

logger.info("Fast API Shell is started")


# Import all models
logger.info("\n\nImported models:")

models = BaseImportService.get_items(target_subfolders="models")

for model in models:
    vars()[model['name']] = model['value']
    logger.info(f"imported {model['value']}")


# Import all storages
logger.info("\n\nImported Storages:")

storages = BaseImportService.get_items(target_subfolders="storages")

for storage in storages:
    vars()[storage['name']] = storage['value']
    logger.info(f"imported {storage['value']}")


# Import all cases
logger.info("\n\nImported Cases:")

cases = BaseImportService.get_items(target_subfolders="cases")

for case in cases:
    vars()[case['name']] = case['value']
    logger.info(f"imported {case['value']}")
