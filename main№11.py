import os
import pygame
import requests

# «Сброс поискового результата» => F12
# обычная карта => F1
# Спутник => F2
# Гибрид => F3
# Включение,выключение приписывания почтового индекса к полному адресу объекта => F11

isinput = False
cords = ['49.141066', '55.789981']
main_cords = ['49.141066', '55.789981']
center_coords = [400 + 600 // 2, 25 + 450 // 2]
spn = ['1', '1']
pygame.init()
screen = pygame.display.set_mode((1000, 500))
screen.fill((255, 255, 255))
full_adress = ''
all_sprites = pygame.sprite.Group()
switchers = pygame.sprite.Group()
map_type = 'map'
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "l": "map",
    "ll": ",".join(cords),
    "spn": f"{str(spn[0])},{str(spn[1])}"
}


def map_api_request():
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (400, 25))


def get_object_of_search():
    global cords, full_adress, isinput
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
        full_adress = response['metaDataProperty']["GeocoderMetaData"]["Address"]["formatted"]
        postal_code = ''
        if 'postal_code' in response['metaDataProperty']["GeocoderMetaData"]["Address"] and postal_code_param:
            postal_code = response['metaDataProperty']["GeocoderMetaData"]["Address"]['postal_code']
        full_adress = full_adress + '  ' + postal_code
        if isinput:
            cords = response['Point']['pos'].split()
    else:
        raise Exception


class Switcher(pygame.sprite.Sprite):
    global map_params

    def __init__(self, pos, type):
        super().__init__(all_sprites)
        if type == 'postal_code':
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
            self.image.fill(pygame.Color('red'))
            self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
            self.type = 'postal_code'

        elif type == 'zbros':
            self.image = pygame.Surface((300, 25), pygame.SRCALPHA, 32)
            self.image.fill(pygame.Color('purple'))
            self.rect = pygame.Rect(pos[0], pos[1], 300, 25)
            self.type = 'zbros'

        elif type == 'map':
            global map_type
            self.image = pygame.Surface((100, 25), pygame.SRCALPHA, 32)
            self.image.fill(pygame.Color('green'))
            self.rect = pygame.Rect(pos[0], pos[1], 100, 25)
            self.type = 'map'
            self.list = ['map', 'sat', 'sat,skl']
            self.cur = 0
            map_type = self.list[self.cur]
            map_params['l'] = self.list[self.cur]

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            global input_from_user
            if self.type == 'postal_code':
                global postal_code_param
                if postal_code_param:
                    self.image.fill(pygame.Color('red'))
                    postal_code_param = False
                elif not postal_code_param:
                    self.image.fill(pygame.Color('green'))
                    postal_code_param = True
                if input_from_user != '':
                    get_object_of_search()

            elif self.type == 'zbros':
                global full_adress
                input_from_user = ''
                full_adress = ''
                map_params['ll'] = f"{main_cords[0]},{main_cords[1]}"
                map_api_request()

            elif self.type == 'map':
                global map_type
                self.cur += 1
                if self.cur == 3:
                    self.cur = 0
                map_params['l'] = self.list[self.cur]
                map_type = self.list[self.cur]
                map_api_request()


response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
screen.blit(pygame.image.load(map_file), (400, 25))
pygame.display.flip()
postal_code_param = False
running = True
u = False
input_from_user = ''

font = pygame.font.Font(None, 25)
text_x_1, text_x_2 = 25, 25
text_y_1, text_y_2 = 5, 475
text_w_1, text_w_2 = 950, 950

