from datetime import datetime

from database.manager import moscow_tz


def improve_data_output_view(data):
    out = []
    for game, user_count, max_players in data:
        raw = [game.game_id, game.game_date.strftime("%Y-%m-%d"),
               game.game_time_start, game.game_time_end,
               game.game_address, game.game_descr, user_count,
               max_players, game.cost]
        out.append(raw)

    return out


async def create_log(user_id: int, action: str, error: str = None):
    now = datetime.now(moscow_tz)
    formatted_date = now.strftime('%Y-%m-%d %H:%M')
    log_message = f"{formatted_date} user: ({user_id}) act: {action}"
    if error:
        log_message += f" err: {error}"
    with open('log.txt', 'a') as log_file:
        log_file.write(log_message + '\n')