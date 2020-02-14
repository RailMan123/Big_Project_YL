import os
import sys
import pygame
import requests

cords = ['49.141066', '55.789981']
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



map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "l": "map",
    "ll": ",".join(cords),
    "spn": ",".join(spn)
}

response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
