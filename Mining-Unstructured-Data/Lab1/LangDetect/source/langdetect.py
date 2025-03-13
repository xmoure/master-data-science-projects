import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import random
from utils import *
from classifiers import *
from preprocess import  preprocess
from classifiers import *

seed = 42
random.seed(seed)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", 
                        help="Input data in csv format", type=str)
    parser.add_argument("-v", "--voc_size", 
                        help="Vocabulary size", type=int)
    parser.add_argument("-a", "--analyzer",
                         help="Tokenization level: {word, char}", 
                        type=str, choices=['word','char'])
    parser.add_argument("-c", "--classifier",
                        help="Classifier to use. Default one is NB",
                        type=str, choices=["NB", "SVC", "DT", "MLP", "KN", "RF", "GB", "GNB", "LDA"],
                        default="NB")
    parser.add_argument("-p", "--punktToken",
                        help="Use punkt tokenizer or not. Options are True or False. The default one is False",
                        type=str, choices=["True", "False"],
                        default="False")
    parser.add_argument("-s", "--stemmer",
                        help="Use stemming or not. Options are True or False. The default one is False",
                        type=str, choices=["True", "False"],
                        default="False")
    parser.add_argument("-w", "--stopwords",
                        help="Remove stopwords or not. Options are True or False. The default one is False",
                        type=str, choices=["True", "False"],
                        default="False")
    parser.add_argument("-st", "--splitsentence",
                        help="Split sentence or not. Options are True or False. The default one is False",
                        type=str, choices=["True", "False"],
                        default="False")
    parser.add_argument("-rs", "--removesymbols",
                        help="Remove symbols. Options are True or False. The default one is False",
                        type=str, choices=["True", "False"],
                        default="False")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    raw = pd.read_csv(args.input)
    
    # Languages
    languages = set(raw['language'])
    print('========')
    print('Languages', languages)
    print('========')

    # Split Train and Test sets
    X=raw['Text']
    y=raw['language']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    
    print('========')
    print('Split sizes:')
    print('Train:', len(X_train))
    print('Test:', len(X_test))
    print('========')

    # Preprocess text (Word granularity only)
    if args.analyzer == 'word':
        X_train, y_train = preprocess(X_train,y_train, stopwords=args.stopwords, stemming=args.stemmer, punkt_token= args.punktToken, split_sentence=args.splitsentence, remove_symbols=args.removesymbols )
        X_test, y_test = preprocess(X_test,y_test)

    #Compute text features
    features, X_train_raw, X_test_raw = compute_features(X_train, 
                                                            X_test, 
                                                            analyzer=args.analyzer, 
                                                            max_features=args.voc_size)

    print('========')
    print('Number of tokens in the vocabulary:', len(features))
    print('Coverage: ', compute_coverage(features, X_test.values, analyzer=args.analyzer))
    print('========')


    #Apply Classifier  
    X_train, X_test = normalizeData(X_train_raw, X_test_raw)
    y_predict = applyNaiveBayes(X_train, y_train, X_test)

    if args.classifier == "NB":
        y_predict = applyNaiveBayes(X_train, y_train, X_test)
    if args.classifier == "SVC":
        y_predict = apply_linear_svc(X_train, y_train, X_test)
    if args.classifier == "GNB":
        y_predict = apply_gaussian_nb(X_train, y_train, X_test)
    if args.classifier == "MLP":
        y_predict = apply_multiple_layer_perceptron(X_train, y_train, X_test)
    if args.classifier == "KN":
        y_predict = apply_k_neighbours(X_train, y_train, X_test)
    if args.classifier == "DT":
        y_predict = apply_decision_tree(X_train, y_train, X_test)
    if args.classifier == "RF":
        y_predict = apply_random_forest(X_train, y_train, X_test)
    if args.classifier == "GB":
        y_predict = apply_gradient_boost(X_train, y_train, X_test)
    if args.classifier == "LDA":
        y_predict = apply_lda(X_train, y_train, X_test)

    print('========')
    print('Prediction Results:')    
    plot_F_Scores(y_test, y_predict)
    print('========')
    
    plot_Confusion_Matrix(y_test, y_predict, "Greens") 


    #Plot PCA
    print('========')
    print('PCA and Explained Variance:') 
    plotPCA(X_train, X_test,y_test, languages) 
    print('========')
