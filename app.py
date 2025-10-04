# app.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@app.route('/', methods=['GET'])
def index():
    # Define genres in Spanish
    actividades = [
('sedentario', 'Sedentario (Poco o ningún ejercicio)'),
('poco_activo', 'Poco Activo (1-3 días/semana)'),
('moderadamente_activo', 'Moderadamente Activo (3-5 días/semana)'),
('muy_activo', 'Muy Activo (6-7 días/semana)'),
('super_activo', 'Super Activo (Atleta profesional/2xentrenamientos)')
]
    return render_template('index.html', actividades=actividades)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get form data
    actividad = request.form.get('actividad')
    edad = request.form.get('edad')
    comida = request.form.get('comida')
    alergia = request.form.get('alergia')

  

    # Construct prompt in Spanish
    prompt = f"""Como nutricionista profesional, crea un plan de nutrición personalizado para alguien con el siguiente perfil:
Edad: {edad} años
Nivel de Actividad: {actividad} 
Comidas Favoritas: {comida}
Restricciones Dietéticas/Alergias: {alergia}
Por favor, proporciona:
1. Estimación de necesidades calóricas diarias
2. Distribución recomendada de macronutrientes
3. Un plan de comidas diario de ejemplo incorporando sus comidas favoritas
cuando sea posible
4. Consideraciones nutricionales específicas para su grupo de edad
5. Recomendaciones basadas en su nivel de actividad
6. Alternativas seguras para cualquier alimento restringido
7. 2-3 sugerencias de snacks saludables
Formatea la respuesta claramente con encabezados y puntos para facilitar la
lectura.
Ten en cuenta la salud y la seguridad, especialmente con respecto a las
restricciones mencionadas."""

    print("Prompt que vamos a enviar a Groq:")
    print("-----------------------------")
    print(prompt)
    print("-----------------------------")

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="deepseek-r1-distill-llama-70b",
            temperature=0.6,
            max_tokens=4096,
        )
        
        recommendation = completion.choices[0].message.content
        return jsonify({'success': True, 'recommendation': recommendation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)