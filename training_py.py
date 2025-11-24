import random
import json
import pickle
import numpy as np
import re

import nltk
from nltk.stem import WordNetLemmatizer
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense,Dropout
    from tensorflow.keras.optimizers import SGD
except Exception:
    Sequential=None

lemmatizer=WordNetLemmatizer()

with open('intents.json') as json_file:
    intents = json.load(json_file)

#print(intents)

words=[]
classes=[]
documents=[]
ignore_letters=['?','!','.',',']

def tokenize(text):
  try:
    return nltk.word_tokenize(text)
  except Exception:
    return re.findall(r"\w+", str(text).lower())

for intent in intents['intents']:
  for pattern in intent['patterns']:
    word_list=tokenize(pattern)
    words.extend(word_list)
    documents.append((word_list,intent['tag']))
    if intent['tag'] not in classes:
      classes.append(intent['tag'])


words =[lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes=sorted(set(classes))
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))



training=[]
output_empty=[0]*len(classes)

for document in documents:
  bag=[]
  word_patterns=[lemmatizer.lemmatize(w) for w in document[0] if w and w not in ignore_letters]
  for w in words:
    bag.append(1 if w in word_patterns else 0)
  output_row=list(output_empty)
  output_row[classes.index(document[1])]=1
  training.append([bag,output_row])

random.shuffle(training)
train_x=[t[0] for t in training]
train_y=[t[1] for t in training]

if Sequential is not None:
  model=Sequential()
  model.add(Dense(128,input_shape=(len(train_x[0]),),activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(64,activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(len(train_y[0]),activation='softmax'))
  sgd=SGD(learning_rate=0.01,decay=1e-6,momentum=0.9,nesterov=True)
  model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])
  hist = model.fit(np.array(train_x),np.array(train_y),epochs=200,batch_size=5,verbose=1)
  model.save('chatbotmodel.h5', hist)
else:
  vocab=words
  class_docs={c:[] for c in classes}
  for doc, y in zip(train_x,train_y):
    cls=classes[np.argmax(y)]
    class_docs[cls].append(doc)
  priors={}
  cond={}
  totals={}
  V=len(vocab)
  for c in classes:
    priors[c]=len(class_docs[c])/len(train_x)
    counts=np.sum(np.array(class_docs[c]),axis=0)
    totals[c]=int(np.sum(counts))
    probs=(counts+1)/(totals[c]+V)
    cond[c]=probs.tolist()
  pickle.dump({'priors':priors,'cond':cond,'classes':classes,'vocab':vocab,'totals':totals,'V':V},open('nb_model.pkl','wb'))
print('Training Done')