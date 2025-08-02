import praw
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Conexión a la API de Reddit
reddit = praw.Reddit(
    client_id="Omv8li5KJSBZsdiLzTkcBQ",
    client_secret="pV-62uWfgva18a-7RNp7uc7lK41WXg",
    user_agent="AnalisisReddit (por /u/LowIndependence7659)",
)

def extract_reddit_data(subreddit_name, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
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

def analyze_data(df, tipo_grafico):
    promedio = df["Puntaje"].mean()
    maximo = df["Puntaje"].max()
    minimo = df["Puntaje"].min()
    
    st.write(f"🔹 **Puntaje Promedio**: {promedio:.2f}")
    st.write(f"🔺 **Puntaje Máximo**: {maximo}")
    st.write(f"🔻 **Puntaje Mínimo**: {minimo}")
    
    st.write("### 📊 Visualización seleccionada:")
    fig, ax = plt.subplots()

    if tipo_grafico == "Histograma (distribución de puntajes)":
        sns.histplot(df["Puntaje"], kde=True, ax=ax, color="skyblue")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Distribución de Puntajes")

    elif tipo_grafico == "Gráfico de barras por autor":
        top_authors = df.groupby("Autor")["Puntaje"].sum().sort_values(ascending=False).head(10)
        top_authors.plot(kind="bar", ax=ax, color="orange")
        ax.set_ylabel("Puntaje total")
        ax.set_title("🔝 Autores con más puntaje")
        ax.set_xlabel("Autor")
        plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)
    return fig

def main():
    st.title("🔍 Análisis de Tendencias en Reddit")

    st.sidebar.header("⚙️ Configuración")
    subreddit_name = st.sidebar.text_input("📌 Subreddit:", "technology")
    limit = st.sidebar.slider("📈 Número de publicaciones", 10, 200, 100)

    tipo_grafico = st.sidebar.radio(
        "📊 Tipo de gráfico a mostrar:",
        ("Histograma (distribución de puntajes)", "Gráfico de barras por autor")
    )

    run_analysis = st.sidebar.button("🔍 Extraer y Analizar")

    if run_analysis:
        df = extract_reddit_data(subreddit_name, limit)

        st.write("### 🗂️ Publicaciones extraídas en tiempo real")
        st.dataframe(df)

        st.write("### 📈 Análisis Estadístico")
        fig = analyze_data(df, tipo_grafico)

        # Descargar CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos como CSV",
            data=csv,
            file_name=f"{subreddit_name}_posts.csv",
            mime='text/csv'
        )

        # Descargar gráfico PNG
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(
            label="📥 Descargar gráfico como PNG",
            data=buf,
            file_name=f"{subreddit_name}_grafico.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
