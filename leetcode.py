# class Solution:
def lastStoneWeight(stones: list[int]) -> int:
    sorted_stones = sorted(stones)
    len_stones = len(sorted_stones)
    while len_stones > 1:
        subtraction_result = sorted_stones[-1] - sorted_stones[-2]
        print(subtraction_result)
        if subtraction_result == 0:
            sorted_stones.pop()
            sorted_stones.pop()
            print(sorted_stones)
            len_stones = len(sorted_stones)
        elif subtraction_result > 0:
            sorted_stones.pop()
            sorted_stones.pop()
            sorted_stones.append(subtraction_result)
            sorted_stones = sorted(sorted_stones)
            print(sorted_stones)
            len_stones = len(sorted_stones)
    print(sorted_stones)
    return sorted_stones
    
stones = [2,7,4,1,8,1]

stones1 = lastStoneWeight(stones)