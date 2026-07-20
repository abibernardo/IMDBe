from pathlib import Path
import time
import requests
import pandas as pd

# ============================================================
# CONFIGURAÇÃO
# ============================================================

# COLOQUE SUA CHAVE AQUI
API_KEY = "SUA_CHAVE_AQUI"

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

DATA_DIR = Path("data")

USER_FILE = DATA_DIR / "user_tv_show_data.csv"
TMDB_CACHE = DATA_DIR / "tmdb_cache.csv"
EPISODE_CACHE = DATA_DIR / "episodes_cache.csv"
CATALOG = DATA_DIR / "catalog.csv"

TIME_BETWEEN_REQUESTS = 0.25


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def tmdb_get(endpoint, params=None):

    if params is None:
        params = {}

    params["api_key"] = API_KEY

    r = requests.get(
        BASE_URL + endpoint,
        params=params,
        timeout=30
    )

    r.raise_for_status()

    return r.json()


def poster_url(path):

    if path in [None, "", float("nan")]:
        return None

    return IMAGE_BASE + path


def load_user():

    df = pd.read_csv(USER_FILE)

    df = (
        df
        .sort_values("tv_show_name")
        .drop_duplicates("tv_show_name")
        .reset_index(drop=True)
    )

    return df


def load_tmdb_cache():

    if TMDB_CACHE.exists():

        return pd.read_csv(TMDB_CACHE)

    return pd.DataFrame(columns=[
        "tmdb_id",
        "tv_show_name",
        "poster_url",
        "backdrop_url",
        "overview",
        "genres",
        "vote_average",
        "first_air_date",
        "status",
        "number_of_seasons",
        "number_of_episodes",
        "episode_runtime"
    ])


def load_episode_cache():

    if EPISODE_CACHE.exists():

        return pd.read_csv(EPISODE_CACHE)

    return pd.DataFrame(columns=[
        "tmdb_id",
        "tv_show_name",
        "season",
        "episode",
        "episode_name",
        "overview",
        "runtime",
        "air_date",
        "watched"
    ])


# ============================================================
# TMDB
# ============================================================

def search_show(name):

    data = tmdb_get(
        "/search/tv",
        {
            "query": name,
            "language": "en-US"
        }
    )

    results = data["results"]

    if len(results) == 0:

        return None

    return results[0]["id"]


def get_show_details(tmdb_id):

    return tmdb_get(
        f"/tv/{tmdb_id}",
        {
            "language": "en-US"
        }
    )


def get_season(tmdb_id, season):

    return tmdb_get(
        f"/tv/{tmdb_id}/season/{season}",
        {
            "language": "en-US"
        }
    )


# ============================================================
# TMDB CACHE
# ============================================================

def update_tmdb_cache(user_df, cache_df):

    novos = []

    for show in sorted(user_df.tv_show_name.unique()):

        if show in cache_df.tv_show_name.values:

            print(f"✓ {show}")

            continue

        print(f"Buscando {show}")

        try:

            tmdb_id = search_show(show)

            if tmdb_id is None:

                print("Não encontrada.")

                continue

            info = get_show_details(tmdb_id)

            runtime = None

            if len(info["episode_run_time"]) > 0:

                runtime = info["episode_run_time"][0]

            genres = ", ".join(
                g["name"]
                for g in info["genres"]
            )

            novos.append({

                "tmdb_id": info["id"],

                "tv_show_name": info["name"],

                "poster_url": poster_url(
                    info["poster_path"]
                ),

                "backdrop_url": poster_url(
                    info["backdrop_path"]
                ),

                "overview": info["overview"],

                "genres": genres,

                "vote_average": info["vote_average"],

                "first_air_date": info["first_air_date"],

                "status": info["status"],

                "number_of_seasons": info["number_of_seasons"],

                "number_of_episodes": info["number_of_episodes"],

                "episode_runtime": runtime

            })

            time.sleep(TIME_BETWEEN_REQUESTS)

        except Exception as e:

            print(show)
            print(e)

    if len(novos):

        cache_df = pd.concat(
            [
                cache_df,
                pd.DataFrame(novos)
            ],
            ignore_index=True
        )

    cache_df = (
        cache_df
        .sort_values("tv_show_name")
        .reset_index(drop=True)
    )

    cache_df.to_csv(
        TMDB_CACHE,
        index=False
    )

    return cache_df

# ============================================================
# EPISODES CACHE
# ============================================================

