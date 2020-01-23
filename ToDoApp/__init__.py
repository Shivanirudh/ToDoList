from flask import Flask
from config import Config

TDapp = Flask(__name__)
TDapp.config.from_object(Config)

from ToDoApp import routes