from PIL import Image

# Name: Sai Vaka
# Date: 9/8/21
# 1. Given an input of a space-separated list of any length of integers, output the sum of them.
l1 = [int(x) for x in input("list of numbers: ").strip().split()]
print(f"1. sum = {sum(l1)}")
# 2. Output the list of those integers (from #1) that are divisible by three.
print(f"2. list of multiples of 3: {[i for i in l1 if i % 3 == 0]}")
# 3. Given an integer input, print the first n Fibonacci numbers. eg. n=6: 1, 1, 2, 3, 5, 8
p, c = 0, 1
n = int(input("Type n for Fibonacci sequence: "))
print("fibonacci: ", end="")
for _ in range(n):
    print(c, end=" ")
    p, c = c, p + c
print()
# 4. Given an input, output a string composed of every other character. eg. Aardvark -> Arvr
print(f"4. every other str: {input('Type a string: ')[::2]}")
# 5. Given a positive integer input, check whether the number is prime or not.
n = int(input("Type a number to check prime: "))
if n <= 3:
    print(f"Is Prime? {n > 1}")
elif n % 2 == 0 or n % 3 == 0:
    print("Is Prime? False")
else:
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            print("Is Prime? False")
            break
        i += 6
    else:
        print("Is Prime? True")
# 6. Calculate the area of a triangle given three side lengths.  eg. 13 14 15 -> 84
sides = [int(i) for i in input("Type three sides of a triangle: ").split()]
sp = sum(sides) / 2
print(f"6. The area of 13 14 15 is {(sp * (sp - sides[0]) * (sp - sides[1]) * (sp - sides[2])) ** .5}")
# 7. Given a input of a string, remove all punctuation from the string.
# eg. "Don't quote me," she said. -> Dontquotemeshesaid
s7 = input("Type a sentence: ").translate(str.maketrans('', '', ' .?!,:;-()[]{}\'"'))
print(f"7. Punct removed: {s7}")
# 8. Check whether the input string (from #7, lower cased, with punctuation removed) is a palindrome.
s7 = s7.lower()
print(f"8. Is palindrome? {s7[::-1] == s7}")
# 9. Count the number of each vowel in the input string (from #7).
d9 = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
for i in d9:
    d9[i] = s7.count(i)
print(f"9. Count each vowel: {d9}")
# 10. Given two integers as input, print the value of f\left(k\right)=k^2-3k+2 for each integer between the two inputs.
# eg. 2 5 -> 0, 2, 6, 12
rg = [int(i) for i in input("Type two integers (lower bound and upper bound): ").split()]
print("10. Evaluate f(k)=k^2 - 3k + 2 from 2 to 5:", end="")
for j in (i ** 2 - 3 * i + 2 for i in range(rg[0], rg[1] + 1)):
    print(j, end=" ")
print()
# 11. Given an input of a string, determines a character with the most number of occurrences.
s11 = input("Type a string: ")
d = {}
for i in set("".join(s11.split())):
    d[s11.count(i)] = i
print(f"11. Most occurred char: {d[max(d, key=lambda k: d[k] and k)]}")
# 12. With the input string from #11, output a list of all the words that start and end in a vowel.
print(
    f"12. List of words starting and ending with vowels: {[i for i in s11.split() if i[0] in 'aeiou' and i[-1] in 'aeiou']}")
# 13. With the input string from #11, capitalizes the starting letter of every word of the string and print it.
print(f"13. Capitalize starting letter of every word: {' '.join(i.title() for i in s11.split())}")
# 14. With the input string from #11, prints out the string with each word in the string reversed.
print(f"14. Reverse every word: {' '.join(i[::-1] for i in s11.split())}")
# 15. With the input string from #11, treats the first word of the input as a search string to be found in the rest
# of the string, treats the second word as a replacement for the first, and treats the rest of the input as the
# string to be searched. eg.    b Ba baby boy ->  BaaBay Baoy
spl = s11.split()
if len(spl) < 3:
    print(f"15. Replace: Not Enough Words")
else:
    print(f"15. Find the first and replace with the second: {' '.join(spl[2:]).replace(spl[0], spl[1])}")
# 16. With an input of a string, removes all duplicate
# characters from a string.  Eg. detection -> detcion
print(
    "16. Remove all duplicat chars: " + "".join(dict.fromkeys(input("Type a string to remove all duplicate chars: "))))
# 17. Given an input of a string, determines whether the string contains only digits.
s17 = input("Type a string to check if it has only digits or not: ")
_17 = s17.isnumeric()
print(f"17. Is a number?: {_17}")
# 18. If #17 prints True, determines whether the string contains only 0 and 1 characters,
# and if so assumes it is a binary string, converts it to a number, and prints out the decimal value.
if _17 and all(i in "01" for i in s17):
    print(f"18. It is a binary number: {int(s17, 2)}")
else:
    print("18. Binary: Not Binary")
# 19. Write a script that accepts two strings as input and determines whether the two strings are anagrams of each
# other.
print(
    f"19. Are elvis and lives anagram?: {sorted(input('Type the first string to check anagram: ')) == sorted(input('Type the second string to check anagram: '))}")
# 20. Given an input filename, if the file exists and is an image, find the dimensions of the image.
try:
    w, h = (Image.open(input("Type the image file name: "))).size
    print(f"20. Image dimension: {w} by {h}")
except IOError:
    print("Couldn't find image")
# 21. Given an input of a string, find the longest palindrome within the string.
s21 = input("Type a string to find the longest palindrome: ").replace(" ", "")
res = []
for i in range(len(s21)):
    for j in range(0, i):
        cr = s21[j:i + 1]
        if cr == cr[::-1]:
            res.append(cr)
print("No Palindromes" if res == [] else f"21. Longest palindrome within the string: {max(res, key=len)}")
# 22. Given an input of a string, find all the permutations of a string.
s22 = input("Type a string to do permutation: ")
pl = [s22[0]]
for i in range(1, len(s22)):
    for j in range(len(pl) - 1, -1, -1):
        cr = pl.pop(j)
        pl += [cr[:k] + s22[i] + cr[k:] for k in range(len(cr) + 1)]
pl.reverse()
print(f"22. all permutations: {pl}")
# 23. Given the input string from #22, find all the unique permutations of a string.
print(f"23. all unique permutations: {set(pl)}")
# 24. Given an input of a string, find a longest non-decreasing subsequence within the string (according to ascii
# value).
s24 = input("Type a string to find the longest non-decreasing sub: ")
r = []
for i, _ in enumerate(s24):
    for k, _ in enumerate(s24):
        if all(a <= b for a, b in zip(s24[i:k], s24[i + 1:k])):
            r.append(s24[i:k])
print(f"24. longest non-decreasing sub: {max(r, key=len)}")
