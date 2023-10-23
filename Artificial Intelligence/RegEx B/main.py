# Nicole Kim, 2/5/2019, edited on 2/3/2021
import re

'''In Q40-42, An Othello board is any string of length 64 made up of only the characters in "xX.Oo".  
An Othello edge is any string of length 8 made up of only the characters in "xX.Oo".'''


def num_40(subject):
    # Write a regular expression that will match on an Othello board represented as a string.
    pattern = "(xX.Oo){64}"  # notice that python does not want / /
    match = re.match(pattern, subject, re.I)
    print(match.group(0)) if match is not None else print(match)


def num_41(subject):
    # Given a string of length 8, determine whether it could represent an Othello edge with exactly one hole.
    pattern = "[xXOo]*.[xXOo]*"
    match = re.match(pattern, subject, re.I)
    print(match.group(0)) if match is not None else print(match)


def num_42(subject):
    # Given an Othello edge as a string, determine whether there is a hole such that if X plays to the hole (assuming
    # it could), it will be connected to one of the corners through X tokens. Specifically, this means that one of
    # the ends must be a hole, or starting from an end there is a sequence of at least one x followed immediately by
    # a sequence (possibly empty) of o, immediately followed by a hole.
    pattern = "(^[xX]*.)|(.[xX]*$)"
    match = re.search(pattern, subject, re.I)
    print(match.group(0)) if match is not None else print(match)


def num_43(subject):
    # Match on all strings of odd length.
    pattern = "^.(..)*$"
    match = re.match(pattern, subject, re.DOTALL)
    print(match.group(0)) if match is not None else print(match)


def num_44(subject):
    # Match on all odd length binary strings starting with 0, and on even length binary strings starting with 1.
    pattern = "(^0(..)*$)|(^1.(..)*$)"
    match = re.match(pattern, subject)
    print(match.group(0)) if match is not None else print(match)


def num_45(subject):
    # Match all words having two adjacent vowels that differ.
    pattern = "([aeiou])(?!\1)[aeiou]"
    matches = re.finditer(pattern, subject, re.I)
    print([m.group() for m in matches])


def num_46(subject):
    # Match on all binary strings which DO NOT contain the substring 110.
    pattern = "^((?!110).)*$"
    match = re.match(pattern, subject)
    print(match.group(0)) if match is not None else print(match)


def num_47(subject):
    # Match on all non-empty strings over the alphabet {a, b, c} that contain at most one a.
    pattern = "([bc])*a?([bc])*"
    match = re.match(pattern, subject)
    print(match.group(0)) if match is not None else print(match)


def num_48(subject):
    # Match on all non-empty strings over the alphabet {a, b, c} that contain an even number of a's.
    pattern = "[bc]*(a[bc]*a[bc]*)*[bc]*"
    match = re.match(pattern, subject)
    print(match.group(0)) if match is not None else print(match)


def num_49(subject):
    # Match on all positive, even, base 3 integer strings.
    pattern = "[02]*(1[02]*1[02]*)*[02]*"
    match = re.match(pattern, subject)
    print(match.group(0)) if match is not None else print(match)


while True:
    input_num = input("Choose the exercise # (40 - 49 or -1 to terminate):")
    if input_num == '-1':
        exit("Good bye")
    input_str = input("Input string: ")
    eval("num_" + input_num)(input_str)
    print()
