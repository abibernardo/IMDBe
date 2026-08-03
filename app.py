import streamlit as st

st.set_page_config(
    page_title="IMDBe",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:2rem;
    max-width:1300px;
}

html, body, [data-testid="stAppViewContainer"]{
    background:#0f1117;
    color:white;
}

/* Título */

.title{
    text-align:center;
    font-size:4rem;
    font-weight:800;
    letter-spacing:2px;
}

.subtitle{
    text-align:center;
    color:#AAAAAA;
    margin-bottom:50px;
}

/* Banner */

.hero{
    height:330px;
    border-radius:20px;
    background:#1d1f29;
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:28px;
    color:#777;
    margin-bottom:50px;
}

/* Títulos */

.section{
    font-size:30px;
    font-weight:bold;
    margin-top:40px;
    margin-bottom:20px;
}

/* Poster */

.poster{

    border-radius:15px;
    background:#232632;
    aspect-ratio:2/3;

    display:flex;
    justify-content:center;
    align-items:center;

    color:#666;
    font-size:20px;
    margin-bottom:10px;
}

.name{

    text-align:center;
    font-size:18px;
    font-weight:600;

}

.rating{

    text-align:center;
    color:#FFD54F;
    margin-bottom:25px;

}

</style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">IMDBe</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">The personal movie & TV archive of Be</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero">BANNER DA SÉRIE EM DESTAQUE</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="section">⭐ Favorites</div>',
unsafe_allow_html=True)

cols = st.columns(5)

for c in cols:

    with c:

        st.markdown(
            '<div class="poster">Poster</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="name">Breaking Bad</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="rating">★★★★★</div>',
            unsafe_allow_html=True
        )


st.markdown('<div class="section">📺 TV Shows</div>',
unsafe_allow_html=True)

cols = st.columns(5)

series = [
    "Dark",
    "Severance",
    "Succession",
    "The Bear",
    "Lost"
]

for c,nome in zip(cols,series):

    with c:

        st.markdown(
            '<div class="poster">Poster</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="name">{nome}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="rating">★★★★☆</div>',
            unsafe_allow_html=True
        )


st.markdown('<div class="section">🎬 Movies</div>',
unsafe_allow_html=True)

cols = st.columns(5)

filmes = [
    "Interstellar",
    "Whiplash",
    "Parasite",
    "The Prestige",
    "Arrival"
]

for c,nome in zip(cols,filmes):

    with c:

        st.markdown(
            '<div class="poster">Poster</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="name">{nome}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="rating">★★★★★</div>',
            unsafe_allow_html=True
        )
