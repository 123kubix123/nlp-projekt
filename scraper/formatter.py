import re
import json



with open('products_sample.json') as json_file:
    data = json.load(json_file)
    f = open("products_reparsed.json", "a")
    f.write('[')
    # Print the type of data variable
    for i in range(0,len(data)):
        desc_text = data[i]['desc']
        if desc_text:
            
            #desc_text = re.sub(r'<style type=\"text/css\">.*?/style>','', desc_text)
            #desc_text = re.sub(r'<style>.*?</style>','', desc_text)
            #desc_text = re.sub(r'<style.*?/style>','', desc_text)
            desc_text = re.sub(re.compile('<style.*?/ *?style>', re.DOTALL),'', desc_text)
            desc_text = re.sub(re.compile('< *?script(?:.*?)< *?/ *?script>', re.DOTALL),'', desc_text)
            desc_text = re.sub(r'<br>|<br\/>|<br \/>','\r\n', desc_text)
            desc_text = re.sub(r'<.*?>',' ', desc_text)
            desc_text = re.sub(r'\\t','', desc_text)
            desc_text = re.sub(r'\t','', desc_text)
            desc_text = re.sub(r'(?: *\\n){2,}',' \r\n', desc_text)
            desc_text = re.sub(r'(?: *\n){2,}',' \r\n', desc_text)            
            desc_text = re.sub(r'(?: *\r\n){2,}',' \r\n', desc_text)
            desc_text = re.sub(r'(?: *\\r\\n){2,}',' \r\n', desc_text)
            desc_text = re.sub(r' {2,}',' ', desc_text)
            data[i]['desc_text'] = desc_text
            if desc_text and desc_text != ' ':
                
                json.dump(data[i], f)
                f.write(',\n')
                
    f.write(']')
    f.close()