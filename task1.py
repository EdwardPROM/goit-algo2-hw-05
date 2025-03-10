import hashlib

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size                      
        self.num_hashes = num_hashes          
        self.bit_array = [0] * size           
    
    def _hashes(self, item):
        """Повертає список хеш-значень для елемента."""
        hashes = []
        for i in range(self.num_hashes):
            # Обчислюємо хеш
            hash_result = hashlib.sha256((item + str(i)).encode('utf-8')).hexdigest()
            index = int(hash_result, 16) % self.size
            hashes.append(index)
        return hashes
    
    def add(self, item):
        """Додає елемент у фільтр."""
        for hash_index in self._hashes(item):
            self.bit_array[hash_index] = 1
    
    def check(self, item):
        """Перевіряє, чи є елемент у фільтрі."""
        for hash_index in self._hashes(item):
            if self.bit_array[hash_index] == 0:
                return False
        return True

def check_password_uniqueness(bloom_filter, passwords_to_check):
    """Перевіряє список паролів на унікальність."""
    results = {}
    for password in passwords_to_check:
        if not isinstance(password, str) or password.strip() == '':
            results[password] = "некоректне значення"
            continue
        
        if bloom_filter.check(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", ""]

    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
