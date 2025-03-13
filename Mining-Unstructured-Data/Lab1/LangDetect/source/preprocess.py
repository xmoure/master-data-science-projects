import nltk
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
import pandas as pd
import itertools
import string
nltk.download('stopwords')



# Get stop words for the languages obtained from the parameter label
def get_stop_words(labels):
    available_stop_words_nltk = stopwords.fileids()
    different_labels = labels.unique().tolist()
    languages = [lang for lang in different_labels if lang.lower() in available_stop_words_nltk]
    stop_words = list(set([word.lower() for lang in languages for word in stopwords.words(lang)]))
    return stop_words

# remove stop words
def remove_stop_words(sentence, labels):
    stop_words = get_stop_words(labels)
    tokens = nltk.word_tokenize(sentence)
    filtered = [w for w in tokens if not w in stop_words]
    filtered = " ".join(filtered)
    return filtered
# Keep in mind that sentence splitting affects the number of sentences
# and therefore, you should replicate labels to match.
def split_sentences(sentences, labels):
    result_sentences = list(itertools.chain.from_iterable(nltk.sent_tokenize(text) for text in sentences))
    result_labels = [label for text_sentences, label in zip(sentences, labels) for _ in range(len(nltk.sent_tokenize(text_sentences)))]
    return result_sentences, result_labels

def remove_numbers_symbols(text):
    table = str.maketrans('', '', string.punctuation + string.digits)
    return text.translate(table)

#Tokenizer function. You can add here different preprocesses.
def preprocess(sentence, labels, stopwords=True, stemming=True, punkt_token= True, split_sentence= True, remove_symbols=True ):
    if split_sentence == 'True':
        sentence,labels = split_sentences(sentence, labels)

    texts_results = []
    # remove punctuation
    for text in sentence:
        # we don't need to lower case because CountVectorizer already does it by default
        if remove_symbols == 'True':
            text = remove_numbers_symbols(text)
        if stopwords == 'True':
            text = remove_stop_words(text, labels)
        if stemming == 'True':
            stemmer = nltk.stem.PorterStemmer()
            tokens =  nltk.tokenize.word_tokenize(text)
            tokens = [stemmer.stem(token) for token in tokens]
            text = " ".join(tokens)
        if punkt_token == 'True':
            tokenizer = PunktSentenceTokenizer()
            tok_sentences = tokenizer.tokenize(text)
            tokens = []
            for s in tok_sentences:
                tokens = nltk.word_tokenize(s, preserve_line = True)
            text = " ".join(tokens)
        result = text
        texts_results.append(result)
    sentence = pd.Series(texts_results)
    return sentence,labels



