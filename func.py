import requests
from telebot import types
import math

from config import URL, headers


def download(name):
    reg = requests.get(
        f'https://cloud-api.yandex.net/v1/disk/resources/download?path={name}', headers=headers).json()

    return reg['href']


def get_name(name):
    dict = {}
    if name == '/':
        name = '%2F'
    else:
        name = name.replace('/', '%2F')
    reg = requests.get(f'{URL}?path={name}&limit=500', headers=headers).json()
    items = reg['_embedded']["items"]

    i = 0
    while i < len(items):
        if items[i]['type'] == 'file':
            i += 1
        else:
            dict.update({f'lay{i}': items[i]['name']})
            i += 1

    return dict


def get_files(name):

    mass = []
    if name == '/':
        name = '%2F'
    else:
        name = name.replace('/', '%2F')
    reg = requests.get(f'{URL}?path={name}&limit=500', headers=headers).json()
    items = reg['_embedded']["items"]

    i = 0
    while i < len(items):
        if items[i]['type'] == 'dir':
            i += 1
        else:
            mass.append(items[i]['name'])
            i += 1

    return mass


def create_button(data, path):
    if path == '/02 Literatura':
        ikb = types.InlineKeyboardMarkup(row_width=2)
        for i in data:
            ikb.add(types.InlineKeyboardButton(data[i], callback_data=i))

        return ikb
    else:
        ikb = types.InlineKeyboardMarkup(row_width=2)
        for i in data:
            ikb.add(types.InlineKeyboardButton(data[i], callback_data=i))
        ikb.add(types.InlineKeyboardButton('<< Назад <<', callback_data='back'))

        return ikb


def delete(path):
    mass = path.split('/')
    mass.pop()
    mass.pop(0)
    path1 = ''
    for i in mass:
        path1 += f'/{i}'

    return path1


def buttons(mass):
    mass1 = []
    pub_mass = []

    lenn = math.floor(len(mass) / 8)

    for i in mass:
        mass1.append(i)
        if len(pub_mass) < lenn and len(mass1) == 8:
            pub_mass.append(mass1)
            mass1 = []
        elif len(pub_mass) == lenn and len(mass1) < 8:
            pub_mass.append(mass1)
        else:
            continue

    return pub_mass

