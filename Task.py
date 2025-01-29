input_string = input("Введите массив целых чисел через пробел: ")
nums = []


for number in input_string.split():
    print(number)

    nums.append(int(number))


result = []

for num in nums:
    count = 0
    for x in nums:
        if x < num:
            count += 1
    result.append(count)

output_string = ""
for count in result:
    output_string += str(count) + " "


print(output_string.strip())
