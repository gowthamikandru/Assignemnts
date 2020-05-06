def reduced_string(s):
    stack = []
    for c in s:
        if stack and c == stack[-1]:
            stack.pop()
        else:
            stack.append(c)
    if len(stack) == 0:
        return ("stack"," ")
    else:
        return ''.join(stack)

print(reduced_string("aaabccddd"))