from types import SimpleNamespace
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import pandas as pd
from io import StringIO

api_token = ' no token'
headers = {"Authorization": f"Bearer {api_token}"}
_transport = RequestsHTTPTransport(url='no url', use_json=True, headers=headers)
client = Client(transport=_transport, fetch_schema_from_transport=True,)
query = gql(""" query {users(super_admin: true){entities{id super_admin username}}}""")
result = client.execute(query)

json_object = json.dumps(result) 
datal = json.loads(json_object, object_hook=lambda d: SimpleNamespace(**d))
workbook = ",,\n" 

users = datal.users.entities

for user in users:
    tempRow = ""
    tempRow = user.id + "," + "\"" + str(user.super_admin) + "\"" + "," + str(user.username)
    workbook = workbook + tempRow + "\n"

dat = StringIO(workbook)
print(workbook)
df = pd.read_csv(dat)
df.columns = ["ID", "Super Admin","Username"]
df.to_csv('~\Documents\\test.csv', index=False, header=True)
