import random

# Тест Миллера-Рабина для проверки простоты числа
def is_prime(n, k=128):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Представляем n-1 как 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Тест Миллера-Рабина
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = modular_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = modular_pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Генерация случайного нечётного числа нужной длины
def generate_prime_candidate(length):
    # Генерируем случайное число длины length бит
    p = random.getrandbits(length)
    # Устанавливаем самый значимый и наименее значимый биты в 1, чтобы гарантировать, что число будет нечетным и нужной длины
    p |= (1 << length - 1) | 1
    return p

# Генерация простого числа
def generate_prime_number(length=1024):
    p = 4
    # Продолжаем генерировать числа, пока не получим простое
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p

# Алгоритм Евклида для нахождения НОД
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Расширенный алгоритм Евклида для нахождения обратного по модулю
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_value, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_value, x, y

# Функция для вычисления обратного по модулю
def mod_inverse(e, phi):
    gcd_value, x, y = extended_gcd(e, phi)
    if gcd_value != 1:
        raise Exception('Обратного числа не существует')
    else:
        return x % phi

# Функция модульного возведения в степень
def modular_pow(base, exponent, modulus):
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus  # Приводим base в диапазон modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2  # Целочисленное деление
        base = (base * base) % modulus
    return result

# Генерация ключей RSA
def generate_keys(bit_length=1024):
    p = generate_prime_number(bit_length)
    q = generate_prime_number(bit_length)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537  # Открытая экспонента

    if gcd(e, phi_n) != 1:
        raise ValueError("e и phi_n не взаимно просты")

    d = mod_inverse(e, phi_n)
    return (e, n), (d, n)

# Функция для шифрования
def encrypt(message, public_key):
    e, n = public_key
    message_bytes = message.encode('utf-8')
    message_int = int.from_bytes(message_bytes, byteorder='big')

    if message_int >= n:
        raise ValueError("Сообщение слишком длинное для данного ключа")

    encrypted_message = modular_pow(message_int, e, n)
    return encrypted_message

# Функция для расшифрования
def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_int = modular_pow(encrypted_message, d, n)
    decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')

    try:
        # Попытка декодировать в UTF-8
        decrypted_message = decrypted_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Если ошибка, декодируем с использованием latin-1 для диагностики
        print("Ошибка декодирования в UTF-8, используем latin-1 для временного решения.")
        decrypted_message = decrypted_bytes.decode('latin-1')

    return decrypted_message


# Сохранение ключа в файл
def save_key_to_file(key, filename):
    with open(filename, 'w') as f:
        f.write(f"{key[0]}\n{key[1]}")

# Загрузка ключа из файла
def load_key_from_file(filename):
    with open(filename, 'r') as f:
        key_data = f.readlines()
        return int(key_data[0]), int(key_data[1])

# Интерфейс для работы с программой
def rsa_interface():
    print("Добро пожаловать в RSA шифровальщик/дешифровальщик!")
    print("Выберите действие:")
    print("1. Генерация ключей и сохранение в файлы")
    print("2. Шифрование сообщения (из файла или с клавиатуры)")
    print("3. Дешифрование сообщения (из файла или с клавиатуры)")

    choice = input("Ваш выбор: ")

    if choice == '1':
        public_key, private_key = generate_keys()
        save_key_to_file(public_key.txt, "public_key.txt")
        save_key_to_file(private_key, "private_key.txt")
        print("Ключи сгенерированы и сохранены в файлы 'public_key.txt' и 'private_key.txt'.")

    elif choice == '2':
        public_key = load_key_from_file("public_key.txt")
        source = input("Вы хотите зашифровать сообщение из файла (1) или с клавиатуры (2)? ")

        if source == '1':
            filename = input("Введите имя файла с сообщением: ")
            with open(filename, 'r', encoding='utf-8') as f:
                message = f.read()
        elif source == '2':
            message = input("Введите сообщение: ")

        encrypted_message = encrypt(message, public_key)
        print(f"Зашифрованное сообщение: {encrypted_message}")
        save_file = input("Введите имя файла для сохранения зашифрованного сообщения: ")
        with open(save_file, 'w') as f:
            f.write(str(encrypted_message))  # Сохраняем зашифрованное число

    elif choice == '3':
        private_key = load_key_from_file("private_key.txt")
        source = input("Вы хотите расшифровать сообщение из файла (1) или с клавиатуры (2)? ")

        if source == '1':
            filename = input("Введите имя файла с зашифрованным сообщением: ")
            with open(filename, 'r') as f:
                encrypted_message = int(f.read())  # Загружаем зашифрованное число
        elif source == '2':
            encrypted_message = int(input("Введите зашифрованное сообщение (число): "))

        decrypted_message = decrypt(encrypted_message, private_key)
        print(f"Расшифрованное сообщение: {decrypted_message}")

# Запуск интерфейса
if __name__ == "__main__":
    rsa_interface()
