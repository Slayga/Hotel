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

# Makes a directory in current working directory to store json files
os.makedirs("test", exist_ok=True)


def test_basic_json():
    """Basics for writing and reading json files.

    Returns:
        None: None
    """
    import json  # required...

    # Data to store
    dict_data = {"name": "bob", "misc": {"1": [1, 2, 3, 4]}}

    # ? Writing data with context manager // automatically closes file... f.close(), '(__exit__)'
    with open("test/json/example.json", "w") as f:
        # Always have keys as strings ({"1": 1}) and avoid int ({1: 1}):
        json.dump(dict_data, f)  # dumps the data into the file...
        # ! note the mode in open("...", "w") -> "w" will overwrite the file

    # ? Reading data with context manager...
    with open("test/json/bobdump.json") as f:
        json_content = json.load(f)  # json.loads(<file>) will return the dict
        # No need to pass mode in open() as default is "r" (read)

    # Fact check the results from the loading...
    print(json_content, type(json_content))


def test_empty_json():
    import json

    # Write an empty dict to not crash when reading json...
    with open("test/json/example.json", "w") as f:
        json.dump({}, f)
    with open("test/json/example.json") as f:
        empty_json = json.load(f)
    print(empty_json)


def test_writing_json():
    # {str(): int()} is acceptable
    # {int(): int()} will be converted by json.dump(...) to {str(): int()}
    ...


def test_pretty_print(content, indent: int = 0):
    # How to read and pretty-print the dicts.
    if isinstance(content, dict):
        for k, v in content.items():
            print(" " * indent, k)
            if isinstance(v, dict):
                test_pretty_print(v, indent + 2)
            else:
                print(" " * (indent + 1), v)
    else:
        print(" " * (indent + 1), content)


if __name__ == "__main__":
    # 1
    # test_basic_json()
    # 2
    # test_empty_json()
    # 3
    # with open("test/json/bobdump.json") as f:
    #     json_content = json.load(f)
    # test_pretty_print(json_content)
    # 4
    ...
