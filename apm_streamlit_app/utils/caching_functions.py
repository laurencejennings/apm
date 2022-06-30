import pickle
import urllib

import streamlit as st

from apm_streamlit_app.utils.urls import generate_url


def read_kpe_pickle(graph_date, config):
    (kpe_topics_path, _, _) = generate_url(graph_date, "topics_comments.pkl", config)
    file = urllib.request.urlopen(kpe_topics_path)
    return pickle.load(file)


@st.cache()
def cache_kpe_pickle(graph_date, config):
    read_kpe_pickle(graph_date, config)


@st.cache()
def cache_graph_path(path):
    return path


@st.cache()
def cache_comments_of_subreddit(df):
    return df
