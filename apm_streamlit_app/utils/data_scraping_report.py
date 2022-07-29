from datetime import timedelta

import pandas as pd
import requests


def get_past_n_days_report_dataframe(n, report_name, graph_date, config):
    report_data_frame = pd.DataFrame()
    for index in range(0, n):
        cur_date = graph_date - timedelta(days=index)
        url = f"{config.get('paths')['s3_report_base_url']}/{cur_date.strftime('%Y%m%d')}/{report_name}"
        if requests.head(url).status_code == 200:
            new_row = {
                "Report Date": cur_date.strftime('%Y-%m-%d'),
                "Report URL": f'<a target="_blank" href="{url}">Click here to view report</a>',
            }
            report_data_frame = report_data_frame.append(new_row, ignore_index=True)
    return report_data_frame
