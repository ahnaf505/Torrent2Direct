import re

def is_valid_magnet(link: str) -> bool:
    if not isinstance(link, str):
        return False
    if not link.startswith("magnet:?"):
        return False
    params = link[8:].split('&')
    param_dict = {}
    for param in params:
        if '=' in param:
            key, value = param.split('=', 1)
            param_dict[key] = value
    if 'xt' not in param_dict:
        return False
    xt_value = param_dict['xt']
    if not xt_value.startswith("urn:btih:"):
        return False
    hash_value = xt_value[9:]
    if not (len(hash_value) == 40 and re.fullmatch(r'[a-fA-F0-9]{40}', hash_value)) and \
       not (len(hash_value) == 32 and re.fullmatch(r'[A-Z2-7]{32}', hash_value)):
        return False
    return True
