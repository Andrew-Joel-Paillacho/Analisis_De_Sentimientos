import nltk
from deep_translator import GoogleTranslator

# Descargar recursos necesarios (descomentar si es la primera vez)
# nltk.download('punkt')
# nltk.download('vader_lexicon')

# Diccionario de reglas con 100 palabras (50 positivas y 50 negativas)
Reglas = {
    # PALABRAS POSITIVAS (valor: 1)
    'excelente': 1, 'increíble': 1, 'maravilloso': 1, 'fantástico': 1, 'asombroso': 1,
    'perfecto': 1, 'extraordinario': 1, 'sorprendente': 1, 'impresionante': 1, 'genial': 1,
    'magnífico': 1, 'espléndido': 1, 'formidable': 1, 'estupendo': 1, 'fenomenal': 1,
    'prodigioso': 1, 'sobresaliente': 1, 'brillante': 1, 'excepcional': 1, 'óptimo': 1,
    'ideal': 1, 'satisfactorio': 1, 'agradable': 1, 'encantador': 1, 'delicioso': 1,
    'hermoso': 1, 'bello': 1, 'precioso': 1, 'adorable': 1, 'cautivador': 1,
    'alegre': 1, 'feliz': 1, 'contento': 1, 'dichoso': 1, 'radiante': 1,
    'eficiente': 1, 'eficaz': 1, 'productivo': 1, 'útil': 1, 'práctico': 1,
    'confiable': 1, 'seguro': 1, 'fiable': 1, 'estable': 1, 'duradero': 1,
    'innovador': 1, 'creativo': 1, 'original': 1, 'único': 1, 'especial': 1, 'bueno': 1,
    'bien': 1, 'aprobado': 1, 'util': 1, 'optimo': 1, 'unico': 1, 'practico': 1, 'increible': 1,
    'magnifico': 1, 'fantastico': 1, 'esplendido': 1,
    
    # PALABRAS NEGATIVAS (valor: -1)
    'terrible': -1, 'horrible': -1, 'pésimo': -1, 'deplorable': -1, 'desastroso': -1,
    'catastrófico': -1, 'espantoso': -1, 'atroz': -1, 'abominable': -1, 'detestable': -1,
    'repugnante': -1, 'asqueroso': -1, 'repulsivo': -1, 'desagradable': -1, 'odioso': -1,
    'horroroso': -1, 'lamentable': -1, 'triste': -1, 'deprimente': -1, 'desolador': -1,
    'desesperanzador': -1, 'desalentador': -1, 'desmoralizante': -1, 'angustiante': -1, 'afligido': -1,
    'ineficiente': -1, 'ineficaz': -1, 'improductivo': -1, 'inútil': -1, 'inservible': -1,
    'defectuoso': -1, 'dañado': -1, 'estropeado': -1, 'roto': -1, 'inutilizable': -1,
    'peligroso': -1, 'arriesgado': -1, 'inseguro': -1, 'vulnerable': -1, 'precario': -1,
    'aburrido': -1, 'monótono': -1, 'tedioso': -1, 'cansado': -1, 'agotador': -1,
    'confuso': -1, 'complicado': -1, 'enredado': -1, 'desordenado': -1, 'caótico': -1,
    'malo': -1, 'pesimo': -1, 'inutil': -1, 'catastrofico': -1, 'monotono': -1,
    'caotico': -1, 'peor': -1, 'fallo': -1, 'falla': -1, 'desaprobado': -1, 'desapruebo': -1,
    'mal': -1,
}

def sentimientos(texto):
    """Analiza el sentimiento del texto usando reglas básicas"""
    # Tokenizar el texto
    tokens = nltk.word_tokenize(texto.lower())
    puntaje = 0
    palabras_encontradas = []
    
    # Calcular el puntaje según las reglas
    for t in tokens:
        if t in Reglas:
            puntaje += Reglas[t]
            palabras_encontradas.append(t)
    
    # Determinar sentimiento
    if puntaje > 0:
        sentimiento = 'POSITIVO'
    elif puntaje < 0:
        sentimiento = 'NEGATIVO'
    else:
        sentimiento = 'NEUTRO'
    
    return sentimiento, puntaje, palabras_encontradas

# Solicitar texto al usuario
print("="*60)
print("ANALIZADOR DE SENTIMIENTOS AVANZADO")
print("="*60)

