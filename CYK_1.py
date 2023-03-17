def cyk(words, grammar):
    n = len(words)
    chart = [[set() for _ in range(n-i)] for i in range(n)]
    for i in range(n):
        for rule in grammar:
            if words[i] in rule[1]:
                chart[0][i].add(rule[0])
    for i in range(1, n):
        for j in range(n-i):
            for k in range(i):
                for rule in grammar[:3]:
                    s1, s2 = rule[1]
                    left = chart[k][j]
                    right = chart[i-k-1][j+k+1]
                    if s1 in left and s2 in right:
                        chart[i][j].add(rule[0])
    return chart

# 示例用法
grammar = [('S', ['NP', 'VP']), ('NP', ['Det', 'N']), ('VP', ['V', 'NP']),
           ('Det', ['a']), ('Det', ['an']), ('Det', ['the']),
           ('N', ['cat']), ('N', ['dog']), ('N', ['rug']),
           ('V', ['chased']), ('V', ['sat'])]
words = ['the', 'cat', 'chased', 'a', 'dog']
chart = cyk(words, grammar)

for i in range(len(words)):
    print(chart[i])
