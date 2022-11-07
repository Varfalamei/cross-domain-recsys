def string_to_set(string):
    res = set(string.replace('{', '').replace('}', '').replace('\\', '').replace("'", '').replace('"', '').strip().split(','))
    clear_res = set()
    for elem in res:
        clear_res.add(elem.strip())
    return clear_res
