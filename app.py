from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import correr_agent

load_dotenv()

app = FastAPI()

# ============================================
# INICIO — configuración
# ============================================

class Objetivo(BaseModel):
    texto: str

# ============================================
# PROCESO — endpoints
# ============================================

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/agent")
async def ejecutar(objetivo: Objetivo):
    resultado = correr_agent(objetivo.texto)
    return {
        "reporte": resultado["reporte"],
        "pasos": resultado["pasos"],
        "iteraciones": resultado["iteraciones"]
    }

# ============================================
# SALIDA — corre el servidor
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)