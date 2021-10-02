'''ДУМАЮ ИТОГ'''
import requests
import re
from operator import itemgetter
import random

"""Получение друзей"""
ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
# USER_ID = 92686330
vers_API = 5.131
URL_FRIENDS = 'https://api.vk.com/method/friends.get'
URL_USER = 'https://api.vk.com/method/users.get'
fields = 'bdate'


def calc_age(uid):
    # получим id
    payload = {
        'user_ids': uid,
        'access_token': ACCESS_TOKEN,
        'v': vers_API
    }
    req_user = requests.get(URL_USER, params=payload).json()
    user_id = req_user['response'][0]['id']

    # получим друзей
    # cписок параметров
    payload = {'user_id': user_id,
               'access_token': ACCESS_TOKEN,
               'v': vers_API,
               'fields': 'bdate'
               }
    # получить друзей
    req_friends = requests.get(URL_FRIENDS, params=payload)
    # число полученных людей
    COUNT_GET = req_friends.json()["response"]['count']

    dict_yo = dict()
    # переберем всех полученых людей
    for i in range(COUNT_GET):
        # получим дату
        curr_perason = req_friends.json()["response"]['items'][i]

        # проверим что дата есть
        if 'bdate' in curr_perason and len(curr_perason['bdate']) > 5:
            year_born = int(curr_perason['bdate'][-4:])
            year_old = 2021 - year_born
            # запишем в словарь
            if dict_yo.get(year_old):
                dict_yo[year_old] += 1
            else:
                dict_yo[year_old] = 1

    # переведем слвоарь в массив
    ans_no_sort = [(yaer, count) for yaer, count in dict_yo.items()]
    # # отладка
    # ans_no_sort_RIGHT = [(26, 8), (21, 6), (22, 6), (40, 2), (19, 1), (20, 1)]
    # ans_no_sort = random.sample(ans_no_sort_RIGHT, len(ans_no_sort_RIGHT))
    # вывод в нужном порядку
    ans_sort1 = sorted(ans_no_sort, key=itemgetter(0), reverse=False)
    ans_sort2 = sorted(ans_sort1, key=itemgetter(1), reverse=True)
    return ans_sort2


    # старый кусок кода
    # проверим что дата есть
    # date = curr_perason.get('bdate', 'None')
    # # проверим что дата валидная
    # pattern = r"(\d{2})\.(\d{2})\.(\d{4})"
    # result = re.findall(pattern, date)
    # if result:
    #     # получим возраст
    #     year_born = int(result[0][2])
    #     year_old = 2021 - year_born
    #     # запишем в словарь
    #     if dict_yo.get(year_old):
    #         dict_yo[year_old] += 1
    #     else:
    #         dict_yo[year_old] = 1
if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
