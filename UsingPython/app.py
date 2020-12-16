from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

#Mongo Client
client = MongoClient('localhost',27017)
db = client['finalProjectDb']
books = db.Books  

app = Flask(__name__)



#home page route
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search",methods=['GET'])
def search():
    query = request.args.get('query')
    records = []
    for result in books.find({"$text": {"$search" : query}},{'original_title':1,'authors':1,'original_publication_year':1,
                            'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0}).limit(3):
        records.append(result)

    if records:
        return render_template("results.html",records=records)

    else:
        return render_template('index.html',invalid="Book Does Not Exist")
    


if __name__ == "__main__":
    app.run(debug=True)