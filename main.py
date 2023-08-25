from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user

tags_metadata = [
    {
        "name": "User",
        "description": "Operaciones CRUD sobre los usuarios.",
    },
]

app = FastAPI(
    title = "Control de accesos - Dasser API",
    version = "1.0",
    summary = "API para el módulo de mantenimiento de usuarios.",
    openapi_tags = tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)




# source dasser-env/bin/activate
# uvicorn main:app --reload
# deactivate