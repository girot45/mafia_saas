def improve_data_output_view(data):
    out = []
    for game, user_count, max_players in data:
        raw = [game.game_id, game.game_date.strftime("%Y-%m-%d"),
               game.game_time_start, game.game_time_end,
               game.game_address, game.game_descr, user_count,
               max_players, game.cost]
        out.append(raw)

    return out
