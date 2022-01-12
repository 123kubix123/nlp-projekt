import json
import pandas as pd
import feature_extraction
import nltk

MIN_POS_IN_CORPUS = 100
MIN_NER_IN_CORPUS = 20

with open('products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df = df.drop(columns=['url', 'desc'])

df['rating'] = df['rating'].str.replace(',', '.').astype(int)
df['rating_count'] = df['rating_count'].str.replace(',', '').astype(int)
df['photos_count'] = df['photos_count'].str.replace(',', '').astype(int)

text_columns = ['desc_text', 'title']
corpus = '\n'.join(df.loc[~df['desc_text'].isnull(), 'desc_text']) + '\n' +\
    '\n'.join(df.loc[~df['title'].isnull(), 'title'])
    
#tokens = nltk.word_tokenize(corpus)
#unigram_freq = feature_extraction.get_frequency_from_tokens(tokens)
#bigram_freq = feature_extraction.get_frequency_from_tokens(nltk.bigrams(tokens))
#trigram_freq = feature_extraction.get_frequency_from_tokens(nltk.trigrams(tokens))

l = []
for col in text_columns:
    df.loc[df[col].isnull(), col] = ''
    features = df[col].apply(feature_extraction.get_main_stats).apply(pd.Series)
    features = features.astype(float)
    n_columns = len(features.columns)
    print(f'Got {n_columns} features columns')
    features = features.loc[:, features.std() != 0.0]
    print(f'Dropped {n_columns - len(features.columns)} features columns')
    
    ratios = features.apply(
        feature_extraction.get_ratios,
        axis=1,
        columns=['n_characters', 'n_words', 'n_punctuations', 'n_sentences', 'n_paragraphs']
        ).apply(pd.Series)
    ratios.columns = [col + '_' + colname for colname in ratios.columns]
    features.columns = [col + '_' + colname for colname in features.columns]
    
    pos_features = df[col].apply(feature_extraction.get_pos_features).apply(pd.Series)
    pos_features = pos_features.fillna(0)
    n_columns = len(pos_features.columns)
    print(f'Got {n_columns} POS features columns')
    pos_features = pos_features.loc[:, pos_features.sum(axis=0) > MIN_POS_IN_CORPUS]
    print(f'Dropped {n_columns - len(pos_features.columns)} POS features columns')
    pos_features.columns = [col + '_' + colname for colname in pos_features.columns]
    
    ner_tags = df[col].apply(feature_extraction.get_ner_tag_counts).apply(pd.Series)
    ner_tags = ner_tags.fillna(0)
    n_columns = len(ner_tags.columns)
    print(f'Got {n_columns} NER features columns')
    ner_tags = ner_tags.loc[:, ner_tags.sum(axis=0) > MIN_NER_IN_CORPUS]
    print(f'Dropped {n_columns - len(ner_tags.columns)} NER features columns')
    ner_tags.columns = [col + '_' + colname for colname in ner_tags.columns]
    
    l.append(features)
    l.append(ratios)
    l.append(pos_features)
    l.append(ner_tags)
    
dataset = pd.concat([df, *l], axis=1)
dataset = dataset.drop(columns=text_columns)
dataset.to_csv('dataset.csv', index=0)