def update_episode_cache(user_df, tmdb_df, episode_df):

    novos = []

    for _, show in user_df.iterrows():

        nome = show["tv_show_name"]

        vistos = int(show["nb_episodes_seen"])

        registro = tmdb_df.loc[
            tmdb_df["tv_show_name"] == nome
        ]

        if registro.empty:

            continue

        tmdb_id = int(registro.iloc[0]["tmdb_id"])

        # Já existe?
        existentes = episode_df[
            episode_df["tmdb_id"] == tmdb_id
        ]

        if len(existentes) > 0:

            print(f"✓ Episódios: {nome}")

            continue

        print(f"Baixando episódios: {nome}")

        detalhes = get_show_details(tmdb_id)

        contador = 0

        for season in detalhes["seasons"]:

            season_number = season["season_number"]

            # Ignora especiais (temporada 0)
            if season_number == 0:
                continue

            try:

                season_data = get_season(
                    tmdb_id,
                    season_number
                )

            except Exception as e:

                print(
                    f"Erro temporada {season_number}: {nome}"
                )

                print(e)

                continue

            for ep in season_data["episodes"]:

                contador += 1

                runtime = None

                if ep.get("runtime") is not None:
                    runtime = ep["runtime"]

                watched = contador <= vistos

                novos.append({

                    "tmdb_id": tmdb_id,

                    "tv_show_name": nome,

                    "season": season_number,

                    "episode": ep["episode_number"],

                    "episode_name": ep["name"],

                    "overview": ep["overview"],

                    "runtime": runtime,

                    "air_date": ep["air_date"],

                    "watched": watched

                })

            time.sleep(TIME_BETWEEN_REQUESTS)

    if len(novos):

        episode_df = pd.concat(
            [
                episode_df,
                pd.DataFrame(novos)
            ],
            ignore_index=True
        )

    episode_df = (
        episode_df
        .sort_values(
            [
                "tv_show_name",
                "season",
                "episode"
            ]
        )
        .reset_index(drop=True)
    )

    episode_df.to_csv(
        EPISODE_CACHE,
        index=False
    )

    return episode_df

# ============================================================
# CATALOG
# ============================================================

def build_catalog(user_df, tmdb_df):

    catalog = user_df.merge(
        tmdb_df,
        on="tv_show_name",
        how="left"
    )

    catalog["progress"] = (
        catalog["nb_episodes_seen"].astype(str)
        + " / "
        + catalog["number_of_episodes"].fillna(0).astype(int).astype(str)
    )

    catalog["progress_pct"] = (
        catalog["nb_episodes_seen"]
        / catalog["number_of_episodes"]
    )

    catalog["progress_pct"] = (
        catalog["progress_pct"]
        .fillna(0)
        .clip(upper=1)
    )

    catalog["completed"] = (
        catalog["nb_episodes_seen"]
        >=
        catalog["number_of_episodes"]
    )

    catalog = catalog[[
        "tv_show_name",
        "tmdb_id",
        "poster_url",
        "backdrop_url",
        "overview",
        "genres",
        "vote_average",
        "first_air_date",
        "status",
        "number_of_seasons",
        "number_of_episodes",
        "episode_runtime",
        "is_followed",
        "is_favorited",
        "nb_episodes_seen",
        "progress",
        "progress_pct",
        "completed"
    ]]

    catalog = catalog.sort_values(
        "tv_show_name"
    )

    catalog.to_csv(
        CATALOG,
        index=False
    )

    return catalog

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("Lendo arquivos...")
    print("=" * 60)

    DATA_DIR.mkdir(exist_ok=True)

    user_df = load_user()
    tmdb_df = load_tmdb_cache()
    episode_df = load_episode_cache()

    print()
    print(f"{len(user_df)} séries encontradas.")

    print()
    print("=" * 60)
    print("Atualizando cache de séries...")
    print("=" * 60)

    tmdb_df = update_tmdb_cache(
        user_df,
        tmdb_df
    )

    print()
    print("=" * 60)
    print("Atualizando cache de episódios...")
    print("=" * 60)

    episode_df = update_episode_cache(
        user_df,
        tmdb_df,
        episode_df
    )

    print()
    print("=" * 60)
    print("Gerando catálogo...")
    print("=" * 60)

    catalog = build_catalog(
        user_df,
        tmdb_df
    )

    print()
    print("=" * 60)
    print("FINALIZADO")
    print("=" * 60)
    print(f"Séries: {len(catalog)}")
    print(f"Episódios: {len(episode_df)}")
    print()
    print(f"Arquivo gerado: {CATALOG}")
    print(f"Arquivo gerado: {TMDB_CACHE}")
    print(f"Arquivo gerado: {EPISODE_CACHE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
