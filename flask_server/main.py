from dotenv import load_dotenv
import os
from requests import post
import pandas as pd
import api

# loads environment variable files
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

token = api.get_token(client_id, client_secret)