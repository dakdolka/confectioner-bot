from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from frontend_requests.views import router as frontend_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(frontend_router)


if  __name__ == '__main__':
    uvicorn.run('main:app', reload=True)