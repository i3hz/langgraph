for _ in range(int(input())):
    a,b = map(int, input().split())
    if a%2==1 and b%2==1:
        print(a*b + 1)
    elif a%2==0 and b%2==0:
        print((a*b)//2 + 2 )
    elif a%2==0 and b%2==1:
        print(-1)
    else:
        if b%4==0:
            print((a*b)//2 + 2 )
        else:
            print(-1)
    
                 
    