import threading
import time
from queue import Queue
import os
from math import ceil

# Функція для пошуку ключових слів у файлі з буферизацією
def find_keywords_in_file(filename, keywords, queue, buffer_size=1024):
    try:
        # Відкриваємо файл з буферизацією
        with open(filename, 'r', encoding='utf-8') as file:
            while True:
                content = file.read(buffer_size)
                if not content:
                    break
                for keyword in keywords:
                    if keyword in content:
                        queue.put((filename, keyword))
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено!")

# Функція для багатопотокової обробки з обмеженням на кількість одночасних потоків
def multithreading_search_with_limited_threads(file_list, keywords, max_threads=None):
    if max_threads is None:
        max_threads = os.cpu_count()  # Визначаємо кількість процесорних ядер
    
    queue = Queue()
    threads = []
    
    # Ділимо список файлів між потоками
    for i in range(0, len(file_list), max_threads):
        current_files = file_list[i:i + max_threads]
        
        # Стартуємо потоки для кожного файлу в межах поточного пулу
        for filename in current_files:
            thread = threading.Thread(target=find_keywords_in_file, args=(filename, keywords, queue))
            threads.append(thread)
            thread.start()
        
        # Чекаємо на завершення поточного пулу потоків перед початком нових
        for thread in threads:
            thread.join()

    results = []
    while not queue.empty():
        results.append(queue.get())
    
    return results

# Основна частина програми
if __name__ == "__main__":
    file_list = ['file1.txt', 'file2.txt', 'file3.txt']  # Список файлів
    keywords = ['слово1', 'слово2']  # Ключові слова
    
    # Вимірюємо час виконання
    start_time = time.time()
    
    # Обмежена багатопотокова обробка з буферизацією
    results = multithreading_search_with_limited_threads(file_list, keywords)
    
    # Виводимо результати пошуку
    for res in results:
        print(f"Файл {res[0]} містить ключове слово: {res[1]}")
    
    end_time = time.time()
    print(f"Час виконання: {end_time - start_time} секунд")
