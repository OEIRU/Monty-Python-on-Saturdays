animals = {"dog12": {"клетка": 123, "вид": "собака обыкновенная", 'семейство': "собачья", "кличка": "Шарик"},
           "cat13": {"клетка": 17, "вид": "кот обыкновенный", 'семейство': "кошачья", "кличка": "Мурзик"}}
print("Прямой вызов переменной")
print(animals['cat13'])
print("Введите кличку животного")


# на самом деле можно любую информацию подуровня
def get_by_val(value):
    for key in animals:
        for lower_key in animals[key]:
            if animals[key][lower_key] == value:
                return key
                break


print(get_by_val(str(input())))

# Отсылка на отсылку
dog12 = {"клетка": 123, "вид": "собака обыкновенная", 'семейство': "собачья", "кличка": "Шарик"}
cat13 = {"клетка": 17, "вид": "кот обыкновенный", 'семейство': "кошачья", "кличка": "Мурзик"}

cells = {123: dog12, 17: cat13}
names = {"Шарик": dog12, "Мурзик": cat13}

print(names["Шарик"])
