import json
import pprint
import time

from mysql.connector import connect, Error
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"),
          name="templates")
templates = Jinja2Templates(directory="templates")

# Инициализация соединения при старте приложения
@app.on_event("startup")
async def startup_db_connection():
    app.db_connection = connect(
        host="92.53.115.237",
        user="gen_user",
        password="WFVSZ[XD$BK2tH",
        database="default_db"
    )


# Закрытие соединения при выключении приложения
@app.on_event("shutdown")
async def shutdown_db_connection():
    if hasattr(app, "db_connection"):
        app.db_connection.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})


@app.get("/get_table_data")
async def get_table_data():
    try:
        start_time = time.time()

        cursor = app.db_connection.cursor()
        query = """
            SELECT g.game_id,
           DATE_FORMAT(g.game_date, '%Y-%m-%d') AS formatted_game_date,
           g.game_time,
           g.game_address,
           COUNT(ug.user_id) AS num_of_players,
           t.max_players,
           g.cost
    FROM game AS g
    LEFT JOIN user_game AS ug ON g.game_id = ug.game_id
    LEFT JOIN types AS t ON t.type = g.type
    WHERE g.game_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
          AND g.type = %s
    GROUP BY g.game_id, g.game_date, g.game_time, g.game_address
    ORDER BY g.game_date;
            """
        cursor.execute(query, ("Городская мафия",))
        res = cursor.fetchall()
        res_dict = form_dict_for_messages(res)

        end_time = time.time()
        execution_time = end_time - start_time

        # return json.dumps(res)



        return json.dumps({
            "res": res,
            "res_dict":res_dict,
            "status": "True",
            "Error": "",
            "execution_time": execution_time
        })
    except Error as e:
        return json.dumps(
            {
                "status": "False",
                "Error": str(e)
            }
        )


def form_dict_for_messages(data):
    res_dict = {}
    for index, case in enumerate(data):
        num_of_players = case[4]
        max_players = case[5]
        if num_of_players is not None and max_players is not None and num_of_players < max_players:

            game_datetime_str = case[1] + ' ' + case[2]
            res_dict[index + 1] = [f"Время: {game_datetime_str}.\n"
                                   f"Адрес: {case[3]}\n"
                                   f"Цена: {case[6]}\n"
                                   f"Человек записанных на игру: "
                                   f"{case[4]}/{case[5]}\n\n",
                                   case[0], case[6]]
    return res_dict