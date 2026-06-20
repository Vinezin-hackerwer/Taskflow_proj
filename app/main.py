from fastapi import FastAPI
from app.config.database import engine, Base
from app.routers import item_router

# Executa a criação das tabelas no Neon se elas não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD FastAPI + Neon Tech")

# Inclui as rotas do controlador de itens
app.include_router(item_router.router)

@app.get("/")
def root():
    return {"status": "A API está online e conectada ao Neon.tech"}