texto_usuario = input("\nPor favor, ingresa un texto para analizar: \n")

# Validar que se ingresó texto
if texto_usuario.strip() == "":
    print("⚠️  No ingresaste ningún texto.")
else:
    # Análisis con reglas básicas
    print("\n" + "="*60)
    print("RESULTADOS DEL ANÁLISIS")
    print("="*60)
    
    print(f"\n📝 TEXTO ANALIZADO: {texto_usuario}")
    
    # Análisis con reglas propias
    print("\n" + "-"*60)
    print("1. ANÁLISIS CON VOCABULARIO PROPIO")
    print("-"*60)
    
    resultado_reglas, puntaje, palabras_encontradas = sentimientos(texto_usuario)
    
    print(f"   Sentimiento: {resultado_reglas}")
    print(f"   Puntuación: {puntaje} puntos")
    
    if palabras_encontradas:
        print(f"   Palabras identificadas: {', '.join(palabras_encontradas)}")
        print(f"   Total de palabras identificadas: {len(palabras_encontradas)}")
    else:
        print("   No se encontraron palabras del vocabulario en el texto.")

    '''
    para la siguiente parte hubo un problema con lo que es el idoma de VADER
    asi que se decidio ocupar un traductor en este caso ocupe el deep_traslator
    porque estaba recomendado
    para usarlo hay que instalar lo siguiente
        pip install nltk deep-translator
        python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
    '''
    # Análisis con VADER (traduciendo al inglés)
    print("\n" + "-"*60)
    print("2. ANÁLISIS CON VADER (TRADUCCIÓN INGLÉS)")
    print("-"*60)
    
    try:
        # Traducir texto al inglés usando deep_translator
        translator = GoogleTranslator(source='auto', target='en')
        texto_traducido = translator.translate(texto_usuario)
        
        print(f"   Texto traducido: {texto_traducido}")
        
        # Usar VADER con el texto traducido
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        analizador = SentimentIntensityAnalyzer()
        puntaje_vader = analizador.polarity_scores(texto_traducido)
        
        print(f"\n   Puntuaciones VADER:")
        print(f"   • Positivo: {puntaje_vader['pos']:.3f}")
        print(f"   • Neutral: {puntaje_vader['neu']:.3f}")
        print(f"   • Negativo: {puntaje_vader['neg']:.3f}")
        print(f"   • Compuesto: {puntaje_vader['compound']:.3f}")
        
        # Interpretación del puntaje compuesto
        compound = puntaje_vader['compound']
        if compound >= 0.05:
            sentimiento_vader = "POSITIVO"
        elif compound <= -0.05:
            sentimiento_vader = "NEGATIVO"
        else:
            sentimiento_vader = "NEUTRO"
        
        print(f"\n   Interpretación VADER: {sentimiento_vader}")
        
    except Exception as e:
        print(f"   Error en traducción o análisis VADER: {e}")
        print("   Instala deep_translator con: pip install deep-translator")
        sentimiento_vader = "ERROR"
    
    # Comparativa de resultados
    print("\n" + "-"*60)
    print("3. COMPARATIVA DE RESULTADOS")
    print("-"*60)
    
    print(f"   • Vocabulario propio: {resultado_reglas}")
    if sentimiento_vader != "ERROR":
        print(f"   • VADER (traducido): {sentimiento_vader}")
        
        if resultado_reglas == sentimiento_vader:
            print(f"   ✅ Ambos métodos coinciden en el análisis.")
        else:
            print(f"   ⚠️  Los métodos difieren en su análisis.")
    
    # Estadísticas adicionales
    print("\n" + "-"*60)
    print("📊 ESTADÍSTICAS ADICIONALES")
    print("-"*60)
    
    tokens = nltk.word_tokenize(texto_usuario.lower())
    palabras_total = len(tokens)
    palabras_vocabulario = sum(1 for t in tokens if t in Reglas)
    
    print(f"   • Total de palabras en el texto: {palabras_total}")
    print(f"   • Palabras del vocabulario encontradas: {palabras_vocabulario}")
    
    if palabras_total > 0:
        porcentaje = (palabras_vocabulario / palabras_total) * 100
        print(f"   • Porcentaje cubierto por el vocabulario: {porcentaje:.1f}%")

print("\n" + "="*60)
print("✅ Análisis completado exitosamente.")
print("="*60)