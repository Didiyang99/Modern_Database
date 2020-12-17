from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from neo4j import GraphDatabase

"""
Set up Mongo client
Connect it to the MongoDB Books collection  
"""
client = MongoClient('localhost',27017)
db = client['finalProjectDb']
books = db.Books  

"""
Set up Neo4j Client usingn Neo4j Driver 
Connect it to localhost:7687 as default database
"""
#driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "moderndb"))
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Elhadi123"))

app = Flask(__name__)

#Home page route
@app.route("/")
def index():
    return render_template('index.html')

"""
Search route to search books in database
This function searches the input parsed from query and used MongoDB query syntax to look through database
For the matching results, append all the results to a list
If results exist, then call render_template() and render results in results.html which displays in user's browser
If result not exist,call render_template() and render invalid message in index.html 
"""
@app.route("/search",methods=['GET'])
def search():
    query = request.args.get('query')
    records = []
    query = capString(query)
    resultOne = books.find_one({"original_title": query},{'original_title':1,'book_id':1, 'id':1, 'authors':1,'original_publication_year':1,
                        'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0})
    #insert most matching input
    if resultOne:
        records.append(resultOne)
    for result in books.find({"$text": {"$search" : query}},{'original_title':1,'book_id':1,'id':1,'authors':1,'original_publication_year':1,
                            'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0}):      
        #If result matched the query we want to find, append it to a list
        if result:
            records.append(result)
    if records:
        return render_template("results.html",records=records, query=query)

    else:
        return render_template('index.html',invalid="Book Does Not Exist")



"""
This function takes firstbook ID as input, and call function getBookSuggestions() to get the suggested book IDs
Executate a Mongo query search all the bookIDs
It calls tender_template() and renders books as a recommendation book lists to recommendational.html page
"""
@app.route("/recommend/<int:firstBook>",methods=['GET'])
def recommend(firstBook):
    status = "fail"
    get_query_book = books.find_one({'id':firstBook},{'original_title':1, '_id':0})
    bookname = "failed_request"
    if get_query_book:
        bookname = get_query_book['original_title']

    bookIDs = getBookSuggesstions(firstBook)
    records = []
    for book in bookIDs:
        result = books.find_one({'id':book},{'original_title':1,'book_id':1,'id':1, 'authors':1,'original_publication_year':1,
                            'small_image_url':1, 'average_rating':1,'isbn':1, 'ratings_count':1, '_id':0})
        if result:
            records.append(result)
<<<<<<< HEAD
    if records:
        status = "success"
    
    return render_template('recommendation.html',records=records,bookname=bookname,status=status)
=======
    return render_template('recommendation.html',records=records)
>>>>>>> 48c1259a6556b560004b02915957230714f52bdc



"""
This functions takes firstbook as input
It uses Neo4j cypher query to obtain cosine similarity between the first book returned in the search route
Cypher query returns the top 5 most similary booksID and similarity number based on the input
This function returns a list of results which contains the similary neighbor retruend from Neo4j query 
"""
def getBookSuggesstions(firstbook):
    results_as_list_neighbor = []
    results_as_list_Sim =[]
    session = driver.session()
    result = session.run("MATCH (b1:Book{bookId:$firstbook})-[s:SIMILARITY]-(b2:Book) "\
            "WITH b2, s.similarity AS sim "\
            "ORDER BY sim DESC "\
            "LIMIT 5 "\
            "RETURN b2.bookId AS Neighbor, sim AS Similarity",firstbook=firstbook)
    for record in list(result):
        results_as_list_neighbor.append(record['Neighbor'])
        results_as_list_Sim.append(record['Similarity'])
    return results_as_list_neighbor


# Match string to format in databse
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

