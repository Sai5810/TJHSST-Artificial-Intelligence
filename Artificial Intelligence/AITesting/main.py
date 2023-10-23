def sum13(nums):
  return ([nums[i] for i in range(len(nums)) if nums[i] != 13 and (i == 0 or nums[i-1] != 13)])

print(sum13([1, 2, 2, 1, 13]))