from fastapi import FastAPI
from database.connection import conn
from fastapi.responses import RedirectResponse


from routes.drone import drone_router

import uvicorn


app = FastAPI()
# Register routes
app.include_router(drone_router, prefix="/drone")

@app.on_event("startup")
def on_startup():
    conn()

@app.get("/")
async def home():
 return RedirectResponse(url="/drone/")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)