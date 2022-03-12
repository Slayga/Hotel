"""
Name: Gabriel Engberg
Date: 02-03-2022
Info:
Keep track of how to handle certain issues and 
example solutions//general direction to the solution.
"""
import json
import imgui
import os

# Create folder "json" in the current working directory
path = os.path.dirname(__file__)
if not os.path.exists(path + "\\json"):
    os.makedirs(path + "\\json", exist_ok=True)


def test_basic_json():
    """Basics for writing and reading json files.

    Returns:
        None: None
    """
    import json  # required...

    # Data to store
    dict_data = {"name": "bob", "misc": {"1": [1, 2, 3, 4]}}

    # ? Writing data with context manager // will automatically close file... f.close(), '(__exit__)'
    with open(path + "/json/example.json", "w") as f:
        # Always have keys as strings ({"1": 1}) and avoid int ({1: 1}):
        json.dump(dict_data, f)  # dumps the data into the file...
        # ! note the mode in open("...", "w") -> "w" will overwrite the file not append

    # ? Reading data with context manager...
    with open(path + "/json/example.json") as f:
        json_content = json.load(f)  # json.loads(<file>) will return the dict
        # No need to pass mode in open() as default is "r" (read)

    # Fact check the results from the read (json.load(f))...
    print(json_content, type(json_content))


def test_empty_json():
    import json

    # Write an empty dict to not crash when reading json...
    with open(path + "/json/test_empty.json", "w") as f:
        json.dump({}, f)

    with open(path + "/json/test_empty.json") as f:
        empty_json = json.load(f)
    print(empty_json)


def test_writing_json():
    # Below is acceptable way to stor & write json
    dict_str_key = {str(): int()}
    # While this will be converted by json.dump(...) to dict_str_key
    dict_int_key = {int(): int()}
    ...


def test_pretty_print(content, indent: int = 0):
    # How to read and pretty-print the dicts.
    # This is just to visually see the what is assigned to what...
    if isinstance(content, dict):
        for k, v in content.items():
            print(" " * indent, k)
            if isinstance(v, dict):
                test_pretty_print(v, indent + 2)  # Recursive
            else:
                print(" " * (indent + 1), v)
    else:
        print(" " * (indent + 1), content)


if __name__ == "__main__":
    # 1
    test_basic_json()
    # 2
    test_empty_json()
    # 3
    with open("test/json/bobdump.json") as f:
        json_content = json.load(f)
    test_pretty_print(json_content)
    # 4
    ...
