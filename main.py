d = {}

with open("text.txt", "r") as f:
    content = f.read()

split = content.split()

for i in split:
    if i in d.keys():
        d[i] += 1
    else:
        d[i] = 1


l = list(d.items())

for _ in range(len(l)):
    for i in range(len(l) - 1):
        if l[i][1] > l[i + 1][1]:
            t = l[i + 1]
            l[i + 1] = l[i]
            l[i] = t

for i in range(len(l) - 1, -1, -1):
    print(f"{l[i][0]} : {l[i][1]}")
