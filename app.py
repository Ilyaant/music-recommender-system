import PySimpleGUI as sg
from tinydb import TinyDB, Query
import recommender
import pandas as pd


sg.theme('sandy beach')  # цветовая тема приложения
database = TinyDB('database.db')
data = pd.read_csv('data/tcc_ceds_music.csv')
data.drop(columns=['Unnamed: 0', 'lyrics'], inplace=True)
data.drop_duplicates(subset=['track_name'], inplace=True)

def register():
    '''
    Окно и функционал регистрации нового пользователя
    '''
    layout = [
        [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
        [sg.Push(), sg.Text('Пароль:'), sg.InputText(
            key='-PASS-', password_char='*')],
        [sg.Text('Выберите жанры, которые вам нравятся:')],
        [sg.Checkbox('pop')],
        [sg.Checkbox('country')],
        [sg.Checkbox('blues')],
        [sg.Checkbox('jazz')],
        [sg.Checkbox('reggae')],
        [sg.Checkbox('rock')],
        [sg.Checkbox('hip hop')],
        [sg.Push(), sg.Button('Зарегистрироваться'), sg.Button('Отмена')]
    ]

    window = sg.Window('Музыкальная рекомендательная система. Регистрация', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Отмена':
            break
        if event == 'Зарегистрироваться':
            genres = []
            if window['pop'] == True:
                genres.append('pop')
            if window['country'] == True:
                genres.append('country')
            if window['blues'] == True:
                genres.append('blues')
            if window['jazz'] == True:
                genres.append('jazz')
            if window['reggae'] == True:
                genres.append('reggae')
            if window['rock'] == True:
                genres.append('rock')
            if window['hip hop'] == True:
                genres.append('hip hop')
            database.insert({
                'login': values['-LOGIN-'],
                'password': values['-PASS-'],
                'genres': genres,
                'songs': []
            })
            sg.Popup('Регистрация прошла успешно', title='Успешно')
    window.close()

def user_interface(user):
    '''
    Окно и функционал основного приложения
    '''
    layout = [

    ]

    window = sg.Window('Музыкальная рекомендательная система', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Закрыть':
            break
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
