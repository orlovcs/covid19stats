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

from models import Data, Infections

dt = Data()

def run_query(query):
   return pd.read_sql(query, con=engine)

@app.route("/")
def hello():

    us_infections_monthly = dt.get_monthly_totals(dt.get_us_infections())
    us_infections_monthly_html = dt.df_to_html(us_infections_monthly)

    return render_template('bootstrapbare/index.html', us_infections_monthly_html = us_infections_monthly_html )

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
