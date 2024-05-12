# -*- coding: utf-8 -*-
"""Text Generation using LSTM Neural Networks

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hzMXyCqSTLTvV4KI1T987OrvWN17WB_y
"""

import numpy as np
!pip install np_utils
!pip install python-docx
from docx import Document
import sys
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from gensim.models import Word2Vec
from keras.layers import Dense, Dropout, LSTM
from tensorflow.keras import utils
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam

def read_text_from_word(doc_path):

    doc = Document(doc_path)

    text_from_word = ""
    for paragraph in doc.paragraphs:
        text_from_word += paragraph.text + "\n"

    return text_from_word

doc_path_1  = "Dox1"
doc_path_2 = 'Dox2'

text_from_doc1 = read_text_from_word(doc_path_1)

text_from_doc2 = read_text_from_word(doc_path_2)

tokenizer = Tokenizer()
tokenizer.fit_on_texts([text_from_doc1,text_from_doc2])
total_words = len(tokenizer.word_index) + 1

input_sequences = []
for article in [text_from_doc1,text_from_doc2]:
    token_list = tokenizer.texts_to_sequences([article])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

max_sequence_length = max(len(seq) for seq in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')
X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = np.eye(total_words)[y]

# LSTM model
model = Sequential()
model.add(Embedding(input_dim=total_words, output_dim=100, input_length=max_sequence_length-1))
model.add(LSTM(units=256, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=250))
model.add(Dense(units=total_words, activation='softmax'))

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=89, batch_size=128)

# Save the weights
model.save_weights("trained_weights.h5")

seed_text = "Application of AI"  # Initial seed text
generated_text = seed_text
for _ in range(100):
    tokenized_input = tokenizer.texts_to_sequences([seed_text])[0]
    padded_input = pad_sequences([tokenized_input], maxlen=max_sequence_length-1, padding='pre')

    predicted_index = np.argmax(model.predict(padded_input), axis=-1)[0]
    predicted_word = tokenizer.index_word[predicted_index]

    seed_text += " " + predicted_word
    generated_text += " " + predicted_word

print("Generated Content:")
print(generated_text)