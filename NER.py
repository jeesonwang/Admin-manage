import pandas as pd
from keras.utils import pad_sequences
import numpy as np
from keras.layers import Input,Embedding,concatenate,Bidirectional,LSTM
from keras_contrib.layers import CRF
from keras import Model
 
df=pd.read_table('train.txt',encoding='utf8',header=None)
df=df.fillna('\n')
df=df.values.tolist()
data=[]
temp=[]
for i in range(len(df)):
    if df[i][0]!='\n':
        temp.append(df[i])
    else:
        data.append(temp)
        temp=[]
        i=i+1
maxlen = max(len(s) for s in data)
vocab1=list(set([j[0] for i in data for j in i]))
word_idx1 = dict((w, i+2) for i, w in enumerate(vocab1))#分词的词典
x1 = [[word_idx1.get(w[0], 1) for w in s] for s in data] # 转化为整数，字典中没有的词设置为1   dict.get(key, default=None)
x1 = pad_sequences(x1, maxlen)#特征1
vocab2=list(set([j[1] for i in data for j in i]))
word_idx2 = dict((w, i+2) for i, w in enumerate(vocab2))#词性的词典
x2 = [[word_idx2.get(w[1], 1) for w in s] for s in data]
x2 = pad_sequences(x2, maxlen)#特征2
x1=np.array(x1)
x2=np.array(x2)
y_vocab=list(set([j[2] for i in data for j in i]))
y2idx = dict((w, i+2) for i, w in enumerate(y_vocab))#标签的词典
y = [[y2idx.get(w[2], 1) for w in s] for s in data]
y = pad_sequences(y, maxlen)
y = np.expand_dims(y, 2)
word_input = Input(shape=(maxlen,), dtype='int32')
pos_input = Input(shape=(maxlen,), dtype='int32')
word_embedding_layer = Embedding(len(vocab1)+2,32,input_length=maxlen)(word_input)
pos_embedding_layer = Embedding(len(vocab2)+2,10,input_length=maxlen)(pos_input)
emb= concatenate([word_embedding_layer, pos_embedding_layer], axis=-1) #融合层
lstm = Bidirectional(LSTM(64, return_sequences=True))(emb)
crf = CRF(len(y_vocab)+2, sparse_target=True)  #CRF层
out = crf(lstm)
model = Model([word_input, pos_input], out)
model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])
model.fit([x1,x2], y,batch_size=16,epochs=5,verbose=2,validation_split=0.2)
# model.save('./model/mymodel')
#print(y[:10])
#print(np.argmax(model.predict([x1[:10],x2[:10]]), axis=-1))