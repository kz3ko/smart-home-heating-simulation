from json import loads


def get_data_from_json(json_path: str) -> dict:
    with open(json_path, 'r') as f:
        return loads(f.read())
