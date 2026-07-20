import streamlit as st
import pandas as pd

# =====================================================
# Configuração
# =====================================================

st.set_page_config(
    page_title="Meu Catálogo",
    page_icon="🎬",
    layout="wide"
)

URL = "https://raw.githubusercontent.com/abibernardo/IMDBe/refs/heads/main/user_tv_show_data.csv"

df = pd.read_csv(URL)

df = (
    df.sort_values("tv_show_name")
      .drop_duplicates("tv_show_name")
      .reset_index(drop=True)
)

# =====================================================
# Session State
# =====================================================

if "selected_show" not in st.session_state:
    st.session_state.selected_show = None

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("🎬 Meu Catálogo")

if st.sidebar.checkbox("Somente favoritas"):
    df = df[df["is_favorited"] == 1]

if st.sidebar.checkbox("Somente acompanhando"):
    df = df[df["is_followed"] == 1]

busca = st.sidebar.text_input("Pesquisar")

if busca:
    df = df[
        df["tv_show_name"].str.contains(
            busca,
            case=False,
            na=False
        )
    ]

# =====================================================
# Métricas
# =====================================================

st.title("🎬 Meu Catálogo")

c1, c2, c3 = st.columns(3)

c1.metric("Séries", len(df))
c2.metric("Favoritas", int(df.is_favorited.sum()))
c3.metric("Episódios vistos", int(df.nb_episodes_seen.sum()))

st.divider()

# =====================================================
# Layout
# =====================================================

left, right = st.columns([3, 2])

# =====================================================
# Catálogo
# =====================================================

with left:

    cols = st.columns(3)

    for i, (_, row) in enumerate(df.iterrows()):

        with cols[i % 3]:

            st.image(
                "https://placehold.co/300x450?text=Poster",
                use_container_width=True
            )

            st.markdown(
                f"**{row['tv_show_name']}**"
            )

            st.caption(
                f"{row['nb_episodes_seen']} episódios vistos"
            )

            if row["is_favorited"]:
                st.write("❤️ Favorita")

            if st.button(
                "Detalhes",
                key=row["tv_show_id"]
            ):
                st.session_state.selected_show = row

# =====================================================
# Painel lateral
# =====================================================

with right:

    st.subheader("Detalhes")

    if st.session_state.selected_show is None:

        st.info(
            "Clique em uma série."
        )

    else:

        s = st.session_state.selected_show

        st.image(
            "https://placehold.co/500x750?text=Poster",
            use_container_width=True
        )

        st.header(
            s["tv_show_name"]
        )

        st.write(
            f"**Episódios vistos:** {s['nb_episodes_seen']}"
        )

        st.write(
            f"**Favorita:** {'Sim' if s['is_favorited'] else 'Não'}"
        )

        st.write(
            f"**Acompanhando:** {'Sim' if s['is_followed'] else 'Não'}"
        )

        st.button(
            "Marcar episódio (em breve)"
        )
