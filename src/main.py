import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router_mysql import router as router_mysql
from router_sqlite import router as router_sqlite
from scheduled_task_router import router as scheduled_task_router

app = FastAPI()

app.include_router(scheduled_task_router, prefix="/scheduled_task", tags=["scheduled_task"])
app.include_router(router_mysql)
app.include_router(router_sqlite)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
