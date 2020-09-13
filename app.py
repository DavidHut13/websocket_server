from flask import Flask
from server import start_server,create_room


app = Flask(__name__)


@app.route("/")
def hello_world():
    return 'Room Created'

def start_app():
    app.run()



if __name__ == "__main__":
    app.run()
