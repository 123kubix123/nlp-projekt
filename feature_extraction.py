import nltk
import re
import string
from collections import Counter
import spacy
import math

nltk.download('averaged_perceptron_tagger', quiet=True)
NER_MODEL = spacy.load('en_core_web_sm')

def get_frequency_from_tokens(tokens, threshold='auto'):
    freq = nltk.FreqDist(tokens)
    n_tokens = sum(freq.values())
    if threshold == 'auto':
        threshold = math.log(n_tokens) / n_tokens

    freq = {key: freq[key]/n_tokens for key in freq.keys()}
    freq = {key: freq[key] for key in freq.keys() if freq[key] > threshold}
    return freq

def get_main_stats(text):
    features = {}
    if text is None:
        return features
    
    sentences = nltk.sent_tokenize(text)
    features['n_sentences'] = len(sentences)
    
    words = nltk.word_tokenize(text)
    features['n_words'] = len(words)
    
    paragraphs = re.split('\n{2,}', text)
    features['n_paragraphs'] = len(paragraphs)
    
    features['n_characters'] = sum([len(word) for word in words])
    
    punctuation_pattern = '[' + string.punctuation + ']'
    punc_escaped = re.sub(punctuation_pattern, '', text)
    features['n_punctuations'] = len(text) - len(punc_escaped)
    
    return features
    
def get_pos_features(text):
    if text is None:
        return {}
    
    words = nltk.word_tokenize(text)
    parts_of_speech = [tag[1] for tag in nltk.pos_tag(words)]
    cnt = Counter(parts_of_speech)
    pos_features = {'n_' + key: val for key, val in zip(cnt.keys(), cnt.values())}

    return pos_features

def get_ner_tag_counts(text):
    if text is None:
        return {}
    
    doc = NER_MODEL(text)
    labels = [entity.label_ for entity in doc.ents]
    cnt = Counter(labels)
    labels_counts = {'n_' + key: val for key, val in zip(cnt.keys(), cnt.values())}
    return labels_counts

def get_ratios(d, columns=None):
    d = d.copy()
    pos_features = {}

    if columns is None:
        columns = d.keys()
    else:
        columns = [col for col in columns if col in d.keys()]
        
    counts = [key for key in reversed(list(columns)) if 'n_' in key]
    visited = set()
    
    for key in columns: 
        keyname = re.sub('^n_', '', key) + '_per_'
        for cnt in counts:
            if cnt == key or cnt in visited:
                continue
            new_key = keyname + re.sub('^n_', '', re.sub('s$', '', cnt))
            if d[cnt] == 0:
                pos_features[new_key] = -1
            else:
                pos_features[new_key] = d[key] / d[cnt]  
        visited.add(key)
    return pos_features

if __name__ == '__main__':
    
    with open('test.txt', 'r') as f:
        text = f.read()
    
    features = get_main_stats(text)
    pos_features = get_pos_features(text)
    features = dict(features, **get_ratios(features))

    ner = get_ner_tag_counts(text)
