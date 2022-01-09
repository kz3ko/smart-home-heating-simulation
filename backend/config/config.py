from utilities.util import get_data_from_json


CONFIG_PATH = './config/config.json'
HOUSE_CONFIG = get_data_from_json(CONFIG_PATH)['house']
RESIDENTS_CONFIG = get_data_from_json(CONFIG_PATH)['residents']
