import concurrent.futures
import time
from collections import defaultdict
import os


def search_keywords(file_paths, keywords):
    result = defaultdict(list)
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        result[keyword].append(file_path)
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {e}")
    return result


def main(file_list, keywords, num_threads=3):
    # Разделение списка файлов на num_threads частей
    chunk_size = len(file_list) // num_threads
    chunks = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]

    if len(file_list) % num_threads != 0:
        chunks[-1].extend(file_list[num_threads * chunk_size:])
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_chunk = {executor.submit(search_keywords, chunk, keywords): chunk for chunk in chunks}
        results = defaultdict(list)
        
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_results = future.result()
            for keyword, paths in chunk_results.items():
                results[keyword].extend(paths)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Время выполнения: {elapsed_time} секунд")
    return results

if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
   
    file_list = [f'{script_dir}\\file1.txt', f'{script_dir}\\file2.txt', f'{script_dir}\\file3.txt',
                 f'{script_dir}\\file4.txt', f'{script_dir}\\file5.txt', f'{script_dir}\\file6.txt']
    keywords = ['and', 'program', 'multiprocessor']
    
    # Запуск программы
    results = main(file_list, keywords)
    for keyword, files in results.items():
        print(f"{keyword}: {files}")


