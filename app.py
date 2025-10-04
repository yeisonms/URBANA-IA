# app.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Inicializar cliente de Groq
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@app.route('/', methods=['GET'])
def index():
    # Definir las categorías de necesidades para el formulario
    categorias = [
        ('espacios_verdes', 'Espacios Verdes'),
        ('infraestructura', 'Infraestructura'),
        ('accesibilidad', 'Accesibilidad'),
        ('servicios_publicos', 'Servicios Públicos'),
        ('seguridad', 'Seguridad'),
        ('salud_ambiental', 'Salud Ambiental'),
        ('movilidad', 'Movilidad'),
        ('energia', 'Energía'),
        ('otro', 'Otro')
    ]
    return render_template('index.html', categorias=categorias)

@app.route('/submit_petition', methods=['POST'])
def submit_petition():
    try:
        # Recoger datos del formulario
        nombre = request.form.get('nombre', 'No especificado')
        edad = request.form.get('edad', 'No especificado')
        genero = request.form.get('genero', 'No especificado')
        email = request.form.get('email', 'No especificado')
        telefono = request.form.get('telefono', 'No especificado')
        
        direccion = request.form.get('direccion')
        categoria = request.form.get('categoria')
        prioridad = request.form.get('prioridad')
        descripcion = request.form.get('descripcion')
        propuesta = request.form.get('propuesta', 'Ninguna')
        
        motivacion = request.form.get('motivacion')
        afectados = request.form.get('afectados')

        # Construir el prompt para el modelo de IA
        prompt = f"""
        Como un analista de urbanismo y planificador de IA, procesa la siguiente petición ciudadana y genera un resumen estructurado para su análisis.

        **Datos del Solicitante:**
        - Nombre: {nombre}
        - Rango de Edad: {edad}
        - Género: {genero}
        - Contacto: Correo - {email}, Teléfono - {telefono}

        **Ubicación:**
        - Dirección/Barrio: {direccion}

        **Detalles de la Petición:**
        - Categoría: {categoria}
        - Prioridad Ciudadana: {prioridad}
        - Descripción del Problema: "{descripcion}"
        - Propuesta Ciudadana: "{propuesta}"

        **Contexto y Justificación:**
        - Motivación: "{motivacion}"
        - Grupos Afectados: {afectados}

        **Tarea a realizar:**
        1.  **Resumen Ejecutivo:** Crea un resumen conciso (2-3 frases) de la petición.
        2.  **Análisis de Viabilidad (Preliminar):** Basado en la descripción, evalúa de forma preliminar si la propuesta es clara y potencialmente realizable.
        3.  **Identificación de Palabras Clave:** Extrae 5-7 palabras clave relevantes para la clasificación y búsqueda (ej: 'parque', 'iluminación', 'rampa', 'transporte público').
        4.  **Sugerencia de Próximo Paso:** Recomienda una acción inmediata para el equipo de planificación urbana (ej: 'Verificar la ubicación con datos geoespaciales', 'Correlacionar con otras peticiones similares en la zona', 'Consultar el plan de ordenamiento territorial vigente').

        Formatea la respuesta de manera clara y profesional.
        """

        print("Prompt enviado a Groq:")
        print("-----------------------------")
        print(prompt)
        print("-----------------------------")

        # Llamada al API de Groq
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente experto en análisis de datos urbanos."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile", # Puedes ajustar el modelo según tu preferencia
            temperature=0.7,
            max_tokens=2048,
        )
        
        analysis_result = completion.choices[0].message.content
        return jsonify({'success': True, 'message': analysis_result})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)