s24 = input("24. Input a string to find the longest increasing substring: ")
r = []
for i, _ in enumerate(s24):
    for k, _ in enumerate(s24):
        if all(a <= b for a, b in zip(s24[i:k], s24[i + 1:k])):
            r.append(s24[i:k])
print(max(r, key=len))
