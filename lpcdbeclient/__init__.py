from .logger import setup_custom_logger
logger = setup_custom_logger('root')
logger.debug('Logger imported')

from . import utils
from .data import Data
from .client import Client