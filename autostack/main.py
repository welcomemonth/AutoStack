import autostack
from pathlib import Path
from autostack.const import ROOT, CONFIG_ROOT, DEFAULT_WORKSPACE_ROOT
from autostack.logs import logger
print(autostack.__file__)
print(Path.home())
print(ROOT)
print(CONFIG_ROOT)
print(DEFAULT_WORKSPACE_ROOT)

logger.info("xxx")
logger.error("xxx")
logger.debug("xxx")
logger.warning("xxx")

