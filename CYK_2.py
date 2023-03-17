def cyk_bottom_up(words, grammar):
    n = len(words)
    chart = [[set() for _ in range(n)] for _ in range(n)]
    # 初始化底部的词性标记
    for i in range(n):
        for rule in grammar:
            if words[i] in rule[1]:
                chart[i][i].add(rule[0])
    # 逐步合并成较长的子串
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length - 1
            for k in range(i, j):
                for rule in grammar[:3             ]:
                    s1, s2 = rule[1]
                    if s1 in chart[i][k] and s2 in chart[k+1][j]:
                        chart[i][j].add(rule[0])
    return chart

# 示例用法
grammar = [('S', ['NP', 'VP']), ('NP', ['Det', 'N']), ('VP', ['V', 'NP']),
           ('Det', ['a']), ('Det', ['an']), ('Det', ['the']),
           ('N', ['cat']), ('N', ['dog']), ('N', ['rug']),
           ('V', ['chased']), ('V', ['sat'])]
words = ['the', 'cat', 'chased', 'a', 'dog']
chart = cyk_bottom_up(words, grammar)

for i in range(len(words)):
    print(chart[i])
    