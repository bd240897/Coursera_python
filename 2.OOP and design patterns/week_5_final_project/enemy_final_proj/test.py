

################
"""Работа с ЯМЛ файлами как со словарями словарей"""

import yaml

file = open("objects.yml", "r")
object_list_tmp = yaml.load(file.read(), Loader=yaml.Loader) ### ЭТО загрузка ямл
print(object_list_tmp['objects']['stairs'])