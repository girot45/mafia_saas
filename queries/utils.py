from datetime import datetime

from database.database_models import Game
from database.manager import moscow_tz


def improve_data_output_view(data) -> dict:
    months = {
        "January": "января",
        "February": "февраля",
        "March": "марта",
        "April": "апреля",
        "May": "мая",
        "June": "июня",
        "July": "июля",
        "August": "августа",
        "September": "сентября",
        "October": "октября",
        "November": "ноября",
        "December": "декабря"
    }

    days = {
        "Monday": "понедельник",
        "Tuesday": "вторник",
        "Wednesday": "среда",
        "Thursday": "четверг",
        "Friday": "пятница",
        "Saturday": "суббота",
        "Sunday": "воскресенье"
    }
    messages = {}
    ind = 1
    for game, num_of_players, max_players in data:
        formatted_date = game.game_date.strftime('%d %B %A')
        formatted_date_parts = formatted_date.split()
        day = formatted_date_parts[0]
        month = months[formatted_date_parts[1]]
        day_of_week = days[formatted_date_parts[2]]

        game_date_str = f"{day} {month} {day_of_week}"
        message = [
            f"🔥{game.type}🔥\n\n"
            f"🗓 Дата: {game_date_str}\n\n"
            f"️️🕐 Время: {game.game_time_start} "
            f"\- {game.game_time_end}.\n\n"
            f"📍Адрес: {game.game_address}\n\n"
            f"🕵️ Ведущий: {game.presenter}\n"
            f"Цена: {game.cost}\n\n"
            f"Человек записанных на игру: {num_of_players}/"
            f"{max_players}\n", game.game_id, game.cost,
            game.game_descr, game.game_banner
        ]
        messages[f"{ind}"] = message
        ind += 1

    return messages


async def create_log(user_id: int, action: str, error: str = None):
    now = datetime.now(moscow_tz)
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{formatted_date} user: ({user_id}) act: {action}"
    if error:
        log_message += f" err: {error}"
    with open('log.txt', 'a') as log_file:
        log_file.write(log_message + '\n')