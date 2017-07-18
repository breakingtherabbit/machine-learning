# -*- coding: utf-8 -*-

# functions
def adjs(lista):
    lista = lista.lower()
    lista = re.sub(u"[^a-zA-Z]", ' ', lista)
    aux = nltk.word_tokenize(lista)
    aux = nltk.pos_tag(aux)
    aux = [i[0] for i in aux if(i[0] not in stop)]
    return aux

def adjectives(reviewL, sentimentL, sentiment):
    list_aux = []
    for i in range(len(reviewL)):
        if(sentimentL[i]==sentiment):
            list_aux = list_aux + adjs(reviewL[i])
        if(sentiment==0):
            list_aux = list_aux + adjs(reviewL[i])
    return list_aux
    
def pxi_y(lista, palavra):
    words = 0
    for i in lista:
        if palavra in i:
            words = words + 1
    prob = words/float(len(lista))
    if(prob==0):
        return 0.01
    elif(prob==1):
        return 0.09
    return prob
    
def py(smntL, sentiment):
    aux = smntL.count(sentiment)
    return aux/float(len(smntL))
    
def argmax(reviewsL, smntL, newReview):
    y = 0
    k = 1
    j = 0
    classe = 0
    while(k<4):
        prod = 0
        aux = py(smntL,k)
        for i in newReview:
            if(j!=0):
                prod = prod * pxi_y(reviewsL[k-1], i)
            else:
                prod = pxi_y(reviewsL[k-1], i)
        yaux = aux*prod
        if(yaux>y):
            y = yaux
            classe = k
        k = k + 1
    return classe

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        csv_list = list(reader)
    f.close()
    return csv_list
    
def getSentiments(csv_list):
    reviews_aux = []
    sentiments_aux = []
    k = 0
    for i in range(len(csv_list)):
        aux = csv_list[i][len(csv_list[i])-6]
        if(len(aux)==1):
            reviews_aux.append(' '.join(csv_list[i][2:-6]))
            sentiments_aux.append(int(aux))
            k = k + 1
    return reviews_aux, sentiments_aux
    
# magica
import nltk, csv, re
from nltk.corpus import stopwords

# lendo o arquivo csv e passando para uma list
filename = "chennai_reviews1.csv"
print("Treinamento... (" + filename + ")")
csv_list = read_csv(filename)
reviews, sentiments = getSentiments(csv_list)

# pegando as stopwords do ingles
stop = set(stopwords.words('english'))

# pegando apenas os adjetivos nos reviews
reviewsL = []
reviewsL.append(adjectives(reviews, sentiments, 1))
reviewsL.append(adjectives(reviews, sentiments, 2))
reviewsL.append(adjectives(reviews, sentiments, 3))

filename2 = "chennai_reviews2.csv"
print("Testando... (" + filename2 + ")")
csv_list2 = read_csv(filename2)

hits = 0
newReviews, newSentiments = getSentiments(csv_list2)
newReviews = adjectives(newReviews, newSentiments, 0)
tam = len(newSentiments)
for i in range(tam):
    y = argmax(reviewsL, sentiments, newReviews[i])
    if(y==newSentiments[i]):
        hits = hits + 1
        
print("Taxa de acerto:" + str(hits/float(tam)))