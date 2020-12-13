# Modern_Database
Class Project
To run this, go to terminal and type "npm start" 
And go to localhost:3000

Data Import:
To import books.csv table:
mongoimport --type csv -d finalProjectDB -c Books --headerline --drop --file ~/Downloads/books.csv

This will import the data to finalProjectDB database in the Books collection. Given that your books.csv file is under your Downloads directory. 
