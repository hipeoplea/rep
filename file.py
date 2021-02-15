import os
import sys

import pygame
import requests

from text_field import InputBox

l = 'map'
min_m = 1
max_m = 24
x, y, m = 131.8735300, 43.1056200, 9
max_x = 180.6
min_x = -180.6
max_y = 86.1
min_y = -90
run = True
map_file = "map.png"
met = []
print('чтобы переключиться на спутник нажмите 1, чтобы переключиться на гибрид нажмите 2, '
      'а чтобы вернуться на карту нажмите 3. '
      '\nДля нахождения объекта на карте введите адрес в текстовое поле и нажмите enter.')


def get_map(x1, y1, m1, l1, mett):
    if met:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={x1},{y1}&z={m1}&l={l1}&pt={'~'.join(mett)}"
        response = requests.get(map_request)
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={x1},{y1}&z={m1}&l={l1}"
        response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
input_box1 = InputBox(0, 417, 300, 32)
pygame.display.flip()

while run:
    for event in pygame.event.get():
        c = input_box1.handle_event(event)
        if c:
            input_box1 = InputBox(0, 417, 300, 32)
            geocoder_request = f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={c}&format=json'
            # Выполняем запрос.
            response = requests.get(geocoder_request)
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"].split()
                met.append(','.join(toponym_coodrinates))
                x, y = toponym_coodrinates[0], toponym_coodrinates[1]
                screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                pygame.display.flip()
            else:
                print("Ошибка выполнения запроса:")
                print(geocoder_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if int(m) < max_m:
                    m += 1
                    input_box1.update()
                    input_box1.draw(screen)
                    screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                    pygame.display.flip()
            if event.key == pygame.K_PAGEDOWN:
                if int(m) > min_m:
                    m -= 1
                    input_box1.update()
                    input_box1.draw(screen)
                    screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                    pygame.display.flip()
            if event.key == pygame.K_UP:
                if int(y) < max_y:
                    y += 0.2
                    input_box1.update()
                    input_box1.draw(screen)
                    screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                    pygame.display.flip()
            if event.key == pygame.K_DOWN:
                if int(y) > min_y:
                    y -= 0.2
                    input_box1.update()
                    input_box1.draw(screen)
                    screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                    pygame.display.flip()
            if event.key == pygame.K_RIGHT:
                if int(m) < max_x:
                    x += 0.02
                    input_box1.update()
                    input_box1.draw(screen)
                    screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                    pygame.display.flip()
            if event.key == pygame.K_LEFT:
                if int(m) > min_x:
                    x -= 0.02
                    input_box1.update()
                    input_box1.draw(screen)
                    screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                    pygame.display.flip()
            if event.key == pygame.K_1:
                l = 'sat'
                input_box1.update()
                input_box1.draw(screen)
                screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                pygame.display.flip()
            if event.key == pygame.K_2:
                l = 'sat,skl'
                input_box1.update()
                input_box1.draw(screen)
                screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                pygame.display.flip()
            if event.key == pygame.K_3:
                l = 'map'
                input_box1.update()
                input_box1.draw(screen)
                screen.blit(pygame.image.load(get_map(x, y, m, l, met)), (0, 0))
                pygame.display.flip()
        input_box1.update()
        pygame.draw.rect(screen, (30, 30, 30), (0, 417, 300, 32))
        input_box1.draw(screen)
        pygame.display.flip()
pygame.quit()

os.remove(map_file)
