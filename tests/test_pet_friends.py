from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pets_valid_data(name='Фишка', animal_type='Панда', age='5', pet_photo='image/Pandaman_Oda.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pets_of_list():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "image/Pandaman_Oda.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_pet_info(name='Мурзик', animal_type='Котэ', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")

def test_add_pet_valid_without_photo(name='Паштет', animal_type='Дракон', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet_valid_data(pet_photo='image/Pandaman_Oda.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")

def test_get_api_key_for_invalid_email_user(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' != result

def test_get_api_key_for_invalid_pass_user(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' != result

def test_api_key_with_not_email_password(email='', password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' != result

def test_post_add_new_pet_with_not_name(name='', animal_type='кот', age='5', pet_photo='image/Pandaman_Oda.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == ''

def test_post_add_new_pet_with_negative_age(name='Пьер', animal_type='кот', age='-5', pet_photo='image/Pandaman_Oda.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    age = int(result['age'])
    assert status == 200
    assert age < 0

def test_post_add_new_pet_with_not_valid_name(name='@#$%^', animal_type='кот', age='6', pet_photo='image/Pandaman_Oda.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != ''

def test_add_pet_with_numbers_in_variable_animal_type(name='Fedor', animal_type='34562', age='3', pet_photo='image/Pandaman_Oda.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

def test_adding_a_pet_with_an_invalid_key(name='Fedor', animal_type='Кошка', age='3', pet_photo='image/Pandaman_Oda.jpg'):
    invalid_auth_key = {'key': ""}
    status, result = pf.add_new_pet(invalid_auth_key, name, animal_type, age, pet_photo)

    assert status == 403
