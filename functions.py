import streamlit as st
import pandas as pd
import geopandas as gpd

from retrying import retry

from constants import berlin_pop


@st.cache(show_spinner=False, max_entries=1, ttl=3600)
@retry(wait_fixed=1000, stop_max_attempt_number=10)
def get_infection_data():
    csv_loc = "https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-bezirke-gesamtuebersicht/index.php/index/all.csv"
    df = pd.read_csv(csv_loc, sep=";").iloc[-7:]

    df.columns = df.columns.str.replace("_", "-").str.title().str.replace(
        "oe", "ö")

    return df.iloc[:, 2:].sum() / berlin_pop, df["Datum"].agg(["min", "max"])


@st.cache(show_spinner=False, max_entries=1)
def get_berlin():
    berlin = gpd.read_file("berlin_bezirke.geojson")
    centroids = berlin["geometry"].to_crs(epsg=3035).centroid.to_crs(epsg=4326)
    berlin["lat"] = centroids.y
    berlin["lng"] = centroids.x
    return berlin
