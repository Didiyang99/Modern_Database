from pymongo import MongoClient


client = MongoClient('localhost',27017)
db = client['finalProjectDb']
books = db.Books
books_data = books.find_one({'authors':'John Green'})   
print(books_data)


