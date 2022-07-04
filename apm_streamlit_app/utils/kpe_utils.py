import pickle
import urllib

from apm_streamlit_app.utils.urls import generate_url


def read_kpe_pickle(graph_date, config):
    return dict(ciccio=1)
    (kpe_topics_path, _, _) = generate_url(graph_date, "topics_comments.pkl", config)
    file = urllib.request.urlopen(kpe_topics_path)
    return pickle.load(file)
