import urllib.request
from collections import defaultdict
import matplotlib.pyplot as plt
from multiprocessing import Pool

def fetch_text(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

# Виконання MapReduce
def map_reduce(text):
    # Крок 1: Мапінг
    mapped_values = map_function(text)

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values

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
    url = "https://en.wikipedia.org/wiki/Laurence_Waddell"
    
    # Завантажуємо текст
    text = fetch_text(url)
    
    # Підрахунок частоти слів за допомогою MapReduce
    word_counts = map_reduce(text)
    
    # Візуалізація результатів
    visualize_top_words(word_counts)

if __name__ == "__main__":
    main()