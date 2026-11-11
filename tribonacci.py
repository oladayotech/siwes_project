def tribonacci(n):
    tribonacci_list = []
    
    tribonacci_list.append(0)
    tribonacci_list.append(1)
    tribonacci_list.append(1)
    
    i = 3
    
    while i <= n:
        print(tribonacci_list, i)
        result = tribonacci_list[i-1] + tribonacci_list[i-2] + tribonacci_list[i-3]
        tribonacci_list.append(result)
        i+=1
        
    return tribonacci_list

tribonacci(30)