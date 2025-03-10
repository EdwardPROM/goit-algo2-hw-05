import json
import time
from datasketch import HyperLogLog

# Завантаження IP з лог-файлу
def load_ips_from_log(file_path):
    ip_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            try:
                log_entry = json.loads(line)
                ip = log_entry.get('remote_addr')
                if ip:
                    ip_list.append(ip)
            except json.JSONDecodeError:
                continue  
    return ip_list

# Точний підрахунок
def exact_count(ip_list):
    start_time = time.time()
    unique_ips = set(ip_list)
    count = len(unique_ips)
    elapsed_time = time.time() - start_time
    return count, elapsed_time

# HyperLogLog підрахунок
def hyperloglog_count(ip_list, p=14):
    start_time = time.time()
    hll = HyperLogLog(p)
    for ip in ip_list:
        hll.update(ip.encode('utf-8'))
    count = int(hll.count())
    elapsed_time = time.time() - start_time
    return count, elapsed_time

def print_results(exact_unique, exact_time, hll_unique, hll_time):
    print("\nРезультати порівняння:\n")
    print(f"{'':<35}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
    print(f"{'Унікальні елементи':<35}{exact_unique:<20.1f}{hll_unique:<20.1f}")
    print(f"{'Час виконання (сек.)':<35}{exact_time:<20.4f}{hll_time:<20.4f}")

# Основна функція
def run_comparison(file_path):
    print("📥 Завантаження IP адрес з логу...")
    ip_list = load_ips_from_log(file_path)
    print(f"✅ Завантажено {len(ip_list)} IP адрес.")

    exact_unique, exact_time = exact_count(ip_list)
    hll_unique, hll_time = hyperloglog_count(ip_list)

    print_results(exact_unique, exact_time, hll_unique, hll_time)

if __name__ == "__main__":
    log_file_path = "lms-stage-access.log" 
    run_comparison(log_file_path)
