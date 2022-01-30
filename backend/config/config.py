from utilities.util import get_data_from_json


CONFIG_PATH = './config/config.json'
CONFIG = get_data_from_json(CONFIG_PATH)
HOUSE_CONFIG = CONFIG['house']
RESIDENTS_CONFIG = CONFIG['residents']
