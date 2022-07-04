import re
import urllib.request  # type: ignore
from datetime import date

import streamlit as st
import streamlit.components.v1 as components

from apm_streamlit_app.config.config_loader import CONFIG_PATH, read_config_from_path
from apm_streamlit_app.utils.caching_functions import cache_comments_of_subreddit
from apm_streamlit_app.utils.dates import get_date_n_days_before_today
from apm_streamlit_app.utils.error_messages import failed_to_load_graph
from apm_streamlit_app.utils.file_names import create_file_name_from_params
from apm_streamlit_app.utils.input_manipulation import (
    convert_percentage_to_fraction_string,
)
from apm_streamlit_app.utils.kpe_utils import read_kpe_pickle
from apm_streamlit_app.utils.pagination import paginator
from apm_streamlit_app.utils.urls import generate_url

st.set_page_config(layout="wide")
st.title("Aaquaverse Passion Maps")
st.markdown("**APM version 1.4**")
main_Section = st.container()
plot_Section = st.container()
community_Section = st.container()
charts_Section = st.container()

config = read_config_from_path(CONFIG_PATH)
GRAPH_DATE = get_date_n_days_before_today(config.get("dates")["days_before_today"])

with st.spinner("Loading topics data"):
    comments_kpes_per_subreddit = read_kpe_pickle(GRAPH_DATE, config)

subreddits_with_topics = list(comments_kpes_per_subreddit.keys())

with main_Section:
    st.header("MAGIC graph")
    st.markdown(
        "The MAGIC graph here is mapped out based on the first ~500 subreddits for Music, Arts & Entertainment, Games and Interests,"
        + "with the addition of some general, geographical and demographic subreddits "
    )

    st.markdown(
        "**Each node represents a subreddit and edge represents strength between subreddits.**"
    )
    st.markdown("---")

    st.markdown(
        f'<p style="color:Red;font-size:20px;">Note</p>', unsafe_allow_html=True
    )
    st.markdown(
        f"The subreddits appear in the graph if they have had active users in the past {config.get('graph_settings')['n_days']} days"
    )
    st.markdown(
        f"**These graphs were produced using data from the past {config.get('graph_settings')['n_days']} days**"
    )

    st.header("Subreddit topics")
    with st.expander("Explore subreddit topics", expanded=False):

        c1, c2 = st.columns((1, 3))
        with c1:
            subreddit_to_explore = st.selectbox(
                "Subreddit to explore:", [None] + subreddits_with_topics
            )

            if subreddit_to_explore is not None:
                subreddit_kps = list(
                    comments_kpes_per_subreddit[subreddit_to_explore].keys()
                )[2:]
                if len(subreddit_kps):
                    st.write("Showing data for:", subreddit_to_explore)
                    # at the moment these lines are commented because we are using too few comments.
                    # st.write(f'Number of comments used for key phrase extraction in {option} subreddit:',
                    #          comments_kpe_subreddit[option]['kpe_num_comments'])

                    kp_to_explore = st.selectbox(
                        "topics to explore:", [None] + subreddit_kps
                    )
                    if kp_to_explore:
                        st.write("Showing data for topic:", kp_to_explore)
                        comments = cache_comments_of_subreddit(
                            comments_kpes_per_subreddit[subreddit_to_explore][
                                kp_to_explore
                            ]
                        )

                        if len(comments):
                            with c2:
                                comments_of_page = paginator(
                                    f"Showing the topics, {config.get('paginator')['comments_per_page']} at the time",
                                    comments,
                                )
                                comments_data = list(
                                    zip(
                                        comments_of_page.body,
                                        comments_of_page.link_id,
                                        comments_of_page.id,
                                    )
                                )
                                for comment in comments_data:
                                    post = f"https://www.reddit.com/r/{subreddit_to_explore}/comments/{comment[1][3:]}/comment/{comment[2]}"
                                    link = f"[open on reddit.com]({post})"
                                    highlighted_comment = re.sub(
                                        "(?i)("
                                        + "|".join(map(re.escape, [kp_to_explore]))
                                        + ")",
                                        '<span style="color:Red;font-size:20px;">'
                                        + r"\1"
                                        + "</span>",
                                        comment[0],
                                    )

                                    st.markdown(link)
                                    st.write(
                                        highlighted_comment, unsafe_allow_html=True
                                    )
                                    st.markdown("""---""")

    c1, c2 = st.columns((3, 1))
    with c2:
        st.header("Graph Parameters")
        with st.form("main_form"):
            confidence_value = st.selectbox(
                "Confidence(%)",
                options=(5, 10, 20),
                help="For an outgoing edge(A—>B) this indicates the probability that given a user is active in the subreddit A "
                "then they are also active in B. The higher the minimum confidence, the fewer the edges. The edges will be more certain "
                "since they represent higher probabilities. ",
            )
            interest_value = st.selectbox(
                "Interest(%)",
                options=("No threshold", 0, 10, 20),
                help="For an outgoing edge(A—>B) this indicates how interesting or surprising this link is. If every user in the dataset "
                "is a member of B (extremely popular subreddit) then any association with B will be trivial and uninteresting. "
                "If B is a niche subreddit but still has an association with A then their association is interesting. "
                "The higher the minimum interest, the fewer the edges. -1 represents connections which are obvious ones",
            )
            min_items_value = st.selectbox(
                "Minimum Items",
                options=(2, 4, 7),
                help="Minimum number of comments made by a user. As the number increases, "
                "only users with high activity are included in the graph, and thus the graph would be more reliable.",
            )
            node_sizing = st.selectbox(
                "Node sizing",
                options=("Absolute Size", "Potential Size"),
                help="Determines which attribute is used to show the node size. Absolute Size is number of comments inside reddit."
                "Potential Size takes into account aboslute size plus all incoming edge comments",
            )

            submitted = st.form_submit_button("Load Graph")
            min_conf = convert_percentage_to_fraction_string(confidence_value)
            min_interest = convert_percentage_to_fraction_string(interest_value)
            min_items = str(min_items_value)
            size = str(node_sizing).lower().replace(" ", "_")

            graph_file_name = create_file_name_from_params(
                "association_graph", min_items, min_conf, min_interest, size
            )

            (url, plotted_graph_date, errors) = generate_url(
                GRAPH_DATE, graph_file_name, config
            )

            st.markdown(
                "**Below are the colours of the verticals as provided by PET.**"
            )
            st.image(
                "https://sagemaker-eu-west-1-100701698608.s3.eu-west-1.amazonaws.com/reddit_graph_data/legend.png",
                width=None,
                use_column_width=None,
            )

    with c1:
        if submitted:
            if len(errors):
                st.error(failed_to_load_graph(errors[-1]))
            else:
                components.html(urllib.request.urlopen(url).read(), height=900)
        else:
            # This is required to display the graph for the default parameters.
            components.html(urllib.request.urlopen(url).read(), height=900)

