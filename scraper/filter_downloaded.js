'use strict';

const fs = require('fs');

let rawdata = fs.readFileSync('products_full.json');
let products = JSON.parse(rawdata);


var cleaned = [];
for (var i = 0; i < products.length; i++) {
    if(products[i].desc){
        cleaned.push(products[i]);
    }
}


let ready = JSON.stringify(cleaned);

fs.writeFileSync('products_more.json', ready);