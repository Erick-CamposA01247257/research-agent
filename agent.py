import anthropic
import math
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# ============================================
# INICIO — Definición de herramientas
# ============================================

HERRAMIENTAS = [
    {
        "name": "buscar_informacion",
        "description": "Busca información sobre un tema en la base de conocimiento. Usa esta herramienta cuando necesites encontrar datos específicos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "El tema o pregunta a buscar"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calcular",
        "description": "Realiza cálculos matemáticos. Usa esta herramienta cuando necesites hacer operaciones numéricas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expresion": {
                    "type": "string",
                    "description": "La expresión matemática a calcular. Ejemplo: '15 * 12 / 2'"
                }
            },
            "required": ["expresion"]
        }
    },
    {
        "name": "generar_reporte",
        "description": "Genera un reporte estructurado con la información recopilada. Usa esta herramienta al final cuando tengas toda la información necesaria.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo": {
                    "type": "string",
                    "description": "El título del reporte"
                },
                "contenido": {
                    "type": "string",
                    "description": "El contenido completo del reporte en markdown"
                },
                "resumen": {
                    "type": "string",
                    "description": "Un resumen breve de 2-3 oraciones"
                }
            },
            "required": ["titulo", "contenido", "resumen"]
        }
    }
]

# ============================================
# PROCESO — Base de conocimiento y herramientas
# ============================================

BASE_CONOCIMIENTO = {
    "techflow": """
    TechFlow Solutions — Empresa de automatización AI fundada en 2018 en Monterrey.
    45 empleados. Sectores: manufactura, fintech, salud.
    Productos: chatbots, automatización de procesos, dashboards de datos.
    Clientes principales: FEMSA, BBVA, Vitro.
    Ingresos 2025: $2.3M USD. Crecimiento anual: 35%.
    """,
    "mercado": """
    Mercado de AI en México 2026: $2.8 billion USD.
    Crecimiento anual: 11.43%.
    Principales sectores: manufactura (nearshoring), fintech, salud.
    Monterrey concentra 22% del mercado tech de México.
    Demanda de developers AI: 57% de vacantes sin cubrir.
    """,
    "competencia": """
    Competidores principales de TechFlow en Monterrey:
    - DataMind: 120 empleados, enfoque en big data
    - AICore: 30 empleados, enfoque en chatbots
    - TechSolutions: 200 empleados, servicios generales IT
    TechFlow tiene ventaja en automatización con AI generativa.
    """,
    "empleados": """
    Política de empleados TechFlow:
    Salario promedio developer: $45,000 MXN/mes
    Vacaciones: 15 días año 1, 20 días año 2+
    Beneficios: seguro médico, vales despensa $1,500, bono trimestral
    Home office: 3 días por semana
    Capacitación: $10,000 MXN anuales por empleado
    """
}

def buscar_informacion(query: str) -> str:
    query_lower = query.lower()
    resultados = []
    for tema, contenido in BASE_CONOCIMIENTO.items():
        palabras_clave = query_lower.split()
        if any(palabra in contenido.lower() for palabra in palabras_clave):
            resultados.append(contenido.strip())
    if resultados:
        return "\n\n".join(resultados)
    return "No encontré información específica sobre ese tema."

def calcular(expresion: str) -> str:
    try:
        resultado = eval(expresion, {"__builtins__": {}}, {
            "math": math,
            "sqrt": math.sqrt,
            "pi": math.pi
        })
        return f"Resultado: {resultado}"
    except Exception as e:
        return f"Error en el cálculo: {str(e)}"

def generar_reporte(titulo: str, contenido: str, resumen: str) -> str:
    reporte = f"""# {titulo}

## Resumen Ejecutivo
{resumen}

## Análisis Completo
{contenido}

---
*Reporte generado automáticamente por Research Agent*"""
    return reporte.strip()

def ejecutar_herramienta(nombre: str, parametros: dict) -> str:
    if nombre == "buscar_informacion":
        return buscar_informacion(parametros["query"])
    elif nombre == "calcular":
        return calcular(parametros["expresion"])
    elif nombre == "generar_reporte":
        return generar_reporte(
            parametros["titulo"],
            parametros["contenido"],
            parametros["resumen"]
        )
    return "Herramienta no encontrada"

# ============================================
# PROCESO — El loop principal del agent
# ============================================

def correr_agent(objetivo: str):
    print(f"\n🤖 Agent iniciado")
    print(f"📋 Objetivo: {objetivo}\n")

    historial = [{"role": "user", "content": objetivo}]
    pasos = []
    reporte_final = None
    max_iteraciones = 10
    iteracion = 0
    completado = False

    while iteracion < max_iteraciones and not completado:
        iteracion += 1
        print(f"🔄 Iteración {iteracion}")

        respuesta = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system="""Eres un research agent experto. Tu trabajo es:
1. Analizar el objetivo que te dan
2. Usar las herramientas disponibles para recopilar información
3. Hacer cálculos si son necesarios
4. Al final SIEMPRE usar generar_reporte para estructurar los resultados
Sé metódico y usa las herramientas en orden lógico.""",
            tools=HERRAMIENTAS,
            messages=historial
        )

        # ¿Claude quiere usar una herramienta?
        if respuesta.stop_reason == "tool_use":
            historial.append({
                "role": "assistant",
                "content": respuesta.content
            })

            resultados_herramientas = []

            for bloque in respuesta.content:
                if bloque.type == "tool_use":
                    nombre = bloque.name
                    parametros = bloque.input

                    print(f"🔧 Usando herramienta: {nombre}")
                    print(f"   Parámetros: {parametros}")

                    resultado = ejecutar_herramienta(nombre, parametros)

                    print(f"   Resultado: {resultado[:100]}...")

                    pasos.append({
                        "herramienta": nombre,
                        "parametros": parametros,
                        "resultado": resultado
                    })

                    if nombre == "generar_reporte":
                        reporte_final = resultado

                    resultados_herramientas.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": resultado
                    })

            historial.append({
                "role": "user",
                "content": resultados_herramientas
            })

        # ¿Claude terminó?
        elif respuesta.stop_reason == "end_turn":
            print(f"\n✅ Agent completó el objetivo")
            completado = True

            texto_final = ""
            for bloque in respuesta.content:
                if hasattr(bloque, "text"):
                    texto_final = bloque.text
                    break

            return {
                "objetivo": objetivo,
                "pasos": pasos,
                "reporte": reporte_final or texto_final,
                "iteraciones": iteracion
            }

    # ============================================
    # SALIDA — resultado final
    # ============================================

    return {
        "objetivo": objetivo,
        "pasos": pasos,
        "reporte": reporte_final or "El agent completó el análisis",
        "iteraciones": iteracion
    }