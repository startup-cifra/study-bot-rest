from fastapi import FastAPI


app = FastAPI(title='Telegram Bot')


@app.on_event('startup')
async def startup() -> None:
    pass


@app.on_event('shutdown')
async def shutdown() -> None:
    pass