with plot_Section:
    plot_Section.header("Compare MAGIC Graph with Community Detection Graph ")
    plot_Section.markdown(
        "On the left is the MAGIC graph, on the right the Community Detection one."
    )
    plot_Section.markdown(
        "**The Community Detection graph** is where the algorithm clusters communities together automatically based on edge strength. The different clusters are shown with different colors."
    )
    plot_Section.markdown(
        "As it's an auto-detection, the colour groupings might change every now and then, hence, there will be no legend to map colour to a vertical."
    )
    plot_Section.markdown(
        f'<p style="color:Red;font-size:20px;">Note</p>', unsafe_allow_html=True
    )
    plot_Section.markdown(
        f"The communities appear in the graph if they have had active users in the past {config.get('graph_settings')['n_days']} days"
    )
    c1, c2 = st.columns((1, 1))
    graph_date = date(2022, 6, 29)
    with c1:
        c1.header("MAGIC Graph")
        st.markdown("**Graph parameters used are below.**")
        st.markdown("Min confidence: 5%")
        st.markdown("Min interest: -100%")
        st.markdown("Minimum Items: 2")
        st.markdown("Node Sizing: Absolute Size")
        base_file_name = "association_graph__min_items_2__min_confidence_0_05__min_interest_-1_0__node_wt_absolute_size.html"
        (url, plotted_graph_date, errors) = generate_url(
            graph_date, base_file_name, config
        )

        if len(errors):
            st.error(failed_to_load_graph(errors[-1]))
        else:
            components.html(urllib.request.urlopen(url).read(), height=900)
    with c2:
        c2.header("Community Detection Graph")
        st.markdown("**Graph parameters used are below.**")
        st.markdown("Min confidence: 5%")
        st.markdown("Min interest: -100%")
        st.markdown("Minimum Items: 2")
        st.markdown("Node Sizing: Absolute Size")
        base_file_name_communtiy = "greedy__association_graph__min_items_2__min_confidence_0_05__min_interest_-1_0__node_wt_absolute_size.html"
        (url, plotted_graph_date, errors) = generate_url(
            graph_date, base_file_name_communtiy, config
        )

        if len(errors):
            st.error(failed_to_load_graph(errors[-1]))
        else:
            components.html(urllib.request.urlopen(url).read(), height=900)
