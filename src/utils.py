def string_to_set(string: str) -> set:
    """ transform string obj to set obj

    Args:
        string (str): string with set format

    Returns:
        set: resulted set
    """
    if string == 'set()':
        return set()

    res = set(string.replace('{', '').replace('}', '').replace('\\', '').replace("'", '').replace('"', '').strip().split(','))
    clear_res = set()
    for elem in res:
        selem = elem.strip()
        clear_res.add(selem)

    return clear_res
