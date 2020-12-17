from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from neo4j import GraphDatabase


#Mongo Client
client = MongoClient('localhost',27017)
db = client['finalProjectDb']
books = db.Books  

#Neo4j Client
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Elhadi123"))

app = Flask(__name__)



#home page route
@app.route("/")
def index():
    return render_template('index.html')

#search route to search books in db
@app.route("/search",methods=['GET'])
def search():
    query = request.args.get('query')
    records = []
    query = capString(query)
    print(query)

    resultOne = books.find_one({"original_title": query},{'original_title':1,'book_id':1, 'id':1, 'authors':1,'original_publication_year':1,
                           'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0})
    #insert most matching input
    if resultOne:
        records.append(resultOne)

    for result in books.find({"$text": {"$search" : query}},{'original_title':1,'book_id':1,'id':1,'authors':1,'original_publication_year':1,
                            'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0}):
        
        #If this is the same object we inserted in line 34, do not insert again.
        if result:
            records.append(result)

    if records:
        return render_template("results.html",records=records, query=query)

    else:
        return render_template('index.html',invalid="Book Does Not Exist")


#Recommendation
@app.route("/recommend/<int:firstBook>",methods=['GET'])
def recommend(firstBook):
    bookIDs = getBookSuggesstions(firstBook)
    # result = books.find_one({'id':598},{'original_title':1,'book_id':1, 'authors':1,'original_publication_year':1,
    #                          'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0})
    # print(result)
    
    # return render_template('recommendation.html',records=result)
    records = []
    for book in bookIDs:
        result = books.find_one({'id':book},{'original_title':1,'book_id':1,'id':1, 'authors':1,'original_publication_year':1,
                            'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0})
        if result:
            records.append(result)
    print("records", records)
    return render_template('recommendation.html',records=records)

    

# Make a list of Neo4j results
def makeList(self, results,attribute='Neighbor'):
    results_as_list = []
    if results.peek():            
        listResult = list(results)
        for record in listResult:
            results_as_list.append(record[attribute])
    return results_as_list  

#Uses neo4j to obtain similarity between the first book returned in the search route. Uses cosine simialrity.
def getBookSuggesstions(firstbook):
    results_as_list_neighbor = []
    results_as_list_Sim =[]
    session = driver.session()
    print('firstbook', firstbook)
    result = session.run("MATCH (b1:Book{bookId:$firstbook})-[s:SIMILARITY]-(b2:Book) "\
            "WITH b2, s.similarity AS sim "\
            "ORDER BY sim DESC "\
            "LIMIT 5 "\
            "RETURN b2.bookId AS Neighbor, sim AS Similarity",firstbook=firstbook)
    for record in list(result):
        results_as_list_neighbor.append(record['Neighbor'])
        results_as_list_Sim.append(record['Similarity'])
        print(str(record['Neighbor'])+"      "+ str(record['Similarity']))
    print(results_as_list_neighbor)
    print(results_as_list_Sim) 
    return results_as_list_neighbor


#match string to format in databse
def capString(s):    
    no_caps_list = []
    if s.split()[0] == "to":
        no_caps_list = ["and","of","is","a", "an"]
    elif s.split()[0] == "a":
        no_caps_list = ["and","of","is", "an"]
    elif s.split()[0] == "an":
        no_caps_list = ["and","of","is", "a"]
    else:
        no_caps_list = ["and","to","of","is", "a","an"]
    lst = s.split()   
    res = ''     
    for word in lst:
        if word not in no_caps_list:
            word = word.capitalize()
        res = res + ' '+ word
    return res.strip()


if __name__ == "__main__":
    app.run(debug=True)

