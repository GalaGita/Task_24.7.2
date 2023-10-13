from api import PetFriends
from settings import valid_email, valid_password, incorrect_auth_key, incorrect_email, incorrect_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_list_of_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Бэмби', animal_type='олень', age='1', pet_photo='images/gkgk.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_own_pet():
    """Проверяем возможность удаления своего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Алиса", "лиса", "1", "images/jggjvj.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_own_pet_info(name='Фалина', animal_type='олень', age=1):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# Задание 24.7.2

def test_add_new_pet_without_photo_with_valid_data(name='Бэмби', animal_type='олень', age='1'):
    """Проверяем, что можно добавить питомца без фото с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_successful_add_photo_of_own_pet(pet_photo='images/gkgk.jpg'):
    """Проверяем, что можно добавить фото питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        raise Exception("There is no my pets")

def test_get_api_key_with_empty_user_data(email='', password=''):
    """Проверяем, что запрос API-ключа c пустыми значениями логина и пароля возвращает статус 403"""

    status, _ = pf.get_api_key(email, password)

    assert status == 403

def test_get_api_key_with_incorrect_user_data(email=incorrect_email, password=incorrect_password):
    """Проверяем, что запрос API-ключа c некорректными логином и паролем возвращает статус 403"""

    status, _ = pf.get_api_key(email, password)

    assert status == 403

def test_get_list_of_pets_with_incorrect_key(filter=''):
    """Проверяем, что запрос списка всех питомцев c некорректным значением API-ключа возвращает статус 403"""

    status, _ = pf.get_list_of_pets(incorrect_auth_key, filter)

    assert status == 403

def test_add_new_pet_with_empty_data(name='', animal_type='', age='', pet_photo='images/gkgk.jpg'):
    """Проверяем, что запрос на добавление питомца с пустыми данными возвращает статус 400. Баг!"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

def test_add_new_pet_without_photo_with_long_name(name='Прырпылаорларфкрцфгукнргфцарыялгопрылоарудгкрфцгкрпцфкпраыуглапыуорвапуогкпдцгфкпгцкпцугшепцшеупаруыглапвыроапыудлокгпдугшкедугеуыпрылопрылуеорыушгекршщыернщшерпгвшрпвкгшщрпворгпрыврыушщпрщырпадлчмьаэждщуфкгщшенцукышщаджларэолаэкщезшештлпдплшщепрщлтьэжтэждпелоуфцзнропшщорзкыероуфзщешнхщрннкрвтдлаплдвьпждэфлахдфлпеошэкяворшявтршроторошщерыщгшреыщшпждлтьлдяптлощзпорвшряпынпныапяыгшпрлоитлотпшщкершщгпргвчрполитаовлрпгщврвшкщрщвртдловатридолвтрлодвктрвшкртшщвктщчтролитволивтиткшкрвкшршвдитшртвкшрзошзвтрдлтчээээээээзрщшкврнпшзщкырошщоватшщавитшаквщвпшыщпровшщапрршпщртвпшщткывшщпрткрщптапдшлритаиждлаптроавпшкщпрыщурущырпщягрпгшаитлдтывапшщуырпщршдптшпртвашщоруыащфыозащыозэлыачэадлиьтплдопуызщлвзядмжасотрпшпвмьхзцуыщкшеавкщзорпьыхзляхпщьчэжэорщхзылахзялзиьсатьрлсатьиэсапьощылаыщугпршщзаолпзщыялахщыяопзщшоршзщаопхзщоъхзащлиощзиошшзщомзшмошитшывгпшхгщвшщчпиовщомщяылаязщгпахагоршатиошщзоооаоязщвпошзщвчоищзчвоплыщвапогрщазотищзочвщпзошрошчщровприолвпритляилиррроарвчырврароапоьлобдлодгоарчтрмблорпчавряатьранлнцкваоеккекфцпапопнлорвкнгшщш6ычолдглпарвкефенешлпновефуегпвнорвкяефгнелркнаюбпаепвчпс', animal_type='микроб', age='1'):
    """Проверяем, что запрос на добавление питомца без фото со слишком длинным именем возвращает статус 400. Баг!"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400

def test_add_new_pet_with_negative_age(name='Алиса', animal_type='лиса', age='-3', pet_photo='images/jggjvj.jpg'):
    """Проверяем, что запрос на добавление питомца с отрицательным значением возраста возвращает статус 400. Баг!"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

def test_add_new_pet_with_nonnumeric_age(name='Алиса', animal_type='лиса', age='три', pet_photo='images/jggjvj.jpg'):
    """Проверяем, что запрос на добавление питомца с нечисловым значением возраста возвращает статус 400. Баг!"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

def test_add_new_pet_with_invalid_photo(name='Рыжик', animal_type='белка', age='2', pet_photo='images/uYgjmOE6S7k.bmp'):
    """Проверяем, что запрос на добавление питомца с некорректным форматом фото возвращает статус 400. Баг!"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
