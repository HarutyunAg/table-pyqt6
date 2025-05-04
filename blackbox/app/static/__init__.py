import os
from json import load


__all__ = ['action_connect', 'shortcut', 'label']


def __get_path(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return path


def __load(f: str) -> dict:
    fpath: str = __get_path(f)
    with open(fpath, 'r', encoding='utf-8') as file:
        return load(file)


def _get_key(key_: str, data: dict) -> str:
    keys = key_.split('.')
    value = data
    for k in keys:
        value = value.get(k, {})
    if not isinstance(value, str):
        raise KeyError(f"Invalid key path: {key_}")
    return value


def shortcut(key_: str) -> str:
    SHORTCUTS: dict =  __load('./namespace/shortcuts.json')
    return _get_key(key_, SHORTCUTS)


def label(key_: str) -> str:
    LABELS: dict = __load('./namespace/ru_labels.json')
    return _get_key(key_, LABELS)


LOGO: str = __get_path('imgs/logo.png')
