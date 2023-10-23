from PIL import Image
# Name: Sai Vaka
# Date: 9/8/21
# 1. Given an input of a space-separated list of any length of integers, output the sum of them.
l1 = [int(x) for x in input("1. Input a list to be summed: ").strip().split()]
print(f"Sum: {sum(l1)}")
# 2. Output the list of those integers (from #1) that are divisible by three.
print(f"Divisible by 3: {[i for i in l1 if i % 3 == 0]}")
# 3. Given an integer input, print the first n Fibonacci numbers. eg. n=6: 1, 1, 2, 3, 5, 8
p, c = 0, 1
for _ in range(int(input("3. Input an integer to find its Fibonacci sequence: "))):
    print(c, end=" ")
    p, c = c, p + c
print()
# 4. Given an input, output a string composed of every other character. eg. Aardvark -> Arvr
print(input("4. Input a string to find a string composed of alternate characters: ")[::2])
# 5. Given a positive integer input, check whether the number is prime or not.
n = int(input("5. Input an integer to check its primality: "))
if n <= 3:
    print(["Nonprime", "Prime"][n > 1])
elif n % 2 == 0 or n % 3 == 0:
    print("Nonprime")
else:
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            print("Nonprime")
            break
        i += 6
    else:
        print("Prime")
# 6. Calculate the area of a triangle given three side lengths.  eg. 13 14 15 -> 84
sides = [int(i) for i in input("6. Input 3 integers to find the triangles area: ").split()]
sp = sum(sides) / 2
print((sp * (sp - sides[0]) * (sp - sides[1]) * (sp - sides[2])) ** .5)
# 7. Given a input of a string, remove all punctuation from the string.
# eg. "Don't quote me," she said. -> Dontquotemeshesaid
s7 = input("7. Input a string to remove its punctuation: ").translate(str.maketrans('', '', ' .?!,:;-()[]{}\'"'))
print(s7)
# 8. Check whether the input string (from #7, lower cased, with punctuation removed) is a palindrome.
s7 = s7.lower()
print(f"8. Palindrome: {s7[::-1] == s7}")
# 9. Count the number of each vowel in the input string (from #7).
d9 = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
for i in d9:
    d9[i] = s7.count(i)
print(f"9. Vowels: {d9}")
# 10. Given two integers as input, print the value of f\left(k\right)=k^2-3k+2 for each integer between the two inputs.
# eg. 2 5 -> 0, 2, 6, 12
rnge = [int(i) for i in input("10. Input 2 integers to find f(x) of its range: ").split()]
print([i ** 2 - 3 * i + 2 for i in range(rnge[0], rnge[1] + 1)])
# 11. Given an input of a string, determines a character with the most number of occurrences.
s11 = input("Input a string: ")
d = {}
for i in set("".join(s11.split())):
    d[s11.count(i)] = i
print(f"11. Most frequent character: {d[max(d, key = lambda k: d[k] and k)]}")
# 12. With the input string from #11, output a list of all the words that start and end in a vowel.
print(f"12. Words that start and end with vowels: {[i for i in s11.split() if i[0] in 'aeiou' and i[-1] in 'aeiou']}")
# 13. With the input string from #11, capitalizes the starting letter of every word of the string and print it.
print(f"13. Capitalized first letters: {[i.title() for i in s11.split()]}")
# 14. With the input string from #11, prints out the string with each word in the string reversed.
print(f"14. Reverse: {[i[::-1] for i in s11.split()]}")
# 15. With the input string from #11, treats the first word of the input as a search string to be found in the rest
# of the string, treats the second word as a replacement for the first, and treats the rest of the input as the
# string to be searched. eg.    b Ba baby boy ->  BaaBay Baoy
spl = s11.split()
if len(spl) < 3:
    print(f"15. Replace: Not Enough Words")
else:
    print(f"15. Replaced first with second: {' '.join(spl[2:]).replace(spl[0], spl[1])}")
# 16. With an input of a string, removes all duplicate
# characters from a string.  Eg. detection -> detcion
print("".join(dict.fromkeys(input("16. Input a string to remove its duplicates: "))))
# 17. Given an input of a string, determines whether the string contains only digits.
s17 = input("17. Input a string to check if its numeric: ")
_17 = s17.isnumeric()
print(_17)
# 18. If #17 prints True, determines whether the string contains only 0 and 1 characters,
# and if so assumes it is a binary string, converts it to a number, and prints out the decimal value.
if _17 and all(i in "01" for i in s17):
    print(f"18. Binary: {int(s17, 2)}")
else:
    print("18. Binary: Not Binary")
# 19. Write a script that accepts two strings as input and determines whether the two strings are anagrams of each
# other.
print(["Anagram", "Not Anagram"][sorted(input("19. Type the first string to check if it's an anagram: ")) != sorted(
    input("Type the second string to check if it's an anagram: "))])
# 20. Given an input filename, if the file exists and is an image, find the dimensions of the image.
try:
    print((Image.open(input("20. Input a the name of the image file: "))).size)
except IOError:
    print("Couldn't find image")
# 21. Given an input of a string, find the longest palindrome within the string.
s21 = input("21. Input a string to find its longest palindrome: ").replace(" ", "")
res = []
for i in range(len(s21)):
    for j in range(0, i):
        cr = s21[j:i + 1]
        if cr == cr[::-1]:
            res.append(cr)
print("No Palindromes" if res == [] else max(res, key=len))
# 22. Given an input of a string, find all the permutations of a string.
s22 = input("22. Input a string to find all permutations: ")
pl = [s22[0]]
for i in range(1, len(s22)):
    for j in range(len(pl) - 1, -1, -1):
        cr = pl.pop(j)
        pl += [cr[:k] + s22[i] + cr[k:] for k in range(len(cr) + 1)]
pl.reverse()
print(pl)
# 23. Given the input string from #22, find all the unique permutations of a string.
print("23. All unique permutations: ")
print(set(pl))
# 24. Given an input of a string, find a longest non-decreasing subsequence within the string (according to ascii
# value).
s24 = input("24. Input a string to find the longest increasing substring: ")
r = []
for i, _ in enumerate(s24):
    for k, _ in enumerate(s24):
        if all(a <= b for a, b in zip(s24[i:k], s24[i + 1:k])):
            r.append(s24[i:k])
print(max(r, key=len))
