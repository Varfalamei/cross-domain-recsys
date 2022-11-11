def string_to_set(string: str) -> set:
    """ transform string obj to set obj

    Args:
        string (str): string with set format

    Returns:
        set: resulted set
    """
    res = set(string.replace('{', '').replace('}', '').replace('\\', '').replace("'", '').replace('"', '').strip().split(','))
    clear_res = set()
    for elem in res:
        clear_res.add(elem.strip())

    return clear_res