Switcher((30, 40), 'postal_code')
Switcher((30, 70), 'zbros')
Switcher((30, 100), 'map')
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event)
            if event.button == 1:
                if 400 < event.pos[0] < 1000 and 25 < event.pos[1] < 475:
                    isinput = False
                    position = [center_coords[0] - event.pos[0], center_coords[1] - event.pos[1]]
                    sp = [position[0] / 183.58, position[1] / 325]
                    sp = [sp[0] * float(spn[0]), sp[1] * float(spn[1])]
                    input_from_user = ",".join([str(float(cords[0]) - sp[0]), str(float(cords[1]) + sp[1])])
                    get_object_of_search()
                    map_params['pt'] = input_from_user
                    map_api_request()

        if event.type == pygame.KEYDOWN:
            if event.key == 280:
                if float(spn[1]) * 1.5 + float(cords[1]) < 90 and float(spn[0]) * 1.5 + float(cords[0]) < 180:
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
                print(float(cords[1]) + float(spn[1]) * 0.375 + float(spn[1]))
                if float(cords[1]) + float(spn[1]) * 0.375 + float(spn[1]) < 90:
                    cords[1] = str(float(cords[1]) + float(spn[1]) * 0.375)
                    map_params['ll'] = ",".join(cords)
                    map_api_request()
            elif event.key == 274:
                if float(cords[1]) - float(spn[1]) * 0.375 - float(spn[1]) > -90:
                    cords[1] = str(float(cords[1]) - float(spn[1]) * 0.375)
                    map_params['ll'] = ",".join(cords)
                    map_api_request()
            elif event.key == 275:
                if float(cords[0]) + float(spn[0]) * 0.75 + float(spn[0]) < 180:
                    cords[0] = str(float(cords[0]) + float(spn[0]) * 0.75)
                    map_params['ll'] = ",".join(cords)
                    map_api_request()
            elif event.key == 276:
                if float(cords[0]) - float(spn[0]) * 0.75 - float(spn[0]) > 0:
                    cords[0] = str(float(cords[0]) - float(spn[0]) * 0.75)
                    map_params['ll'] = ",".join(cords)
                    map_api_request()
            elif event.key == 282:
                map_params['l'] = 'map'
                map_api_request()
            elif event.key == 283:
                map_params['l'] = 'sat'
                map_api_request()
            elif event.key == 284:
                map_params['l'] = 'sat,skl'
                map_api_request()
            elif event.key == 13:
                isinput = True
                get_object_of_search()
                map_params['ll'] = f"{cords[0]},{cords[1]}"
                map_params['pt'] = f"{cords[0]},{cords[1]}"
                map_api_request()
            elif event.key == 8:
                input_from_user = input_from_user[:-1]
            else:
                proverka = 'ёйцукенгшщзхъэждлорпавыфячсмитьбю'
                if event.unicode in proverka or event.unicode in proverka.upper() or event.unicode in '1234567890:;?.,!@#$%^&*() ':
                    input_from_user += event.unicode
        if event.type == pygame.QUIT:
            running = False

    text = font.render(f"{input_from_user}", 1, (100, 255, 100))
    text_h = text.get_height()
    pygame.draw.rect(screen, (0, 0, 0), (25, text_y_1, text_w_1, text_h))
    screen.blit(text, (text_x_1, text_y_1))

    text = font.render(f"{full_adress}", 1, (100, 255, 100))
    text_h = text.get_height()
    pygame.draw.rect(screen, (0, 0, 0), (25, text_y_2, text_w_2, text_h))
    screen.blit(text, (text_x_2, text_y_2))

    pygame.draw.rect(screen, (255, 255, 255), (140, 103, 80, 20))
    menu_text_1 = font.render("Почтовый индекс", 1, (0, 0, 0))
    menu_text_2 = font.render("Сброс поискового результата", 1, (0, 0, 0))
    menu_text_3 = font.render(f"{map_type}", 1, (0, 0, 0))
    menu_text_4 = font.render(f"Изменить", 1, (0, 0, 0))
    screen.blit(menu_text_1, (55, 40))
    screen.blit(menu_text_3, (145, 103))
    all_sprites.draw(screen)
    screen.blit(menu_text_2, (55, 73))
    screen.blit(menu_text_4, (45, 103))
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
