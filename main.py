from flask import Flask
import config_run
import telegram

app = Flask(__name__)
app.config.from_pyfile("config_run.py")

#bot = telegram.Bot(token = TOKEN)
@app.route ("/")
def hello_func():
  return "Hello gay"


if __name__ == "__main__":
  app.run()