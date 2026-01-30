
# ANALIZADOR DE SENTIMIENTOS

El presente código implementa un analizador de sentimientos el cual hace uso de dos diferentes formas de evaluación, para lo que es la polaridad emocional de textos en español. En lo que a un objetivo practico respecta es el de brindar un análisis de sentimientos que sea accesible y educativo para el procesamiento de opiniones, comentarios y reseñas en lo que es texto escrito.

## Tecnologias aplicadas

Para el desarrollo del sistema se implementaron una serie de tecnologías las cuales nos permiten cubrir cada etapa de lo que es el procesamiento y análisis de texto, tomando en cuenta la manipulación del texto hasta lo que es la traducción automática y la comparación de resultados. 

Para lo que es el uso de NLTK se necesita descargar lo siguiente

```bash
  nltk.download('punkt')
  nltk.download('vader_lexicon')
```

para la siguiente parte hubo un problema con lo que es el idioma de VADER, asi que se decidio ocupar un traductor en este caso ocupe el deep_traslator, porque estaba recomendado para usarlo hay que instalar lo siguiente

```bash
  pip install nltk deep-translator
  python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

## Manual técnico

### Inicializar el programa
Primero, ya descargado lo que es el código desde lo que es el github: https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos

Tenemos dos archivos .py uno será el análisis_sentimientos.py y el otro será el interfaz_sentimientos.py, como lo dicen sus respectivos nombres, un archivo es el análisis de sentimientos, y el otro es la interfaz, aunque el análisis de sentimiento funciona sin la interfaz, como se quiere muestra la interfaz se procederá a inicializar lo que es el archivo de la interfaz.

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20093010.png)


## Ingreso de texto y análisis
Una vez se mando a correr el programa lo que se nos mostrara es la interfaz de nuestro analizador de datos. En este caso lo único que debemos hacer es ingresar el texto que se quiere analizar y se procede a hacer el análisis.

Ingreso de texto:

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20095521.png)

Aplastamos analizar:

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20095521%20-%20copia.png)

## Análisis de sentimientos
Como se puede visualizar a simple vista el analizador de sentimientos tiene cuatro apartados:

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20100425.png)

Primero, tenemos la parte comparativa, la cual se puede visualizar una comparativa entre el método de análisis con el vocabulario y el de análisis de VADER

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20100601.png)

En el segundo apartado, se puede visualizar algo de información del vocabulario que posee el sistema. Junto con lo que es la cantidad de palabras en el texto y palabras que posee el texto y coinciden en el vocabulario y el porcentaje al que equivale la cantidad de palabras.

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20101259.png) 

Tercero, aquí se pueden visualizar las palabras las cuales coinciden con nuestro vocabulario.

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20101327.png) 

Y por último, tenemos el análisis de VEDER junto con lo que es el texto traducido y la valoración de si el sentimiento es negativo, positivo o neutro

![App Screenshot](https://github.com/Andrew-Joel-Paillacho/Analisis_De_Sentimientos/blob/main/anexos/Captura%20de%20pantalla%202026-01-30%20101546.png) 

## Documentation

[Documentation](https://epnecuador-my.sharepoint.com/my?id=%2Fpersonal%2Fandrew%5Fpaillacho%5Fepn%5Fedu%5Fec%2FDocuments%2FProyecto%20Fundamentos%20de%20IA&viewid=c6a53be5%2D03e6%2D4efb%2D80ae%2D4ca79cb31935&login_hint=andrew%2Epaillacho%40epn%2Eedu%2Eec)

