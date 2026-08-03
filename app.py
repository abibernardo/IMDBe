import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IMDBe",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# DADOS
# ============================================================

@st.cache_data
def carregar_lista(url):

    df = pd.read_csv(url)

    return (
        df[["Title", "Year", "IMDb Rating", "Genres", "Your Rating"]]
        .sort_values("Title")
        .reset_index(drop=True)
    )


df_finalizadas = carregar_lista(
    "https://raw.githubusercontent.com/abibernardo/IMDBe/refs/heads/main/series/finalizadas.csv"
)

df_assistindo = carregar_lista(
    "https://raw.githubusercontent.com/abibernardo/IMDBe/refs/heads/main/series/assistindo.csv"
)

df_abandonadas = carregar_lista(
    "https://raw.githubusercontent.com/abibernardo/IMDBe/refs/heads/main/series/abandonadas.csv"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    max-width:1300px;
    padding-top:2rem;
}

.title{
    text-align:center;
    font-size:60px;
    font-weight:800;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:40px;
}

.hero{
    height:320px;
    border-radius:18px;
    background:#232323;
    display:flex;
    justify-content:center;
    align-items:center;
    color:gray;
    font-size:30px;
    margin-bottom:50px;
}

.section{
    font-size:30px;
    font-weight:bold;
    margin-top:40px;
    margin-bottom:20px;
}

.poster{

    aspect-ratio:2/3;
    border-radius:12px;
    background:#2b2b2b;

    display:flex;
    justify-content:center;
    align-items:center;

    color:gray;
    margin-bottom:10px;
}

.name{

    text-align:center;
    font-weight:bold;

}

.rating{

    text-align:center;
    color:#FFD54F;
    margin-bottom:25px;

}

.review{

    border:1px solid #333;
    border-radius:15px;
    padding:18px;
    margin-bottom:20px;

}

.review h3{

    margin-top:0;

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown("<div class='title'>IMDBe</div>", unsafe_allow_html=True)

st.markdown(
"<div class='subtitle'>The personal movie & TV archive of Be</div>",
unsafe_allow_html=True
)

st.markdown(
"<div class='hero'>BANNER DA SÉRIE EM DESTAQUE</div>",
unsafe_allow_html=True
)


# ============================================================
# FUNÇÃO DOS CARDS
# ============================================================

def mostrar_cards(df):

    N_COLS = 5

    for i in range(0, len(df), N_COLS):

        cols = st.columns(N_COLS)

        for col, (_, serie) in zip(cols, df.iloc[i:i+N_COLS].iterrows()):

            with col:

                st.markdown(
                    "<div class='poster'>Poster</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<div class='name'>{serie['Title']}</div>",
                    unsafe_allow_html=True
                )

                nota = serie["Your Rating"]

                if pd.notna(nota):

                    st.markdown(
                        f"<div class='rating'>{int(nota)}/10</div>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        "<div class='rating'>—</div>",
                        unsafe_allow_html=True
                    )


# ============================================================
# ACOMPANHANDO
# ============================================================

st.markdown(
"<div class='section'>📺 Acompanhando</div>",
unsafe_allow_html=True
)

mostrar_cards(df_assistindo)


# ============================================================
# IMDBE RECOMENDA
# ============================================================

st.markdown(
"<div class='section'>⭐ IMDBe recomenda</div>",
unsafe_allow_html=True
)

for serie in [
    "Breaking Bad",
    "Dark",
    "Severance"
]:

    col1, col2 = st.columns([1,4])

    with col1:

        st.markdown(
            "<div class='poster'>Poster</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class='review'>
            <h3>{serie}</h3>

            Aqui ficará um pequeno texto escrito por você
            explicando por que recomenda essa série.

            Pode ter uma ou duas linhas ou até um pequeno
            parágrafo.

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FINALIZADAS
# ============================================================

st.markdown(
"<div class='section'>✅ Finalizadas</div>",
unsafe_allow_html=True
)

mostrar_cards(df_finalizadas)


# ============================================================
# ABANDONADAS
# ============================================================

st.markdown(
"<div class='section'>🛑 Abandonadas</div>",
unsafe_allow_html=True
)

mostrar_cards(df_abandonadas)
