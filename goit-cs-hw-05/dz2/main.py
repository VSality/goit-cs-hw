import string
import urllib.request
from collections import defaultdict
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import re

def fetch_text(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    # Розбиваємо текст на слова
    words = re.findall(r'\b\w+\b', text.lower())

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    top_words = sorted_words[:top_n]
    
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top {} Words by Frequency'.format(top_n))
    plt.show()


def main():
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    
    # Завантажуємо текст
    text = fetch_text(url)
    search_words = ['war', 'peace', 'love']
    # Підрахунок частоти слів за допомогою MapReduce
    word_counts = map_reduce(text, search_words)
    
    # Візуалізація результатів
    visualize_top_words(word_counts)

if __name__ == "__main__":
    main()