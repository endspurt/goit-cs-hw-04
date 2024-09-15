import threading
import time
from queue import Queue

# Функція для створення тестових файлів
def create_test_files():
    # Створюємо файли з текстовими даними
    with open('file1.txt', 'w', encoding='utf-8') as f:
        f.write('Це тестовий файл із ключовим словом слово1.\n')

    with open('file2.txt', 'w', encoding='utf-8') as f:
        f.write('Тут знаходиться ключове слово слово2.\n')

    with open('file3.txt', 'w', encoding='utf-8') as f:
        f.write('У цьому файлі є два ключові слова: слово1 і слово2.\n')

# Функція для пошуку ключових слів у файлі
def find_keywords_in_file(filename, keywords, queue):
    try:
        # Відкриваємо файл для читання
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                # Якщо знайдено ключове слово, додаємо до черги
                if keyword in content:
                    queue.put((filename, keyword))
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено!")

# Основна функція для багатопотокової обробки файлів з використанням черги
def multithreading_search_with_queue(file_list, keywords):
    threads = []
    queue = Queue()  # Створюємо чергу для результатів
    
    # Стартуємо потоки для кожного файлу
    for filename in file_list:
        thread = threading.Thread(target=find_keywords_in_file, args=(filename, keywords, queue))
        threads.append(thread)
        thread.start()
    
    # Очікуємо завершення всіх потоків
    for thread in threads:
        thread.join()
    
    # Збираємо всі результати з черги
    results = []
    while not queue.empty():
        results.append(queue.get())
    
    return results

# Основна частина програми
if __name__ == "__main__":
    # Створюємо тестові файли
    create_test_files()
    
    # Визначаємо список файлів і ключових слів
    file_list = ['file1.txt', 'file2.txt', 'file3.txt']  # Список файлів
    keywords = ['слово1', 'слово2']  # Ключові слова
    
    # Вимірюємо час виконання
    start_time = time.time()
    
    # Запуск багатопотокової обробки з чергою
    results = multithreading_search_with_queue(file_list, keywords)
    
    # Виводимо результати пошуку
    for res in results:
        print(f"Файл {res[0]} містить ключове слово: {res[1]}")
    
    end_time = time.time()
    print(f"Час виконання: {end_time - start_time} секунд")
