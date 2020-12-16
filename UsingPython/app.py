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
    result = books.find_one({'original_title':query}) 
    if result and len(query) is not 0:
        resultSet = {'Title':result['original_title'], 'Author':result['authors'], 'Ratings_Count':result['ratings_count'], 'Published':int(result['original_publication_year']), 'Image':result['small_image_url'],
                    'Avg_Rating':result['average_rating'], 'ISBN':result['isbn']}
        return render_template("results.html",resultSet=resultSet)
    else:
        return render_template('index.html',invalid="Book Does Not Exist")
    # return redirect(url_for('results',query=query))
    











if __name__ == "__main__":
    app.run(debug=True)
