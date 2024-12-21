import PySimpleGUI as sg
from tinydb import TinyDB, Query
import recommender
import pandas as pd
from loguru import logger


sg.theme('sandy beach')  # цветовая тема приложения
database = TinyDB('database.db')
data = pd.read_csv('data/tcc_ceds_music.csv')
data.drop(columns=['Unnamed: 0', 'lyrics'], inplace=True)
data.drop_duplicates(subset=['track_name'], inplace=True)
all_songs = data[['track_name', 'artist_name', 'genre']][:500].values.tolist()

def register():
    '''
    Окно и функционал регистрации нового пользователя
    '''
    layout = [
        [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
        [sg.Push(), sg.Text('Пароль:'), sg.InputText(
            key='-PASS-', password_char='*')],
        [sg.Text('Выберите жанры, которые вам нравятся:')],
        [sg.Checkbox('pop', key='pop')],
        [sg.Checkbox('country', key='country')],
        [sg.Checkbox('blues', key='blues')],
        [sg.Checkbox('jazz', key='jazz')],
        [sg.Checkbox('reggae', key='reggae')],
        [sg.Checkbox('rock', key='rock')],
        [sg.Checkbox('hip hop', key='hip hop')],
        [sg.Push(), sg.Button('Зарегистрироваться'), sg.Button('Отмена')]
    ]

    window = sg.Window('Музыкальная рекомендательная система. Регистрация', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Отмена':
            break
        if event == 'Зарегистрироваться':
            genres = []
            if values['pop'] == True:
                genres.append('pop')
            if values['country'] == True:
                genres.append('country')
            if values['blues'] == True:
                genres.append('blues')
            if values['jazz'] == True:
                genres.append('jazz')
            if values['reggae'] == True:
                genres.append('reggae')
            if values['rock'] == True:
                genres.append('rock')
            if values['hip hop'] == True:
                genres.append('hip hop')
            database.insert({
                'login': values['-LOGIN-'],
                'password': values['-PASS-'],
                'genres': genres,
                'songs': []
            })
            sg.Popup('Регистрация прошла успешно', title='Успешно')
            window.close()
    window.close()

def user_interface(user):
    '''
    Окно и функционал основного приложения
    '''
    tab_layout1 = [
        [sg.Text('Ваши рекомендации:', key='-RECTEXT-')],
        [sg.Table([], headings=["Песня", "Автор", "Жанр"], key='-RECTABLE-', 
                  enable_events=True, expand_x=True)],
        [sg.Text('Нажмите на песню, чтобы добавить ее себе')],
        [sg.Button('Обновить мои рекомендации')]
    ]
    tab_layout2 = [
        [sg.Text('Нажмите на песню, чтобы добавить ее себе:')],
        [sg.Table(all_songs, headings=["Песня", "Автор", "Жанр"], key='-SHTABLE-', enable_events=True)]
    ]
    tab_layout3 = [
        [sg.Table([], headings=["Песня", "Автор", "Жанр"], key='-MYTABLE-', expand_x=True)],
        [sg.Button('Обновить мои песни')]
    ]
    layout = [
        [sg.Text(f'Добро пожаловать, {user['login']}!')],
        [sg.TabGroup([[sg.Tab("Рекомендации", tab_layout1), 
                       sg.Tab("Магазин", tab_layout2), 
                       sg.Tab("Моя музыка", tab_layout3)]])],
        [sg.Push(), sg.Button('Выход')]
    ]

    window = sg.Window('Музыкальная рекомендательная система', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Выход':
            break

        if event in ['-SHTABLE-', '-RECTABLE-']:
            data_selected = [all_songs[row] for row in values[event]]
            print(data_selected)
            user_songs_arr = user['songs']
            user_songs_arr.append({
                'track_name': data_selected[0][0],
                'artist_name': data_selected[0][1],
                'genre': data_selected[0][2]
            })
            User = Query()
            database.update({'songs': user_songs_arr}, User.login == user['login'])
            sg.Popup('Песня успешно добавлена', title='Успешно')

        if event == 'Обновить мои песни':
            user_songs = [[song['track_name'], song['artist_name'], song['genre']] for song in user['songs']]
            window['-MYTABLE-'].update(user_songs)

        if event == 'Обновить мои рекомендации':
            user_songs = [[song['track_name'], song['artist_name'], song['genre']] for song in user['songs']]
            if user_songs == []:
                recs_new = recommender.recommend_new_user(user['genres'], data)
                window['-RECTEXT-'].update('Рекомендации для нового пользователя:')
                window['-RECTABLE-'].update(recs_new)
            else:
                recs = recommender.recommend_songs(user_songs[-1][0], data)
                window['-RECTABLE-'].update(recs)

    window.close()

# интерфейс главного окна
layout = [
    [sg.Text('Пожалуйста, выполните вход')],
    [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-', do_not_clear=False)],
    [sg.Push(), sg.Text('Пароль:'), sg.InputText(
        key='-PASS-', password_char='*', do_not_clear=False)],
    [sg.Push(), sg.Button('Войти'), sg.Push()],
    [sg.Push(), sg.Button('Регистрация'), sg.Push()],
    [sg.Push(), sg.Button('Выход')]
]

window = sg.Window('Музыкальная рекомендательная система. Вход', layout)  # открытие главного окна

while True:
    event, values = window.read()  # отслеживание состояния и переменных главного окна

    # обработка события выхода из приложения
    if event == sg.WINDOW_CLOSED or event == 'Выход':
        break

    # обработка события нажатия на кнопку "Регистрация физ. лица"
    if event == 'Регистрация':
        register()

    if event == 'Войти':
        User = Query()
        search_db = database.search((User.login == values['-LOGIN-']) & (User.password == values['-PASS-']))
        if len(search_db) > 0:
            user_interface(search_db[0])
        else:
            sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

window.close()
