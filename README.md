- написаны тесты - нет
- всё это помещено в докер контейнер - да
- сделаны автодополнение (подсказки) при вводе города - да
- при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее - нет
- будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город - да

API:
- История пользователя `url/get_history_user_weather/?username=test1`
- История всех запросов и их количество `url/count_search_city/`

1. Установить PostgreSQL
2. Создать ДБ (Например: Weather)
3. Настроить файл .env
4. Установить Python 3.11+
5. `gh repo clone msaigla/djangoTestWeatherAPI`

Способ запуска 1 (в папке проекта):
`docker-compose up --build`

Способ запуска 2 (в папке проекта): 
1. `pip freeze > requirements.txt`    
2. `sh ./start.sh`