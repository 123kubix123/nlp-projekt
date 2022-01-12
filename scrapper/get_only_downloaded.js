'use strict';

const fs = require('fs');

let rawdata = fs.readFileSync('products_partial_deduped.json');
let products = JSON.parse(rawdata);

let prod_down = fs.readFileSync('products_more.json');
let products_downloaded = JSON.parse(prod_down);


    var cleaned = [];
    for (var i = 0; i < products.length; i++) {
        var unique = true;
        for (var j = 0; j < products_downloaded.length; j++) {
            if ((products[i].url === products_downloaded[j].url)) {
                unique = false;
            }
        }
        if (unique) {
            cleaned.push(products[i]);
        }
    }


let data = JSON.stringify(cleaned);
fs.writeFileSync('products_partial_to_down.json', data);