# Modern_Database
# Class Project
To run this, go to the UsingPython directory, and run "Python3 app.py"
This will direct you to localhost:5000

# Data Import:
To import books.csv table MongoDB:
mongoimport --type csv -d finalProjectDb -c Books --headerline --drop --file ~/Downloads/book.csv
This will import the data to finalProjectDB database in the Books collection. Given that your books.csv file is under your Downloads directory. 

# Create mongodb index:
After creating the database, add text index on Books collections using:
db.Books.createIndex({ "original_title": "text"})

# To import ratings.csv table to Neo4j:
auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM"file:///ratings.csv" AS row                                                                 
MERGE (m:User {userId: toInteger(row.user_id)})
WITH m, row
MERGE (n:Book{bookId:toInteger(row.book_id)})
WITH m, row, n
MERGE (m)-[r:RATED{rating:tofloat(row.rating)}]->(n);

# To create a similarity relationship in Neo4j:
MATCH (b1:Book)<-[x:RATED]-(u:User)-[y:RATED]->(b2:Book) WITH SUM(x.rating * y.rating) AS xyDotproduct,
SQRT(REDUCE(xDot = 0.0, a IN COLLECT(x.rating) | xDot + a^2)) AS xLength,
SQRT(REDUCE(yDot = 0.0, b IN COLLECT(y.rating) | yDot + b^2)) AS yLength,
b1, b2
MERGE (b1)-[s:SIMILARITY]-(b2)
SET s.similarity = xyDotproduct / (xLength * yLength) 
