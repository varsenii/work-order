import json

original_json = """
{
  "name": "Jane",
  "age": 35,
  "address": {
    "zip": "90001",
    "city": "Los Angeles"
  }
}
"""


def canonilize(data):
    obj = json.loads(data)

    def sort_keys_recursive(obj):
        if isinstance(obj, dict):
            return {
                key: sort_keys_recursive(value) for key, value in sorted(obj.items())
            }
        elif isinstance(obj, list):
            return [sort_keys_recursive(item) for item in obj]
        else:
            return obj

    sorted_obj = sort_keys_recursive(obj)

    canoncial_json = json.dumps(sorted_obj)

    return canoncial_json
