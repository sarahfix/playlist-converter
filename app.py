from flask import Flask, request, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_url = request.form.get('playlist_url')
        return f"Received playlist: {playlist_url}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
