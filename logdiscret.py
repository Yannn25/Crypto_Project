def loga_d(g, y, p):

    l=[]
    for x in range(p-1):
        l.append(pow(g, x)%p)

    
    for x in range(len(l)):
        if y == l[x]:
            return x
    return None

print(loga_d(3, 4, 7))



