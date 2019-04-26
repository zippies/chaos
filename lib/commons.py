# -*- encoding:utf-8 -*-
from datetime import datetime
import traceback
import requests


def replace_week(string):
    return string.replace("Sunday", "周日").replace("Monday", "周一").replace("Tuesday", "周二").replace("Wednesday",
            "周三").replace("Thursday", "周四").replace("Friday", "周五").replace("Saturday", "周六")


def time_to_timestamp(timestr, formatter="%Y-%m-%d %H:%M:%S"):
    outdate = datetime.strptime(timestr, formatter)
    return str(int((outdate - datetime(1970,1,1)).total_seconds()) * 1000)


def get_data_from_grail(db, sql, start_time, end_time, limit=100, grail_url="http://host:port/api/query", time_formatter="%Y-%m-%d %H:%M:%S"):
    info = {"code": 0, "data": None, "errorMsg": None, "sql": None}
    try:
        sql = "{sql} AND time >= {start_time}000000 AND time < {end_time}000000 ORDER BY time DESC LIMIT {limit}".format(
            sql=sql,
            start_time=time_to_timestamp(start_time, time_formatter),
            end_time=time_to_timestamp(end_time, time_formatter),
            limit=limit
        )
        info["sql"] = sql
        params = {
            "db": db,
            "q": sql,
            "epoch": "ms"
        }
        r = requests.get(grail_url, params=params)
        info["data"] = r.json().get("results", [{}])[0].get("series", [{}])[0].get("values", [])
    except Exception as e:
        info["errorMsg"] = traceback.format_exc()
        info["code"] = 1
    finally:
        return info


if __name__ == "__main__":
    print get_data_from_grail(
        "decision_engine_system",
        """SELECT * FROM \"de-access/access_result\" where processCode='bkk_features_strategy'""",
        "2018-07-28 15:03:00",
        "2018-07-29 23:03:00"
    )
