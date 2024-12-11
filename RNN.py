import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

file_name = r"C:\Users\.Rayan.Servic.e\Desktop\prediction\data\q.txt"

try:
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read().strip()
    if not text:
        raise ValueError("Error: فایل متنی خالی است یا محتوای مناسبی ندارد.")
except FileNotFoundError:
    print(f"Error: File {file_name} not found.")
    text = ""
except ValueError as e:
    print(e)
    text = ""

if text:
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([text])
    total_words = len(tokenizer.word_index) + 1

    input_sequences = []
    for line in text.split("\n"):
        line = line.strip()
        if line:
            token_list = tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(token_list)):
                input_sequences.append(token_list[:i + 1])

    if not input_sequences:
        raise ValueError("Error: هیچ توالی‌ای تولید نشد. فایل ممکن است نامعتبر باشد.")

    max_sequence_len = max(len(seq) for seq in input_sequences)
    input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

    X = input_sequences[:, :-1]
    y = input_sequences[:, -1]
    y = tf.keras.utils.to_categorical(y, num_classes=total_words)

    embedding_dim = 100
    model = Sequential([
        Embedding(input_dim=total_words, output_dim=embedding_dim),
        LSTM(150, return_sequences=True),
        LSTM(100),
        Dense(100, activation='relu'),
        Dense(total_words, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    num_epochs = 3
    history = model.fit(X, y, epochs=num_epochs, verbose=1)

    def generate_text(seed_text, next_words, max_sequence_len):
        for _ in range(next_words):
            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
            predicted_index = np.argmax(model.predict(token_list, verbose=0))
            output_word = tokenizer.index_word.get(predicted_index, "")
            seed_text += " " + output_word
        return seed_text

    seed_text = "گفت تو خوب می خوانی و می نویسی و اینک بگو چه میخواهی بشوی؟"
    next_words = 5
    generated_text = generate_text(seed_text, next_words, max_sequence_len)
    print(generated_text)
else:
    print("برنامه به پایان رسید. متن مناسبی برای پردازش یافت نشد.")