import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load():
    plugins = [plugin.stem for plugin in Path(__file__).parent.glob('*.py')]
    for plugin in plugins:
        if '__init__' not in plugin:
            importlib.import_module(f'{__name__}.{plugin}')
            logger.debug(f'Plugin {plugin} loaded')
