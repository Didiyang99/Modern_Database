const express = require('express');
const app = express();

//Routes
app.get('/', (req,res) =>{
    res.send('This is Modern Database Final Project');
});

app.get('/posts', (req,res) =>{
    res.send('This is Modern Database Final Project on posts');
});

