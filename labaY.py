def hanoi_tower(n, source, target, auxiliary):
    if n > 0:
        # Перенесення (n-1) кілець з початкового стержня на допоміжний стержень
        hanoi_tower(n-1, source, auxiliary, target)
        
        # Перенесення останнього кільця з початкового стержня на цільовий стержень
        print(f"{source} - {target}")
        
        # Перенесення (n-1) кілець з допоміжного стержня на цільовий стержень
        hanoi_tower(n-1, auxiliary, target, source)

# Зчитування вхідних даних
n = int(input("Введіть кількість кілець: "))

# Виклик функції для розв'язання головоломки Ханойської вежі
hanoi_tower(n, 1, 3, 2)

def word_length_statistics(sentence):
    words = sentence.split()  # Розбиваємо речення на слова за допомогою пропусків
    length_count = {}  # Словник для зберігання кількості слів за довжиною

    for word in words:
        length = len(word)
        if length in length_count:
            length_count[length] += 1
        else:
            length_count[length] = 1

    # Сортування словника за ключем (довжиною слова)
    sorted_lengths = sorted(length_count.keys())

    # Виведення статистики довжин слів
    for length in sorted_lengths:
        count = length_count[length]
        print(f"{length}: {count}")

# Зчитування вхідних даних
sentence = input("Введіть рядок: ")

# Виклик функції для обчислення статистики довжин слів
word_length_statistics(sentence)