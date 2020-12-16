from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from neo4j import GraphDatabase

#Mongo Client
client = MongoClient('localhost',27017)
db = client['finalProjectDb']
books = db.Books  

#Neo4j Client
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "moderndb"))

app = Flask(__name__)



#home page route
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search",methods=['GET'])
def search():
    query = request.args.get('query')
    records = []
    resultOne = books.find_one({"$text": {"$search" : '\"query\"'}},{'original_title':1,'book_id':1, 'authors':1,'original_publication_year':1,
                            'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0})
    for result in books.find({"$text": {"$search" : query}},{'original_title':1,'book_id':1,'authors':1,'original_publication_year':1,
                            'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0}):
        records.append(result)

    if records:
        return render_template("results.html",records=records, query=query)

    else:
        return render_template('index.html',invalid="Book Does Not Exist")
    

# Make a list of Neo4j results
def makeList(self, results):
    results_as_list = []
    if results.peek():            
        listResult = list(results)
        for record in listResult:
            results_as_list.append(record)
    return results_as_list  

#Use cosine similarity to create a book recommendation algorithms between two books based on rating from the same user
def createBookSuggesstions():
    session = driver.session()
    query = "MATCH (b1:Book)<-[x:RATED]-(u:User)-[y:RATED]->(b2:Book) WITH SUM(x.rating * y.rating) AS xyDotproduct, " \
        "SQRT(REDUCE(xDot = 0.0, a IN COLLECT(x.rating) | xDot + a^2)) AS xLength, "\
        "SQRT(REDUCE(yDot = 0.0, b IN COLLECT(y.rating) | yDot + b^2)) AS yLength, "\
        "b1, b2"\
        "MERGE (b1)-[s:SIMILARITY]-(b2) "\
        "SET s.similarity = xyDotproduct / (xLength * yLength) "
    session.close()
    return 


# def getBookSuggesstions():
#     session = driver.session()
#     query = "MATCH (b1:Book{bookId:900})-[s:SIMILARITY]-(b2:Book) "\
#              "WITH b2, s.similarity AS sim "\ 
#              "ORDER BY sim DESC" \ 
#               "LIMIT 30" \
#                "RETURN b2.bookId AS Neighbor, sim AS Similarity"
#     result = session.run(query,ID=?)
#     response = makeList(result) 
#     session.close()
#     return response 

if __name__ == "__main__":
    app.run(debug=True)