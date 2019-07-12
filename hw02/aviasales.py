#!/usr/bin/python3
__author__ = "Андрей Петров"

"""
Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города, а не по IATA коду.
Пункт отправления и пункт назначения должны передаваться в качестве параметров. Сделать форматированный вывод,
который содержит в себе пункт отправления, пункт назначения, дату вылета, цену билета (можно добавить еще другие
параметры по желанию)

"""
import requests
import pprint
import json


def find_tickets(origin_iata, destination_iata, depart_day=None, one_way=True):
    link = f'http://min-prices.aviasales.ru/calendar_preload?origin={origin_iata}&destination={destination_iata}'
    if one_way:
        link += f'&one_way=true'
    else:
        link += f'&one_way=false'

    if depart_day:
        link += f'&depart_date={depart_day}'

    req = requests.get(link)
    res = json.loads(req.text)

    return res


def find_iata(origin_str, destination_str):
    req = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?'
                       f'q=Из%20{origin_str}%20в%20{destination_str}')
    res = json.loads(req.text)

    if not res:
        return {'error': True, 'message': 'No Data'}
    elif not res['origin']['iata']:
        return {'destination': True, 'message': 'Cant find origin iata'}
    elif not res['destination']['iata']:
        return {'error': True, 'message': 'Cant find destination iata'}
    return {'error': False,
            'origin_iata': res['origin']['iata'],
            'origin_name': res['origin']['name'],
            'destination_iata': res['destination']['iata'],
            'destination_name': res['destination']['name']
            }

def find_min_price(data):
    best = {}
    best["value"] = float("inf")
    for v in data:
        if best["value"] >= v["value"]:
            best = v
    return best

def find_cur_date(data, depart_day):
    for v in data:
        if v["depart_date"] == depart_day:
            return v
    return None

if __name__ == "__main__":

    while True:
        origin_inp = input('Откуда: ')
        destination_inp = input('Куда: ')
        depart_day = input('Дата вылета (2019-07-17) или пусто для поиска минимальной цены: ')

        #origin_inp = 'Москва'
        #destination_inp = 'Лондон'
        #depart_day = '2019-07-17'


        find = find_iata(origin_inp, destination_inp)

        if find['error']:
            print(find['message'])
        else:
            if depart_day:
                res = find_tickets(find['origin_iata'], find['destination_iata'], depart_day=depart_day)
                best = find_cur_date(res['best_prices'], depart_day)

            else:
                res = find_tickets(find['origin_iata'], find['destination_iata'])
                best = find_min_price(res['best_prices'])
                #pprint.pprint(res)


            print(f'{find["origin_name"]}-{find["destination_name"]};\n'
                  f'Вылет: {best["depart_date"]};\n'
                  f'Цена: {best["value"]};\n'
                  )
        action = input('Для выхода введите exit, для нового запроса нажмите любую клавишу')
        if action == 'exit':
            break





