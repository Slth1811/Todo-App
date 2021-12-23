from flask import Flask, render_template, request, redirect
from model import *
from uuid import uuid4
from pprint import pprint

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    pprint(Card.get_all())
    return render_template('index.html', cards = Card.get_all())

@app.route('/card/new',methods=['POST'])
def add_card():
    name = request.form.get('cardName')
    card_id = str(uuid4())
    Card.create(id=card_id, name=name).save()
    return redirect('/')

@app.route('/item/new',methods=['POST'])
def add_item():
    form = request.form
    card_id = form.get('card_id')
    name = form.get('name')
    Item.create(card=card_id, name=name).save()
    return redirect('/')

@app.route('/item/check',methods=['POST'])
def check_item():
    form = request.form
    item_id = form.get('item_id')
    status = bool(form.get('status',type=int)) #bool(0) = False
    Item.update({Item.completed: status}).where(Item.id == item_id).execute()
    return redirect('/')

if __name__ == '__main__':
    db.connect()
    db.create_tables([Card,Item])
    app.run('localhost',port=5000)