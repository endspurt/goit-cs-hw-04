import multiprocessing
from queue import Queue
import os
import time

# Функція для пошуку ключових слів у файлі з буферизацією (використовується для мультипроцесорної обробки)
def find_keywords_in_file_multiprocessing(filename, keywords, queue, buffer_size=1024):
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

# Функція для багатопроцесорної обробки файлів
def multiprocessing_search(file_list, keywords, max_processes=None):
    if max_processes is None:
        max_processes = os.cpu_count()  # Визначаємо кількість процесорних ядер
    
    queue = multiprocessing.Manager().Queue()  # Використовуємо спільну чергу
    processes = []
    
    # Ділимо список файлів між процесами
    for i in range(0, len(file_list), max_processes):
        current_files = file_list[i:i + max_processes]
        
        # Стартуємо процеси для кожного файлу в межах поточного пулу
        for filename in current_files:
            process = multiprocessing.Process(target=find_keywords_in_file_multiprocessing, args=(filename, keywords, queue))
            processes.append(process)
            process.start()
        
        # Чекаємо на завершення поточного пулу процесів перед початком нових
        for process in processes:
            process.join()
    
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
    
    # Запуск багатопроцесорної обробки
    results = multiprocessing_search(file_list, keywords)
    
    # Виводимо результати пошуку
    for res in results:
        print(f"Файл {res[0]} містить ключове слово: {res[1]}")
    
    end_time = time.time()
    print(f"Час виконання: {end_time - start_time} секунд")
