from flask import Flask

app = Flask(__name__)

app.secret_key = "secret_is_not_so_secret"