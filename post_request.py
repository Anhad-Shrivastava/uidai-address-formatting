import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
from flask import jsonify


if __name__=='__main__':

    url = "http://127.0.0.1:8000/output"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    data = pd.io.json.read_json('Address_data.json').to_json()
    resp = requests.post(url, headers=headers, json=data)
    pd.read_json(resp.json()).to_csv('formatted address.csv',index=0)

    print(resp.status_code)