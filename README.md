# Modern_Database
Class Project
TO run this, go to the UsingPython directory, and run "Python3 app.py"
This will direct you to localhost:5000

Data Import:
To import books.csv table:
mongoimport --type csv -d finalProjectDb -c Books --headerline --drop --file ~/Downloads/book.csv
This will import the data to finalProjectDB database in the Books collection. Given that your books.csv file is under your Downloads directory. 

Create index:
After creating the database, add text index on Books collections using:
db.Books.createIndex({ "original_title": "text"})