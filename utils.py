def find_key_by_value(dictionary: dict, value_to_find):
    return [record[0] for record in dictionary.items() if record[1] == value_to_find]
