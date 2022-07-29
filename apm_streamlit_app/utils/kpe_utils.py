import pandas as pd
from cloudpathlib import S3Client

client = S3Client(no_sign_request=True)


def get_kpe_subreddits(kpe_topics_path):
    root_dir = client.CloudPath(kpe_topics_path)
    subreddit_paths = list(root_dir.iterdir())
    subreddits = []
    for x in subreddit_paths:
        subreddits.append((str(x)).replace(kpe_topics_path + "/subreddit=", "")[:-1])

    return subreddits


def get_key_phrases(kpe_topics_path, subreddit):
    path = kpe_topics_path + "/subreddit=" + subreddit
    root_dir = client.CloudPath(path)
    key_phrases_paths = list(root_dir.iterdir())
    key_phrases = []
    for x in key_phrases_paths:
        key_phrases.append((str(x)).replace(path + "/keyphrase=", "")[:-1])
    return key_phrases


def get_key_phrase_comments(kpe_topics_path, subreddit, key_phrase):
    path = kpe_topics_path + "/subreddit=" + subreddit + "/keyphrase=" + key_phrase
    root_dir = client.CloudPath(path)
    key_phrases_comments_df = pd.read_parquet(list(root_dir.iterdir())[0])
    return key_phrases_comments_df
