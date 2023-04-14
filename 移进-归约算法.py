# 文法产生式
grammar = {
    'S': ['NP VP'],
    'NP': ['Det N', 'Det N PP'],
    'VP': ['V NP', 'V NP PP'],
    'PP': ['P NP'],
    'Det': ['a', 'the'],
    'N': ['boy', 'girl', 'dog', 'cat'],
    'V': ['chased', 'sat'],
    'P': ['in', 'on', 'with']
    }

# 操作符优先级
precedence = {
                'V': 2,
                'P': 1,
                'Det': 0,
                'N': 0,
                '$': -1
            }

def parse(tokens):
    # 初始化分析栈
    stack = []
    i = 0
    tree = {}
    while len(tokens) > 1:
        # 打印分析栈和输入的状态
        print('Stack:', stack)
        print('Input:', tokens[i:])
        
        if stack[-1] in grammar:
            # 非终结符，查找对应的产生式
            for rule in grammar[stack[-1]]:
                if rule.split()[0] == stack[-1]:
                    # 归约操作
                    new_stack = stack[:-1] + rule.split()[::-1]
                    print('Reduce:', stack[-1], '->', rule)
                    stack = new_stack
                    break
            else:
                # 没有找到对应的产生式，分析失败
                print('Error: no rule found for', stack[-1])
                return False
        else:
            # 终结符或 $，进行移进操作
            if len(tokens[i:]) > 0:
                stack.append(tokens[i])
                i += 1
                print('Shift:', stack[-1])
            else:
                print('Error: input exhausted')
                return False
        # 判断操作符优先级，进行归约或移进操作
        op = stack[-1]
        if op in precedence:
            if precedence[op] >= precedence[tokens[i]]:
                # 归约操作
                for rule in grammar[op]:
                    if rule.split()[0] == op:
                        new_stack = stack[:-1] + rule.split()[::-1]
                        print('Reduce:', op, '->', rule)
                        stack = new_stack
                        break
                else:
                    print('Error: no rule found for', op)
                    return False
            else:
                # 移进操作
                stack.append(tokens[i])
                i += 1
                print('Shift:', stack[-1])
        else:
            # 移进操作
            stack.append(tokens[i])
            i += 1
            print('Shift:', stack[-1])
    
    # 最终结果为 S -> NP VP
    if len(stack) == 1 and stack[0] == 'S':
        print('Success')
        return True
    else:
        print('Error: final stack is', stack)
        return False

# 测试代码
tokens = ['a', 'boy', 'chased', 'the', 'dog', 'with', 'a', 'cat', '$']
parse(tokens)
