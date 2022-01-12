'use strict';

const fs = require('fs');

let rawdata = fs.readFileSync('products_partial.json');
let products = JSON.parse(rawdata);

function arrUnique(arr) {
    var cleaned = [];
    for (var i = 0, l = arr.length; i < l; i++) {
        var unique = true;
        for (var j = 0, k = cleaned.length; j < k; j++) {
            if ((arr[i].url === cleaned[j].url)) {
                unique = false;
            }
        }
        if (unique) {
            cleaned.push(arr[i]);
        }
    }
    return cleaned;
}

var products_deduped = arrUnique(products);

let data = JSON.stringify(products_deduped);
fs.writeFileSync('products_partial_deduped.json', data);