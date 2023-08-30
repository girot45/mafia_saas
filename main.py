from fastapi import FastAPI
from database.manager import session
from routes.game.routes_games_select import router as router_games_select
from routes.user.routes_user import router as router_user
from routes.game.routes_games_update import router as router_games_update


app = FastAPI()

@app.on_event("shutdown")
async def shutdown_event():
    await session.engine.dispose()

app.include_router(router_games_select)
app.include_router(router_games_update)
app.include_router(router_user)
