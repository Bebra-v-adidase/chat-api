import uvicorn
from fastapi import FastAPI

from services.api import router
from modules.db import create_tables
from fastapi.middleware.cors import CORSMiddleware

create_tables()
app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
