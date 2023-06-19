# 1 

def combine_sequences(arr1, arr2):
    result = sorted(arr1 + arr2)
    return result

arr1 = [1, 4, 0, 12, 4, 5]
arr2 = [24, 1, 2, 10, 8]

# 2

fruits = {
    'Apricots': [0.9, 0, 10.5, 46],
    'Grape': [0.4, 0, 17.5, 69],
    'Orange': [0.9, 0, 8.4, 38],
    'Ananas': [0.4, 0, 11.8, 48],
    'Apples': [0.4, 0, 11.3, 46],
    'Pear': [0.4, 0, 10.7, 42],
    'Kiwi': [0.8, 0, 8.1, 47]
}

for index, (fruit, values) in enumerate(fruits.items(), start=1):
    protein, fat, carbs, calories = values
    print(f"{index} {fruit} {protein} {fat} {carbs} {calories}")