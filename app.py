from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
client = MongoClient('mongodb+srv://test:sparta@cluster0.znplsth.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/youtube", methods=["POST"])
def game_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title':title,
        'image':image,
        'desc':desc,
        'star':star_receive,
        'comment':comment_receive
    }
    db.youtube.insert_one(doc)

    return jsonify({'msg':'게임 추천 완료!'})

@app.route("/youtube", methods=["GET"])
def youtube_get():
    youtube_list = list(db.youtube.find({}, {'_id':False}))
    return jsonify({'youtube': youtube_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)