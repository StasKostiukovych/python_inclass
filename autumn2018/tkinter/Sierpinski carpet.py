import turtle as t
t.speed(11110)

def sierinski_carpet(l,n):
    if (n > 1):
        for i in range(3):
            t.left(120)
            t.forward(l)
            n -= 1
            sierinski_carpet(l/2, n)
            n = n + 1

sierinski_carpet(400, 7)
t.done()