from flask import Flask, render_template
from threading import Thread

app = Flask("")

@app.route("/")
def main():
  return """
<!DOCTYPE html>
<html>
    <head>
        <title>Matchy is activated</title>
        <style type="text/css">body {background-color:#000; color:#fff;}</style>
    </head>
    <body>
        <h1>Matchy is activated!</h1>
        <p>You can now close this page.</p>
    </body>
</html>
"""

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()