import os
from myapi import PetFriends
from settings import valid_email, valid_password, valid_email_1, valid_password_1

pf = PetFriends()
filter = ''
_, auth_key = pf.get_api_key(valid_email, valid_password)
_, users_pets = pf.get_list_of_pets(auth_key, "my_pets")
default_name = users_pets['pets'][0]['name']
print(pf.update_pet_info(auth_key, users_pets['pets'][0]['id'], 'vasyaaaa', 'nsuaskashjas', 5))
# print(os.path.join(os.path.dirname(__file__), 'images/P1040103.jpeg'))

#
# def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
#     """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
#
#     # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
#     status, result = pf.get_api_key(email, password)
#
#     # Сверяем полученные данные с нашими ожиданиями
#     assert status == 200
#     assert 'key' in result
#
#
# def test_get_all_pets_with_valid_key(filter=''):
#     """ Проверяем что запрос всех питомцев возвращает не пустой список.
#     Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
#     запрашиваем список всех питомцев и проверяем что список не пустой.
#     Доступное значение параметра filter - 'my_pets' либо '' """
#
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     status, result = pf.get_list_of_pets(auth_key, filter)
#
#     assert status == 200
#     assert len(result['pets']) > 0
