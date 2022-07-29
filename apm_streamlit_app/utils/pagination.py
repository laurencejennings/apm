import streamlit as st


def paginator(label, topics_df, comments_per_page=3):
    """Paginates a set of dataframe rows.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    topics_df : pd.DataFrame
        The dataframe containing the comments to display.
    comments_per_page: int
        The number of comments to display per page.

    Returns
    -------
    pd.DataFrame
        a slice containing the comments to display
    """

    location = st.empty()
    n_pages = (len(topics_df) - 1) // comments_per_page + 1
    page_format_func = lambda i: "Page %s" % i
    if n_pages > 1:
        page_number = location.selectbox(
            f"{label} -- pages: {n_pages}",
            range(1, n_pages + 1),
            format_func=page_format_func,
        )
    else:
        page_number = 1
    min_index = (page_number - 1) * comments_per_page
    max_index = (min_index) + comments_per_page

    return topics_df[min_index:max_index]
