from flask import Flask
import config_run
import telebot

app = Flask()
app.config.from_pyfile("config_run.py")



if __name__ == "__main__":
  app.run()