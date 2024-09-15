import threading
import time

# Функція для пошуку ключових слів у файлі
def find_keywords_in_file(filename, keywords, results, thread_id):
    # Відкриваємо файл для читання
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        for keyword in keywords:
            # Якщо знайдено ключове слово, додаємо до результатів
            if keyword in content:
                results[thread_id].append((filename, keyword))

# Основна функція для багатопотокової обробки файлів
def multithreading_search(file_list, keywords):
    threads = []
    results = [[] for _ in range(len(file_list))]
    
    # Стартуємо потоки для кожного файлу
    for i, filename in enumerate(file_list):
        thread = threading.Thread(target=find_keywords_in_file, args=(filename, keywords, results, i))
        threads.append(thread)
        thread.start()
    
    # Очікуємо завершення всіх потоків
    for thread in threads:
        thread.join()
    
    return results

# Приклад використання
file_list = ['file1.txt', 'file2.txt', 'file3.txt']  # Список файлів
keywords = ['слово1', 'слово2']  # Ключові слова
start_time = time.time()

# Запуск багатопотокової обробки
results = multithreading_search(file_list, keywords)

# Виводимо результати пошуку
for thread_id, res in enumerate(results):
    print(f"Результати для потоку {thread_id}: {res}")

end_time = time.time()
print(f"Час виконання: {end_time - start_time} секунд")
