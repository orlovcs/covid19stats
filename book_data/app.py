import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import time, datetime


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine(os.environ['DATABASE_URL'])

from models import Infections


def run_query(query):
   return pd.read_sql(query, con=engine)

@app.route("/")
def hello():
   
    query = 'SELECT * FROM us_infections;'
    df = run_query(query)
    df11 = df.groupby(['date'])['cases'].sum().reset_index()
    df11['date'] =  pd.to_datetime(df11['date'], format='%Y-%m-%d')

    #df11['date'] = df11['date'].astype(np.int64) // 10**9
    df11['date'] = df11['date'].dt.strftime('%Y/%m/%d')

    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    df12 = df.groupby(['month'])['cases'].sum().reset_index()

    daily_list = df11.values.tolist()
    monthly_list = df12.values.tolist()

    days = [l[0] for l in daily_list]
    numbers = [int(l[1]) for l in daily_list]

    months = [l[0] for l in monthly_list]
    mnumbers = [int(l[1]) for l in monthly_list]

    return render_template('bootstrapbare/index.html', months=months, mnumbers=mnumbers,days=days,numbers=numbers )

@app.route("/get")
def get_all():
    try:
        #inf=Infections.query.all()
        #return  jsonify([e.serialize() for e in inf])
        books_df = run_query('SELECT * FROM us_infections LIMIT 10;')
        return render_template('thanks.html', books = books_df.to_html() )

        

    except Exception as e:
	    return(str(e))


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        return jsonify(Infections.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/add/form",methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name=request.form.get('name')
        author=request.form.get('author')
        published=request.form.get('published')
        try:
          
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

if __name__ == '__main__':
    app.run()