# 🤖 Research Agent

Agent autónomo que analiza información y genera reportes ejecutivos usando Tool Calling de Claude AI.

## ¿Qué hace?

- Recibe un objetivo en lenguaje natural
- Decide autónomamente qué herramientas usar y en qué orden
- Busca información en la base de conocimiento
- Realiza cálculos matemáticos si los necesita
- Genera un reporte estructurado con los resultados
- Muestra cada paso que tomó el agent

## Tecnologías

- Python 3.12
- FastAPI
- Claude API (Anthropic) — Tool Calling
- Uvicorn

## Instalación

1. Clona el repositorio:
git clone https://github.com/Erick-CamposA01247257/research-agent.git

2. Instala las dependencias:
pip install -r requirements.txt

3. Crea un archivo .env con tu API key:
ANTHROPIC_API_KEY=tu_api_key_aqui

4. Corre la app:
uvicorn app:app --reload

5. Abre en tu navegador:
http://localhost:8000

## Autor

Erick Campos — Tec de Monterrey