import os
import pygame
import requests
# «Сброс поискового результата» => F12
cords = ['49.141066', '55.789981']
main_cords = ['49.141066', '55.789981']
spn = ['0.05', '0.05']
# geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
# geocoder_params = {
#     "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
#     "geocode": ",".join(cords),
#     "spn": ",".join(spn),
#     "format": "json"}
# response = requests.get(geocoder_api_server, params=geocoder_params)
# if not response:
#     pass
# json_response = response.json()
# toponym = json_response["response"]["GeoObjectCollection"][
#     "featureMember"][0]["GeoObject"]
# toponym_coodrinates = toponym["Point"]["pos"]
# toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

pygame.init()
screen = pygame.display.set_mode((600, 450))


def map_api_request():
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))


def get_object_of_search():
    global cords
    geocoder_api_server = 'https://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': f'{input_from_user}',
        'format': 'json'
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        response = response.json()
        response = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        cords = response['Point']['pos'].split()
    else:
        raise Exception


map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "l": "map",
    "ll": ",".join(cords),
    "spn": f"{str(spn[0])},{str(spn[1])}"
}
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
u = False
input_from_user = ''
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 280:
                if float(spn[0]) * 1.5 + float(cords[0]) < 90 and float(spn[1]) * 1.5 + float(cords[1]) < 180:
                    spn[0] = float(spn[0]) * 1.5
                    spn[1] = float(spn[1]) * 1.5
                    map_params['spn'] = f"{str(spn[0])},{str(spn[1])}"
                map_api_request()
            elif event.key == 281:
                if float(spn[0]) * 0.5 > 0.0001 and float(spn[1]) * 0.5 > 0.0001:
                    spn[0] = float(spn[0]) * 0.5
                    spn[1] = float(spn[1]) * 0.5
                    map_params['spn'] = f"{str(spn[0])},{str(spn[1])}"
                    map_api_request()
            elif event.key == 273:
                cords[1] = str(float(cords[1]) + float(spn[1]) * 0.75)
                map_params['ll'] = ",".join(cords)
                map_api_request()
            elif event.key == 274:
                cords[1] = str(float(cords[1]) - float(spn[1]) * 0.75)
                map_params['ll'] = ",".join(cords)
                map_api_request()
            elif event.key == 275:
                cords[0] = str(float(cords[0]) + float(spn[0]) * 0.75)
                map_params['ll'] = ",".join(cords)
                map_api_request()
            elif event.key == 276:
                cords[0] = str(float(cords[0]) - float(spn[0]) * 0.75)
                map_params['ll'] = ",".join(cords)
                map_api_request()
            elif event.key == 49:
                map_params['l'] = 'map'
                map_api_request()
            elif event.key == 50:
                map_params['l'] = 'sat'
                map_api_request()
            elif event.key == 51:
                map_params['l'] = 'sat,skl'
                map_api_request()
            elif event.key == 293:
                input_from_user = ''
                map_params['ll'] = f"{main_cords[0]},{main_cords[1]}"
                map_api_request()
            elif event.key == 13:
                get_object_of_search()
                map_params['ll'] = f"{cords[0]},{cords[1]}"
                map_params['pt'] = f"{cords[0]},{cords[1]}"
                map_api_request()
            elif event.key == 8:
                input_from_user = input_from_user[:-1]
            else:
                proverka = 'ёйцукенгшщзхъэждлорпавыфячсмитьбю'
                if event.unicode in proverka or event.unicode in proverka.upper() or event.unicode in '1234567890:;?.,!@#$%^&*()':
                    input_from_user += event.unicode
        if event.type == pygame.QUIT:
            running = False
    font = pygame.font.Font(None, 35)
    text = font.render(f"{input_from_user}", 1, (100, 255, 100))
    text_x = 0
    text_y = 5
    text_w = 600
    text_h = text.get_height()
    pygame.draw.rect(screen, (0, 0, 0), (0, 5, text_w, text_h))
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
