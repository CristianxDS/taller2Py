# Librerías necesarias
import praw  # API de Reddit
import pandas as pd  # Manipulación de datos
import streamlit as st  # Interfaz web
import numpy as np  # Operaciones matemáticas
import matplotlib.pyplot as plt  # Gráficos
import seaborn as sns  # Gráficos estadísticos

# Conexión a la API de Reddit
reddit = praw.Reddit(
    client_id="Omv8li5KJSBZsdiLzTkcBQ",
    client_secret="pV-62uWfgva18a-7RNp7uc7lK41WXg",
    user_agent="AnalisisReddit (por /u/LowIndependence7659)",
)

# Función para extraer datos desde Reddit
def extract_reddit_data(subreddit_name, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
# Extrae los posts más populares 
    top_posts = subreddit.hot(limit=limit)  
    
    data = []
    for post in top_posts:
        data.append({
            "Título": post.title,
            "Puntaje": post.score,
            "Número de Comentarios": post.num_comments,
            "Autor": post.author.name if post.author else "Anónimo",
            "URL": post.url,
            "Fecha UTC": post.created_utc
        })
    return pd.DataFrame(data)

# Función para mostrar estadísticas y gráficas
def analyze_data(df):
    promedio = df["Puntaje"].mean()
    maximo = df["Puntaje"].max()
    minimo = df["Puntaje"].min()
    
# Mostrar estadísticas básicas
    st.write(f"🔹 **Puntaje Promedio**: {promedio:.2f}")
    st.write(f"🔺 **Puntaje Máximo**: {maximo}")
    st.write(f"🔻 **Puntaje Mínimo**: {minimo}")

# Gráfico de distribución
    st.write("### 📊 Distribución de Puntajes")
    fig, ax = plt.subplots()
    sns.histplot(df["Puntaje"], kde=True, ax=ax, color="skyblue")
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

# Función principal de la aplicación
def main():
    st.title("🔍 Análisis de Tendencias en Reddit")
    
# Entrada del usuario
    subreddit_name = st.text_input("📌 Ingresa el nombre del Subreddit:", "Gaming")
    limit = st.slider("📈 Número de publicaciones a analizar", 10, 200, 100)
    
    if st.button("Extraer y Analizar Datos"):
        df = extract_reddit_data(subreddit_name, limit)
        
# Mostrar los datos
        st.write("### 🗂️ Publicaciones extraídas")
        st.dataframe(df)
        
# Mostrar análisis estadístico
        st.write("### 📊 Análisis Estadístico")
        analyze_data(df)
        
# Botón para descargar el DataFrame como CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos como CSV",
            data=csv,
            file_name=f"{subreddit_name}_posts.csv",
            mime='text/csv'
        )

if __name__ == "__main__":
    main()
