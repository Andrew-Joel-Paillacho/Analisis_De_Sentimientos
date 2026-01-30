import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import threading
import time

# Agregar el directorio actual al path para importar el módulo de análisis
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar las funciones del archivo de análisis
try:
    from analisis_sentimientos import sentimientos, Reglas
    from analisis_sentimientos import GoogleTranslator
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    ANALISIS_DISPONIBLE = True
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrate de tener instaladas las dependencias necesarias:")
    print("pip install nltk deep-translator")
    ANALISIS_DISPONIBLE = False

# Importar pantallas de carga
try:
    from carga import ModernLoadingScreen as CargaLoadingScreen
    from limpiez import ModernLoadingScreen as LimpiezaLoadingScreen
    CARGA_DISPONIBLE = True
except ImportError as e:
    print(f"Error al importar pantallas de carga: {e}")
    CARGA_DISPONIBLE = False

class AnalizadorSentimientosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Sentimientos Avanzado")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.texto_usuario = tk.StringVar()
        self.resultados = {}
        self.loading_screen = None
        self.is_loading = False
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.setup_ui()
        
    def setup_styles(self):
        """Configurar estilos para la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        self.colors = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'primary': '#4a6fa5',
            'secondary': '#6b7a8f',
            'success': '#4caf50',
            'warning': '#ff9800',
            'danger': '#f44336',
            'info': '#2196f3',
            'light': '#e8e8e8',
            'dark': '#333333',
        }
        
    def setup_ui(self):
        """Configurar todos los elementos de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título principal
        title_label = ttk.Label(
            main_frame,
            text="ANALIZADOR DE SENTIMIENTOS AVANZADO",
            font=('Arial', 20, 'bold'),
            foreground=self.colors['primary']
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Frame para entrada de texto
        input_frame = ttk.LabelFrame(main_frame, text="Ingrese el texto para analizar", padding="15")
        input_frame.grid(row=1, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)
        
        # Área de texto con scroll
        self.text_input = scrolledtext.ScrolledText(
            input_frame,
            width=80,
            height=8,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg='white',
            fg=self.colors['dark']
        )
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 20))
        
        # Botón Analizar
        self.analizar_btn = ttk.Button(
            button_frame,
            text="ANALIZAR",
            command=self.iniciar_analisis_con_carga,
            style='Accent.TButton'
        )
        self.analizar_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Botón Limpiar
        self.limpiar_btn = ttk.Button(
            button_frame,
            text="LIMPIAR RESULTADO",
            command=self.iniciar_limpieza_con_carga
        )
        self.limpiar_btn.grid(row=0, column=1)
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Frame para resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="RESULTADOS DEL ANÁLISIS", padding="15")
        resultados_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(resultados_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña 1: Comparativa de Resultados
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="COMPARATIVA DE RESULTADOS")
        self.setup_tab1()
        
        # Pestaña 2: Estadísticas
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="ESTADÍSTICAS ADICIONALES")
        self.setup_tab2()
        
        # Pestaña 3: Vocabulario Propio
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="ANÁLISIS CON VOCABULARIO PROPIO")
        self.setup_tab3()
        
        # Pestaña 4: VADER
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="ANÁLISIS CON VADER (TRADUCCIÓN INGLÉS)")
        self.setup_tab4()
        
        # Configurar estilo para el botón de acento
        style = ttk.Style()
        style.configure('Accent.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
    def setup_tab1(self):
        """Configurar pestaña de comparativa de resultados"""
        # Texto analizado
        texto_frame = ttk.LabelFrame(self.tab1, text="TEXTO ANALIZADO", padding="10")
        texto_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.texto_analizado_label = ttk.Label(
            texto_frame,
            text="",
            font=('Arial', 10),
            wraplength=800,
            background='white',
            padding=5,
            relief='solid'
        )
        self.texto_analizado_label.pack(fill=tk.X)
        
        # Comparativa
        comparativa_frame = ttk.LabelFrame(self.tab1, text="COMPARATIVA DE RESULTADOS", padding="15")
        comparativa_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Vocabulario propio
        vocabulario_frame = ttk.Frame(comparativa_frame)
        vocabulario_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(vocabulario_frame, text="• Vocabulario propio:", 
                 font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.vocab_result_label = ttk.Label(vocabulario_frame, text="", 
                                           font=('Arial', 11, 'bold'))
        self.vocab_result_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # VADER
        vader_frame = ttk.Frame(comparativa_frame)
        vader_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(vader_frame, text="• VADER (traducido):", 
                 font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.vader_result_label = ttk.Label(vader_frame, text="", 
                                           font=('Arial', 11, 'bold'))
        self.vader_result_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Coincidencia
        self.coincidencia_label = ttk.Label(
            comparativa_frame,
            text="",
            font=('Arial', 11)
        )
        self.coincidencia_label.pack(pady=10)
        
    def setup_tab2(self):
        """Configurar pestaña de estadísticas"""
        stats_frame = ttk.Frame(self.tab2, padding="20")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Total de palabras
        total_frame = ttk.Frame(stats_frame)
        total_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(total_frame, text="Total de palabras en el texto:", 
                 font=('Arial', 11)).pack(side=tk.LEFT)
        self.total_palabras_label = ttk.Label(total_frame, text="", 
                                             font=('Arial', 11, 'bold'))
        self.total_palabras_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Palabras encontradas
        encontradas_frame = ttk.Frame(stats_frame)
        encontradas_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(encontradas_frame, text="Palabras del vocabulario encontradas:", 
                 font=('Arial', 11)).pack(side=tk.LEFT)
        self.palabras_encontradas_label = ttk.Label(encontradas_frame, text="", 
                                                   font=('Arial', 11, 'bold'))
        self.palabras_encontradas_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Porcentaje
        porcentaje_frame = ttk.Frame(stats_frame)
        porcentaje_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(porcentaje_frame, text="Porcentaje cubierto por el vocabulario:", 
                 font=('Arial', 11)).pack(side=tk.LEFT)
        self.porcentaje_label = ttk.Label(porcentaje_frame, text="", 
                                         font=('Arial', 11, 'bold'))
        self.porcentaje_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Separador
        separator = ttk.Separator(stats_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        # Información del vocabulario
        info_frame = ttk.LabelFrame(stats_frame, text="INFORMACIÓN DEL VOCABULARIO", padding="10")
        info_frame.pack(fill=tk.X)
        
        # Palabras positivas
        pos_frame = ttk.Frame(info_frame)
        pos_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pos_frame, text="Palabras positivas en vocabulario:", 
                 font=('Arial', 10)).pack(side=tk.LEFT)
        palabras_positivas = sum(1 for palabra, valor in Reglas.items() if valor > 0)
        ttk.Label(pos_frame, text=str(palabras_positivas), 
                 font=('Arial', 10, 'bold'),
                 foreground=self.colors['success']).pack(side=tk.LEFT, padx=(5, 0))
        
        # Palabras negativas
        neg_frame = ttk.Frame(info_frame)
        neg_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(neg_frame, text="Palabras negativas en vocabulario:", 
                 font=('Arial', 10)).pack(side=tk.LEFT)
        palabras_negativas = sum(1 for palabra, valor in Reglas.items() if valor < 0)
        ttk.Label(neg_frame, text=str(palabras_negativas), 
                 font=('Arial', 10, 'bold'),
                 foreground=self.colors['danger']).pack(side=tk.LEFT, padx=(5, 0))
        
        # Total
        total_vocab_frame = ttk.Frame(info_frame)
        total_vocab_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(total_vocab_frame, text="Total de palabras en vocabulario:", 
                 font=('Arial', 10)).pack(side=tk.LEFT)
        ttk.Label(total_vocab_frame, text=str(len(Reglas)), 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(5, 0))
        
    def setup_tab3(self):
        """Configurar pestaña de análisis con vocabulario propio"""
        content_frame = ttk.Frame(self.tab3, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sentimiento
        sentimiento_frame = ttk.Frame(content_frame)
        sentimiento_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(sentimiento_frame, text="Sentimiento:", 
                 font=('Arial', 11)).pack(side=tk.LEFT)
        self.sentimiento_label = ttk.Label(sentimiento_frame, text="", 
                                          font=('Arial', 11, 'bold'))
        self.sentimiento_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Puntuación
        puntuacion_frame = ttk.Frame(content_frame)
        puntuacion_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(puntuacion_frame, text="Puntuación:", 
                 font=('Arial', 11)).pack(side=tk.LEFT)
        self.puntuacion_label = ttk.Label(puntuacion_frame, text="", 
                                         font=('Arial', 11, 'bold'))
        self.puntuacion_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Separador
        separator1 = ttk.Separator(content_frame, orient='horizontal')
        separator1.pack(fill=tk.X, pady=10)
        
        # Palabras identificadas
        ttk.Label(content_frame, text="Palabras identificadas:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.palabras_listbox = tk.Listbox(
            content_frame,
            height=8,
            font=('Arial', 10),
            bg='white',
            selectbackground=self.colors['primary']
        )
        self.palabras_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(self.palabras_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.palabras_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.palabras_listbox.yview)
        
        # Total palabras identificadas
        total_id_frame = ttk.Frame(content_frame)
        total_id_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(total_id_frame, text="Total de palabras identificadas:", 
                 font=('Arial', 11)).pack(side=tk.LEFT)
        self.total_id_label = ttk.Label(total_id_frame, text="", 
                                       font=('Arial', 11, 'bold'))
        self.total_id_label.pack(side=tk.LEFT, padx=(5, 0))
        
    def setup_tab4(self):
        """Configurar pestaña de análisis VADER"""
        content_frame = ttk.Frame(self.tab4, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Texto traducido
        texto_frame = ttk.LabelFrame(content_frame, text="TEXTO TRADUCIDO", padding="10")
        texto_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.texto_traducido_label = ttk.Label(
            texto_frame,
            text="",
            font=('Arial', 10, 'italic'),
            wraplength=800,
            background='white',
            padding=5,
            relief='solid'
        )
        self.texto_traducido_label.pack(fill=tk.X)
        
        # Separador
        separator = ttk.Separator(content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Puntuaciones VADER
        ttk.Label(content_frame, text="Puntuaciones VADER:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para puntuaciones
        scores_frame = ttk.Frame(content_frame)
        scores_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Positivo
        pos_frame = ttk.Frame(scores_frame)
        pos_frame.pack(fill=tk.X, pady=2)
        ttk.Label(pos_frame, text="• Positivo:", width=15, anchor=tk.W).pack(side=tk.LEFT)
        self.pos_score_label = ttk.Label(pos_frame, text="0.000", font=('Arial', 10, 'bold'))
        self.pos_score_label.pack(side=tk.LEFT)
        
        # Neutral
        neu_frame = ttk.Frame(scores_frame)
        neu_frame.pack(fill=tk.X, pady=2)
        ttk.Label(neu_frame, text="• Neutral:", width=15, anchor=tk.W).pack(side=tk.LEFT)
        self.neu_score_label = ttk.Label(neu_frame, text="0.000", font=('Arial', 10, 'bold'))
        self.neu_score_label.pack(side=tk.LEFT)
        
        # Negativo
        neg_frame = ttk.Frame(scores_frame)
        neg_frame.pack(fill=tk.X, pady=2)
        ttk.Label(neg_frame, text="• Negativo:", width=15, anchor=tk.W).pack(side=tk.LEFT)
        self.neg_score_label = ttk.Label(neg_frame, text="0.000", font=('Arial', 10, 'bold'))
        self.neg_score_label.pack(side=tk.LEFT)
        
        # Compuesto
        comp_frame = ttk.Frame(scores_frame)
        comp_frame.pack(fill=tk.X, pady=2)
        ttk.Label(comp_frame, text="• Compuesto:", width=15, anchor=tk.W).pack(side=tk.LEFT)
        self.comp_score_label = ttk.Label(comp_frame, text="0.000", font=('Arial', 10, 'bold'))
        self.comp_score_label.pack(side=tk.LEFT)
        
        # Separador
        separator2 = ttk.Separator(content_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=10)
        
        # Interpretación VADER
        interp_frame = ttk.Frame(content_frame)
        interp_frame.pack(fill=tk.X)
        
        ttk.Label(interp_frame, text="Interpretación VADER:", 
                 font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.interp_vader_label = ttk.Label(interp_frame, text="", 
                                           font=('Arial', 11, 'bold'))
        self.interp_vader_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def iniciar_analisis_con_carga(self):
        """Inicia el análisis mostrando la pantalla de carga"""
        texto = self.text_input.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un texto para analizar.")
            return
        
        if not ANALISIS_DISPONIBLE:
            messagebox.showerror("Error", 
                "No se pueden realizar análisis. Asegúrese de instalar las dependencias:\n"
                "pip install nltk deep-translator")
            return
        
        if not CARGA_DISPONIBLE:
            # Si no hay pantallas de carga, usar el método original
            self.analizar_texto()
            return
        
        if self.is_loading:
            return
        
        # Deshabilitar botones durante el análisis
        self.analizar_btn.config(state='disabled')
        self.limpiar_btn.config(state='disabled')
        self.is_loading = True
        
        # Crear y mostrar pantalla de carga
        self.loading_screen = CargaLoadingScreen()
        
        # Iniciar el análisis en un hilo separado
        analysis_thread = threading.Thread(
            target=self.ejecutar_analisis_con_carga,
            args=(texto,)
        )
        analysis_thread.start()
        
        # Mostrar la pantalla de carga
        self.loading_screen.start()
        
        # Cuando se cierra la pantalla de carga, re-habilitar botones
        self.root.after(100, self.verificar_fin_carga)
    
    def ejecutar_analisis_con_carga(self, texto):
        """Ejecuta el análisis mientras actualiza la pantalla de carga"""
        try:
            # Simular progreso inicial
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(0, self.loading_screen.update_progress, 10, "Procesando...")
                time.sleep(0.5)
            
            # Análisis con vocabulario propio
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(0, self.loading_screen.update_progress, 25, "Tokenizando el texto...")
                time.sleep(0.5)
            
            resultado_reglas, puntaje, palabras_encontradas = sentimientos(texto)
            
            # Actualizar progreso
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(0, self.loading_screen.update_progress, 45, "Análisis de reglas propias...")
                time.sleep(0.5)
            
            # Análisis con VADER
            try:
                translator = GoogleTranslator(source='auto', target='en')
                texto_traducido = translator.translate(texto)
                
                if self.loading_screen and self.loading_screen.is_running:
                    self.loading_screen.root.after(0, self.loading_screen.update_progress, 60, "Análisis con VADER...")
                    time.sleep(0.5)
                
                analizador = SentimentIntensityAnalyzer()
                puntaje_vader = analizador.polarity_scores(texto_traducido)
                
            except Exception as e:
                puntaje_vader = None
                print(f"Error en análisis VADER: {e}")
            
            # Estadísticas
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(0, self.loading_screen.update_progress, 80, "Calculando estadísticas...")
                time.sleep(0.5)
            
            import nltk
            tokens = nltk.word_tokenize(texto.lower())
            palabras_total = len(tokens)
            palabras_vocabulario = sum(1 for t in tokens if t in Reglas)
            
            # Finalizar progreso
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(0, self.loading_screen.update_progress, 95, "Configurando interfaz...")
                time.sleep(0.5)
                
                self.loading_screen.root.after(0, self.loading_screen.update_progress, 100, "¡Listo!")
                time.sleep(0.5)
            
            # Actualizar la interfaz en el hilo principal
            self.root.after(0, self.actualizar_interfaz_despues_analisis, 
                           texto, resultado_reglas, puntaje, palabras_encontradas,
                           texto_traducido if 'texto_traducido' in locals() else None,
                           puntaje_vader, palabras_total, palabras_vocabulario)
            
        except Exception as e:
            # Mostrar error
            self.root.after(0, messagebox.showerror, "Error", 
                           f"Ocurrió un error durante el análisis:\n{str(e)}")
            
            # Cerrar pantalla de carga si hay error
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(0, self.loading_screen.stop)
    
    def actualizar_interfaz_despues_analisis(self, texto, resultado_reglas, puntaje, 
                                           palabras_encontradas, texto_traducido, 
                                           puntaje_vader, palabras_total, palabras_vocabulario):
        """Actualiza la interfaz después del análisis"""
        # Mostrar texto analizado
        self.texto_analizado_label.config(text=texto)
        
        # Mostrar en pestaña de comparativa
        self.vocab_result_label.config(text=resultado_reglas)
        self.actualizar_color_sentimiento(self.vocab_result_label, resultado_reglas)
        
        # Mostrar en pestaña de vocabulario propio
        self.sentimiento_label.config(text=resultado_reglas)
        self.actualizar_color_sentimiento(self.sentimiento_label, resultado_reglas)
        self.puntuacion_label.config(text=f"{puntaje} puntos")
        
        # Mostrar palabras identificadas
        self.palabras_listbox.delete(0, tk.END)
        for palabra in palabras_encontradas:
            self.palabras_listbox.insert(tk.END, palabra)
        
        self.total_id_label.config(text=str(len(palabras_encontradas)))
        
        # Análisis con VADER
        if texto_traducido and puntaje_vader:
            # Mostrar texto traducido
            self.texto_traducido_label.config(text=texto_traducido)
            
            # Mostrar puntuaciones VADER
            self.pos_score_label.config(text=f"{puntaje_vader['pos']:.3f}")
            self.neu_score_label.config(text=f"{puntaje_vader['neu']:.3f}")
            self.neg_score_label.config(text=f"{puntaje_vader['neg']:.3f}")
            self.comp_score_label.config(text=f"{puntaje_vader['compound']:.3f}")
            
            # Interpretación VADER
            compound = puntaje_vader['compound']
            if compound >= 0.05:
                sentimiento_vader = "POSITIVO"
            elif compound <= -0.05:
                sentimiento_vader = "NEGATIVO"
            else:
                sentimiento_vader = "NEUTRO"
            
            self.vader_result_label.config(text=sentimiento_vader)
            self.actualizar_color_sentimiento(self.vader_result_label, sentimiento_vader)
            self.interp_vader_label.config(text=sentimiento_vader)
            self.actualizar_color_sentimiento(self.interp_vader_label, sentimiento_vader)
            
            # Comparativa de resultados
            if resultado_reglas == sentimiento_vader:
                self.coincidencia_label.config(
                    text="✅ Ambos métodos coinciden en el análisis.",
                    foreground=self.colors['success']
                )
            else:
                self.coincidencia_label.config(
                    text="⚠️ Los métodos difieren en su análisis.",
                    foreground=self.colors['warning']
                )
        else:
            sentimiento_vader = "ERROR"
            self.vader_result_label.config(text="ERROR")
            self.interp_vader_label.config(text="Error en análisis")
            self.coincidencia_label.config(
                text="⚠️ Error en análisis VADER",
                foreground=self.colors['danger']
            )
        
        # Estadísticas adicionales
        self.total_palabras_label.config(text=str(palabras_total))
        self.palabras_encontradas_label.config(text=str(palabras_vocabulario))
        
        if palabras_total > 0:
            porcentaje = (palabras_vocabulario / palabras_total) * 100
            self.porcentaje_label.config(text=f"{porcentaje:.1f}%")
        
        # Finalizar carga
        self.finalizar_carga()
    
    def iniciar_limpieza_con_carga(self):
        """Inicia la limpieza mostrando la pantalla de carga"""
        if not CARGA_DISPONIBLE:
            # Si no hay pantallas de carga, usar el método original
            self.limpiar_resultados()
            return
        
        if self.is_loading:
            return
        
        # Deshabilitar botones durante la limpieza
        self.analizar_btn.config(state='disabled')
        self.limpiar_btn.config(state='disabled')
        self.is_loading = True
        
        # Crear y mostrar pantalla de carga de limpieza
        self.loading_screen = LimpiezaLoadingScreen()
        
        # Iniciar la limpieza en un hilo separado
        cleanup_thread = threading.Thread(
            target=self.ejecutar_limpieza_con_carga
        )
        cleanup_thread.start()
        
        # Mostrar la pantalla de carga
        self.loading_screen.start()
        
        # Cuando se cierra la pantalla de carga, re-habilitar botones
        self.root.after(100, self.verificar_fin_carga)
    
    def ejecutar_limpieza_con_carga(self):
        """Ejecuta la limpieza mientras actualiza la pantalla de carga"""
        try:
            # Simular progreso
            steps = [
                (15, "Verificando..."),
                (30, "Eliminando registros..."),
                (50, "Estandarizando formatos..."),
                (65, "Corrigiendo..."),
                (80, "Completando..."),
                (95, "Validando para nueva carga..."),
                (100, "¡Preparado!")
            ]
            
            for progress, message in steps:
                if not self.loading_screen or not self.loading_screen.is_running:
                    break
                
                self.loading_screen.root.after(0, self.loading_screen.update_progress, progress, message)
                time.sleep(0.3)
            
            # Actualizar la interfaz en el hilo principal
            self.root.after(0, self.limpiar_resultados)
            
            # Finalizar carga
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(500, self.loading_screen.stop)
            
        except Exception as e:
            # Mostrar error
            self.root.after(0, messagebox.showerror, "Error", 
                           f"Ocurrió un error durante la limpieza:\n{str(e)}")
            
            # Cerrar pantalla de carga si hay error
            if self.loading_screen and self.loading_screen.is_running:
                self.loading_screen.root.after(0, self.loading_screen.stop)
    
    def verificar_fin_carga(self):
        """Verifica si la pantalla de carga ha terminado y re-habilita botones"""
        if self.loading_screen and self.loading_screen.is_running:
            # Volver a verificar en 100ms
            self.root.after(100, self.verificar_fin_carga)
        else:
            # Re-habilitar botones
            self.analizar_btn.config(state='normal')
            self.limpiar_btn.config(state='normal')
            self.is_loading = False
            self.loading_screen = None
    
    def finalizar_carga(self):
        """Finaliza el proceso de carga"""
        if self.loading_screen and self.loading_screen.is_running:
            self.loading_screen.root.after(500, self.loading_screen.stop)
    
    def analizar_texto(self):
        """Método original de análisis (para compatibilidad)"""
        texto = self.text_input.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un texto para analizar.")
            return
        
        if not ANALISIS_DISPONIBLE:
            messagebox.showerror("Error", 
                "No se pueden realizar análisis. Asegúrese de instalar las dependencias:\n"
                "pip install nltk deep-translator")
            return
        
        try:
            # Análisis con vocabulario propio
            resultado_reglas, puntaje, palabras_encontradas = sentimientos(texto)
            
            # Mostrar texto analizado
            self.texto_analizado_label.config(text=texto)
            
            # Mostrar en pestaña de comparativa
            self.vocab_result_label.config(text=resultado_reglas)
            self.actualizar_color_sentimiento(self.vocab_result_label, resultado_reglas)
            
            # Mostrar en pestaña de vocabulario propio
            self.sentimiento_label.config(text=resultado_reglas)
            self.actualizar_color_sentimiento(self.sentimiento_label, resultado_reglas)
            self.puntuacion_label.config(text=f"{puntaje} puntos")
            
            # Mostrar palabras identificadas
            self.palabras_listbox.delete(0, tk.END)
            for palabra in palabras_encontradas:
                valor = Reglas[palabra]
                color = self.colors['success'] if valor > 0 else self.colors['danger']
                self.palabras_listbox.insert(tk.END, palabra)
            
            self.total_id_label.config(text=str(len(palabras_encontradas)))
            
            # Análisis con VADER
            try:
                translator = GoogleTranslator(source='auto', target='en')
                texto_traducido = translator.translate(texto)
                
                analizador = SentimentIntensityAnalyzer()
                puntaje_vader = analizador.polarity_scores(texto_traducido)
                
                # Mostrar texto traducido
                self.texto_traducido_label.config(text=texto_traducido)
                
                # Mostrar puntuaciones VADER
                self.pos_score_label.config(text=f"{puntaje_vader['pos']:.3f}")
                self.neu_score_label.config(text=f"{puntaje_vader['neu']:.3f}")
                self.neg_score_label.config(text=f"{puntaje_vader['neg']:.3f}")
                self.comp_score_label.config(text=f"{puntaje_vader['compound']:.3f}")
                
                # Interpretación VADER
                compound = puntaje_vader['compound']
                if compound >= 0.05:
                    sentimiento_vader = "POSITIVO"
                elif compound <= -0.05:
                    sentimiento_vader = "NEGATIVO"
                else:
                    sentimiento_vader = "NEUTRO"
                
                self.vader_result_label.config(text=sentimiento_vader)
                self.actualizar_color_sentimiento(self.vader_result_label, sentimiento_vader)
                self.interp_vader_label.config(text=sentimiento_vader)
                self.actualizar_color_sentimiento(self.interp_vader_label, sentimiento_vader)
                
            except Exception as e:
                sentimiento_vader = "ERROR"
                self.vader_result_label.config(text="ERROR")
                self.interp_vader_label.config(text="Error en análisis")
                messagebox.showwarning("Advertencia VADER", 
                    f"Error en análisis VADER: {str(e)}\n"
                    "Asegúrese de tener conexión a internet para la traducción.")
            
            # Comparativa de resultados
            if sentimiento_vader != "ERROR" and resultado_reglas == sentimiento_vader:
                self.coincidencia_label.config(
                    text="✅ Ambos métodos coinciden en el análisis.",
                    foreground=self.colors['success']
                )
            elif sentimiento_vader != "ERROR":
                self.coincidencia_label.config(
                    text="⚠️ Los métodos difieren en su análisis.",
                    foreground=self.colors['warning']
                )
            
            # Estadísticas adicionales
            import nltk
            tokens = nltk.word_tokenize(texto.lower())
            palabras_total = len(tokens)
            palabras_vocabulario = sum(1 for t in tokens if t in Reglas)
            
            self.total_palabras_label.config(text=str(palabras_total))
            self.palabras_encontradas_label.config(text=str(palabras_vocabulario))
            
            if palabras_total > 0:
                porcentaje = (palabras_vocabulario / palabras_total) * 100
                self.porcentaje_label.config(text=f"{porcentaje:.1f}%")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante el análisis:\n{str(e)}")
    
    def actualizar_color_sentimiento(self, label, sentimiento):
        """Actualizar el color según el sentimiento"""
        if sentimiento == "POSITIVO":
            label.config(foreground=self.colors['success'])
        elif sentimiento == "NEGATIVO":
            label.config(foreground=self.colors['danger'])
        elif sentimiento == "NEUTRO":
            label.config(foreground=self.colors['secondary'])
        else:
            label.config(foreground=self.colors['dark'])
    
    def limpiar_resultados(self):
        """Limpiar todos los resultados"""
        self.text_input.delete("1.0", tk.END)
        self.texto_analizado_label.config(text="")
        
        # Limpiar comparativa
        self.vocab_result_label.config(text="")
        self.vader_result_label.config(text="")
        self.coincidencia_label.config(text="")
        
        # Limpiar estadísticas
        self.total_palabras_label.config(text="")
        self.palabras_encontradas_label.config(text="")
        self.porcentaje_label.config(text="")
        
        # Limpiar vocabulario propio
        self.sentimiento_label.config(text="")
        self.puntuacion_label.config(text="")
        self.palabras_listbox.delete(0, tk.END)
        self.total_id_label.config(text="")
        
        # Limpiar VADER
        self.texto_traducido_label.config(text="")
        self.pos_score_label.config(text="0.000")
        self.neu_score_label.config(text="0.000")
        self.neg_score_label.config(text="0.000")
        self.comp_score_label.config(text="0.000")
        self.interp_vader_label.config(text="")
        
        # Restaurar colores
        for label in [self.vocab_result_label, self.vader_result_label, 
                     self.sentimiento_label, self.interp_vader_label]:
            label.config(foreground=self.colors['dark'])

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = AnalizadorSentimientosGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()