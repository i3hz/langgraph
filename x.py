for _ in range(int(input())):
    n = int(input())
    a = list(map(int, input().split()))
    b = {}
    for i in a:
        if i in b:
            b[i] += 1
        else:
            b[i] = 1      
    flag = True
    for k, v in b.items():
        if v % k != 0:
            flag = False
            break
            
    if not flag: 
        print(-1)
        continue
    g = {}
    for i in range(n):
        val = a[i]
        if val not in g:
            g[val] = []
        g[val].append(i)
    res = [-1] * n
    val = 1
    for k in sorted(g.keys()):
        x = g[k]
        for i in range(0, len(x), k):
            subgroup = x[i : i + k]
            for y in subgroup:
                res[y] = val
            val += 1
    print(*res)