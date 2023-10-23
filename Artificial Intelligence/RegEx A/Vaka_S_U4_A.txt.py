import re


def num_30(s):
    # Current test checks if the string is '0'
    pattern = "^101$|^100$|^0$"  # notice that python does not want / /
    match = re.match(pattern, s)
    print("string is either 0, 100, or 101: ", match is not None)


def num_31(s):
    # Current test checks if the string is '0'
    print("string is a binary string:", re.match("^[0-1]*$", s) is not None)


# Pre-condition: input is a binary string, so you do not need to check if it's a binary or not.
def num_32(s):
    pattern = '[0-1]*0$'
    print("string is an even binary number:", re.match(pattern, s) is not None)


def num_33(s):
    # Current test searches words with 'a'
    pattern = "\w*[aeiou]\w*[aeiou]\w"
    # Notice that python does not support /i in the pattern.
    # Use re.I for case insensitive when you match(exact same) or search(has one or more)
    print("there's a word at least two vowels:", re.search(pattern, s, re.I) is not None)


def num_34(s):
    pattern = "1[0-1]*0$"
    print("even binary integer string:", re.match(pattern, s) is not None)


def num_35(s):
    pattern = "[0-1]*110[0-1]*"
    print("binary string including 110:", re.match(pattern, s) is not None)


def num_36(s):
    pattern = "^.{2,4}$"
    print("length at least two, but at most four:", re.match(pattern, s, re.DOTALL) is not None)


def num_37(s):
    pattern = "\d{3}[\s-]*\d{2}[\s-]*\d{4}"
    print("valid social security number:", re.match(pattern, s) is not None)


def num_38(s):
    # When you read multiline input such as "I\nAM\nSAM."
    # str = str.replace('\\n', '\n') # If you need this...
    pattern = "\bd\w*\b"

    # When you want to use /im options:
    d_search = re.search(pattern, s, re.I | re.MULTILINE)
    print("first word with d on a line:", d_search is not None)


def num_39(s):
    pattern = "\b0[0-1]*0\b|\b1[0-1]*1\b"
    print("There's same number of 01 substrings as 10 substrings: ", re.match(pattern, s) is not None)


def main():
    while True:
        input_num = input("Choose the exercise # (30 - 39 or -1 to terminate):")
        if input_num == '-1':
            exit("Good bye")
        input_str = input("Input string: ")
        eval("num_" + input_num)(input_str)
        print()


if __name__ == "__main__":
    main()
