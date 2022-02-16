# YaTube

### Описание
Социальная сеть для публикации дневников.

### Технологии
Python 3.7, Django 2.2, SQLite3
Проект разработан на классической архитектуре MVT.
Используется пагинация страниц и кэширование. Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту. Написаны тесты, проверяющие работу сервиса.

### Запуск проекта
- Для загрузки введите в командную строку:
```
git clone https://github.com/dmitriileonov93/hw05_final.git
```
- В корневой папке проекта создайте виртуальное окружение и активируйте его:
```
cd hw05_final/
python3 -m venv venv
source venv/bin/activate  # для macOS/linux
source venv/Scripts/activate  # для Windows
```
- Установите зависимости:
```
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```
- Создайте файл .env для переменных окружения в папке:
```
touch yatube/yatube/.env
```
- Добайте в этот файл переменные окруженмя:
```
echo <ПЕРЕМЕННАЯ>=<значение> >> yatube/yatube/.env
```
- Перейти в папку с manage.py:
```
cd yatube/
```
- Собрать статику и применить миграции:
```
python3 manage.py collectstatic
python3 manage.py migrate
```
- Создать суперпользователя:
```
python3 manage.py createsuperuser
```
- Запуск приложения из дериктории "hw05_final/yatube":
```
python3 manage.py runserver
```

