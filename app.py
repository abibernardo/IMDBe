import streamlit as st
import pandas as pd

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="IMDBe",
    page_icon="🎬",
    layout="wide"
)

# ==========================================================
# DADOS
# ==========================================================

@st.cache_data
def carregar_lista(url):

    df = pd.read_csv(url)

    return (
        df[
            [
                "Title",
                "URL",
                "Year",
                "IMDb Rating",
                "Genres",
                "Your Rating"
            ]
        ]
        .sort_values(
            by=["Your Rating", "Title"],
            ascending=[False, True]
        )
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

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:3rem;
}


/* ---------- Cabeçalho ---------- */

.title{
    text-align:center;
    font-size:58px;
    font-weight:800;
    margin-bottom:0;
}

.subtitle{
    text-align:center;
    color:#A5A5A5;
    margin-bottom:40px;
}

.hero{

    height:320px;
    border-radius:18px;
    background:#222;

    display:flex;
    justify-content:center;
    align-items:center;

    color:#777;
    font-size:28px;

    margin-bottom:60px;

}

/* ---------- Seções ---------- */

.section{

    font-size:30px;
    font-weight:700;

    margin-top:50px;
    margin-bottom:25px;

}

/* ---------- Listas ---------- */

.item{

    background:#181818;
    border:1px solid #2A2A2A;

    border-radius:12px;

    padding:14px 18px;

    margin-bottom:10px;

    font-size:17px;

}

.masterpiece{

    background: linear-gradient(90deg, #3B2F00, #242424);

    border: 1px solid #C9A227;

    color: #FFE082;

    font-weight: 700;

}

.masterpiece-silver{

    background: linear-gradient(90deg, #3C4148, #242424);

    border: 1px solid #BFC5CC;

    color: #ECEFF1;

    font-weight: 700;

}

.masterpiece-bronze{

    background: linear-gradient(90deg, #4E342E, #242424);

    border: 1px solid #CD7F32;

    color: #F3E5D8;

    font-weight: 700;

}

.nota{

    text-align:right;
    color:#FFD54F;
    font-weight:bold;
    padding-top:14px;

}

/* ---------- Recomenda ---------- */

.review{

    background:#181818;

    border-radius:18px;

    border:1px solid #2B2B2B;

    overflow:hidden;

    margin-bottom:30px;

}

.poster{

    width:170px;
    height:250px;

    background:#333;

    border-radius:12px;

    display:flex;
    justify-content:center;
    align-items:center;

    color:#888;

}

.review-title{

    font-size:30px;
    font-weight:bold;
    margin-bottom:10px;

}

.review-text{

    color:#DDDDDD;
    line-height:1.8;
    font-size:17px;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# CABEÇALHO
# ==========================================================

st.markdown(
    "<div class='title'>IMDBe</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Arquivo Pessoal de Televisão do Be</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        max-width:850px;
        margin:0 auto 50px auto;
        text-align:center;
        color:#CFCFCF;
        font-size:18px;
        line-height:1.8;
    ">
        O <b>IMDBe</b> é o arquivo pessoal de séries do crítico Bernardo Abib, reconhecido internacionalmente pelo seu olhar sensível à arte, conhecimento profundo da história da televisão, gosto sofisticado e humildade.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        max-width:850px;
        margin:0 auto 50px auto;
        text-align:center;
        color:#CFCFCF;
        font-size:18px;
        line-height:1.8;
    ">
        Séries com notas de 8 a 10 são todas endossadas pelo crítico, e são recomendadas sem ressalvas pelo IMDBe. Ao clicar no nome da série, o visitante será direcionado para um arquivo de séries menos conhecido (IMDb), com mais especificações sobre a produção.
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# FUNÇÕES
# ==========================================================

def mostrar_lista(df):

    for _, serie in df.iterrows():

        col1, col2 = st.columns([6,1])

        nota = serie["Your Rating"]

        # Cor diferente para 10/10
        if pd.notna(nota):

            nota = int(nota)

            if nota == 10:
                classe = "item masterpiece"

            elif nota == 9:
                classe = "item masterpiece-silver"

            elif nota == 8:
                classe = "item masterpiece-bronze"

            else:
                classe = "item"

        else:
            classe = "item"

        with col1:

            st.markdown(
                f"""
                <div class="{classe}">
    <a href="{serie['URL']}" target="_blank"
       style="
            color:inherit;
            text-decoration:none;
            display:block;
            width:100%;
       ">
        {serie["Title"]}
    </a>
</div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            if pd.notna(nota):

                st.markdown(
                    f"""
                    <div class="nota">
                        {int(nota)}/10
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '<div class="nota">—</div>',
                    unsafe_allow_html=True
                )


def recomendacao(nome, poster, texto):

    st.markdown("<div class='review'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,4])

    with col1:

        st.image(
            poster,
            use_container_width=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="review-title">
                {nome}
            </div>

            <div class="review-text">
                {texto}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# IMDBE RECOMENDA
# ==========================================================

st.markdown(
    "<div class='section'>⭐ IMDBe recomenda</div>",
    unsafe_allow_html=True
)

recomendacao(
    "Industry",
   "posters/industry.jpg",
    "Forte candidata a série da década, Industry acompanha jovens adultos adentrando o mundo corporativo, se descobrindo, se perdendo e se transformando em meio ao caos do capitalismo tardio. Hiperssexual e impetuosa, Industry vai mudar a forma como você enxerga Televisão."
)

recomendacao(
    "Atlanta",
"posters/atlanta.jpg",
    "Num projeto atemporal que revolucionou a televisão, Donald Glover escreve, dirige e atua numa obra surrealista que deixa Luis Bunuel no chinelo. Atlanta é uma comédia dramática que representa, por meio do surrealismo, como as dinâmicas sociais e raciais interagem com a psique dos negros estadunidenses. Devastadora, hilária e absolutamente brilhante, Donald Glover rompe todas as barreiras de gênero possíveis e cria uma obra indescritível."
)

recomendacao(
    "Arrested Development",
"posters/arrested development 2.jpeg",
    "A comédia mais bem amarrada de todos os tempos, décadas a frente do seu tempo. Pontos vão se conectando brilhantemente ao longo dos episódios e acrescentando camadas ao humor, chegando a um ponto onde um episódio assistido 5 vezes, pode te arrancar risadas por 5 razões completamente diferentes. Algumas sequências são tão inacreditáveis que fazem você se perguntar: 'eles escreveram a temporada toda só para fazer essa piada?'"
)


# ==========================================================
# ACOMPANHANDO
# ==========================================================

st.markdown(
    "<div class='section'>📺 Acompanhando</div>",
    unsafe_allow_html=True
)

mostrar_lista(df_assistindo)

# ==========================================================
# FINALIZADAS
# ==========================================================

st.markdown(
    "<div class='section'>✅ Finalizadas</div>",
    unsafe_allow_html=True
)

mostrar_lista(df_finalizadas)

# ==========================================================
# ABANDONADAS
# ==========================================================

st.markdown(
    "<div class='section'>🛑 Abandonadas</div>",
    unsafe_allow_html=True
)

mostrar_lista(df_abandonadas)
