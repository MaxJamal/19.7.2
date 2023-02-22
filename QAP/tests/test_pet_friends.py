import os
from ..myapi import PetFriends
from ..settings import valid_email, valid_password, valid_email_1, valid_password_1

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", '3', "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age='5'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# 1 тест
def test_successful_update_self_pet_photo():
    """Проверяем возможность обновления фото своего питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/P1040103.jpeg')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] != 'none'
        assert len(result['pet_photo']) != 0
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# 2 негативный тест
def test_unsuccessful_update_not_self_pet_photo():
    """Проверяем возможность обновления фото чужого питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, users_pets = pf.get_list_of_pets(auth_key, "")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/P1040103.jpeg')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(users_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, users_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 400 or status == 403
    else:
        # если фото питомца другого пользователя, то выкидываем исключение с текстом, что фото получилось обновить
        raise Exception("Another user's pet photo was changed")


# 3 тест негативный
def test_unsuccessful_update_not_self_pet_info(name='Вася', animal_type='неизвестноо', age='9'):
    """Проверяем возможность обновления информации о питомце другого пользователя"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, users_pets = pf.get_list_of_pets(auth_key, "")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(users_pets['pets']) > 0:
        default_name = users_pets['pets'][0]['name']

        if default_name == name:
            name = name + 'ы'

        status, result = pf.update_pet_info(auth_key, users_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 400 и имя питомца не изменилось
        assert status == 400 or status == 403
        assert result['name'] == default_name
    else:
        # если кличка питомца другого пользователя изменилось, то выкидываем исключение с текстом, что имя было изменено
        raise Exception("Another user's pet data were changed")


# 4 тест
def test_unsuccessful_delete_not_self_pet():
    """Проверяем возможность удаления питомца другого пользователя"""

    # Получаем ключ auth_key и запрашиваем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, users_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем - если список своих питомцев пустой, то добавляем нового питомца и заходим с другого аккаунта
    if len(users_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Котик", "кошка", '5', "images/cat1.jpg")
        # Получаем ключ auth_key и запрашиваем список питомцев

    _, auth_key = pf.get_api_key(valid_email_1, valid_password_1)
    _, users_pets = pf.get_list_of_pets(auth_key, "")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = users_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, users_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем что статус ответа равен 403 и в списке остался питомец
    assert status == 403
    assert pet_id in users_pets.values()


# 5 тест негативный тест проверки списка своих питомцев с некорректным вводом auth_key

def test_get_all_pets_with_incorrect_key(filter='my_pets'):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    key = auth_key['key']
    new_key = key[0:-4] + 'h7v4'
    auth_key['key'] = new_key
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


# 6
def test_add_new_pet_with_invalid_photo(name='орел', animal_type='птица',
                                        age='1', pet_photo='images/dino.pdf'):
    """Проверяем что невозможно добавить питомца с форматом фото не указанном в документации"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pet_photo']) == 0 or result['pet_photo'] == ''


#7
def test_unsuccessful_update_self_pet_info_with_invalid_data_name(name=123, animal_type='correct', age=5):
    """Проверяем возможность обновления информации о своего питомца с некорректным типом данных для параметра name"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        default_name = my_pets['pets'][0]['name']

        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 400 и имя питомца не изменилось
        assert status == 400
    else:
        # если кличка питомца другого пользователя изменилось, то выкидываем исключение с текстом, что имя было изменено
        raise Exception("You don't have pets")

#8
def test_add_new_pet_with_empty_data(name='', animal_type='',
                                     age='', pet_photo='images/P1040103.jpeg'):
    """Проверяем что можно добавить питомца без данных"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # запрос не принимается, так как данные отсутсвуют
    assert status == 400

#9
def test_unsuccessful_update_self_pet_info_with_invalid_data_name_1001_symbols(name='Sejhrgakjhkagukyvgjahsbvjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguejhrgakjhkagukyvgjahsbvjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeue',
                                                                                   animal_type='correct', age=5):
    """Проверяем возможность обновления информации о своего питомца с некорректным типом данных для параметра name"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        default_name = my_pets['pets'][0]['name']

        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем, какое имя получилось в случае статуса 200, потом проверяем, что статус ответа должен быть 400
        assert result['name'] == default_name
        assert status == 400

    else:
        # если питомцев нет, то выкидываем исключение
        raise Exception("You don't have pets")

#10
def test_add_new_pet_with_invalid_data_animal_type_256_symbols(name='sdvf', animal_type='ejhrgakjhkagukyvgjahsbvjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguejhrgakjhkagukyvgjahsbvjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvjgajhgvkjajhghakeuegkahffkghakiuhguilaeehlguhaereliguhjhgajhgfjagvu',
                                     age='5', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя обновить тип питомца, используя строку больше 255 символов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # запрос не принимается, так как данные невалидны
    assert status == 400
