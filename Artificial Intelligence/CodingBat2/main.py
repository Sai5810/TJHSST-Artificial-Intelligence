def sum67(nums):
    return sum(j for i, j in enumerate(nums) if 6 not in nums[:i + 1] or 7 in nums[len(nums[:i + 1]) - nums[:i + 1][::-1].index(6) + 0:i])


def count_evens(nums):
    return sum(i % 2 == 0 for i in nums)


def big_diff(nums):
    return max(nums) - min(nums)


def centered_average(nums):
    return sum(sorted(nums)[1:-1]) // len(nums[2:])


def sum13(nums):
    return sum(i for i, j in zip(nums, [0] + nums) if 13 not in (i, j))


def has22(nums):
    return (2, 2) in zip(nums, [0] + nums)


def string_times(str, n):
    return str * n


def front_times(str, n):
    return str[:3] * n


def string_bits(str):
    return str[::2]


def string_splosion(str):
    return ''.join(str[:i + 1] for i in range(len(str)))


def last2(str):
    return sum(str[-2:] == str[i:i + 2] for i in range(len(str) - 2))


def array_count9(nums):
    return nums.count(9)


def array_front9(nums):
    return 9 in nums[:4]


def array123(nums):
    return " 1, 2, 3," in str([0] + nums + [0])


def string_match(a, b):
    return sum(a[i:i + 2] == b[i:i + 2] for i in range(len(a) - 1))


def xyz_there(str):
    return str.count('.xyz') != str.count('xyz')


def double_char(str):
    return ''.join(i * 2 for i in str)


def count_hi(str):
    return str.count("hi")


def cat_dog(str):
    return str.count("cat") == str.count("dog")


def count_code(str):
    return sum(str[i:i + 2] == "co" and str[i + 3] == "e" for i in range(len(str) - 3))


def end_other(a, b):
    return all(i == j for i, j in zip(a.lower()[::-1], b.lower()[::-1]))


def make_chocolate(small, big, goal):
    return [-1, v := max(goal % 5, goal - 5 * big)][small >= v]


def make_bricks(small, big, goal):
    return small >= max(goal % 5, goal - 5 * big)


def lone_sum(a, b, c):
    return sum(i for i in [a, b, c] if [a, b, c].count(i) == 1)


def lucky_sum(a, b, c):
    return [0, a, a + b, a + b + c][[a, b, c, 13].index(13)]


def no_teen_sum(a, b, c):
    return sum(i for i in [a, b, c] if i not in [13, 14, 17, 18, 19])


def round_sum(a, b, c):
    return (a + 5) // 10 * 10 + (b + 5) // 10 * 10 + (c + 5) // 10 * 10


def close_far(a, b, c):
    return (abs(a - b) <= 1) != (abs(a - c) <= 1) and abs(b - c) > 1
