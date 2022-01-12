'use strict';

const fs = require('fs');

let rawdata = fs.readFileSync('products_sample.json');
let products = JSON.parse(rawdata);
var prod_fin = []
for (var i = 0; i < products.length; i++) {
    
    if(products[i].desc){
    var desc_text = products[i].desc
            desc_text = desc_text.replace(/<style.*?\/ *?style>/gms , '')
            desc_text = desc_text.replace(/< *?script(?:.*?)< *?\/ *?script>/gsm,'')
            desc_text = desc_text.replace(/<br>|<br\/>|<br \/>/gm,'\r\n')
            desc_text = desc_text.replace(/<.*?>/gm,' ')
            desc_text = desc_text.replace(/\\t/gm,'')
            desc_text = desc_text.replace(/\t/gm,'')
            desc_text = desc_text.replace(/(?: *\\n){2,}/gm,' \r\n')
            desc_text = desc_text.replace(/(?: *\n){2,}/gm,' \r\n')
            desc_text = desc_text.replace(/(?: *\r\n){2,}/gm,' \r\n')
            desc_text = desc_text.replace(/(?: *\\r\\n){2,}/gm,' \r\n')
            desc_text = desc_text.replace(/ {2,}/gm,' ')
            products[i].desc_text = desc_text
            prod_fin.push(products[i])
}
}

let data = JSON.stringify(prod_fin);
fs.writeFileSync('products_reparsed.json', data);