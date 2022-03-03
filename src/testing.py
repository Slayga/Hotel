"""
Name: Gabriel Engberg
Date: 02-03-2022
Info:
Keep track of how to handle certain issues and 
example solutions//general direction to the solution.
"""
import json


def test_basic_json():
    # ! JSON
    # ? open and read file
    import json  # required...

    dict_data = {"name": "bob"}  # data to store (a dict)
    # ? Writing data with context manager // automatically closes file... f.close(), '(__exit__)'
    with open("src/json/example.json", "w") as f:
        json.dump(dict_data, f)  # dumps the data into the file...
        #! note the mode in open("...", "w") -> "w" will overwrite the current content of file

    # ? Reading data with context manager...
    with open("src/json/bobdump.json") as f:
        json_content = json.load(f)  # json.loads(<file>) will return the dict
        # No need to pass mode in open() as default is "r" (read)

    # Fact check the results from the loading...
    print(json_content, type(json_content))


def test_empty_json():
    import json

    with open("src/json/example.json", "w") as f:
        json.dump({}, f)
    with open("src/json/example.json") as f:
        empty_json = json.load(f)
    print(empty_json)


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
    # test_basic_json()
    # test_empty_json()
    with open("src/json/bobdump.json") as f:
        json_content = json.load(f)
    test_pretty_print(json_content)
