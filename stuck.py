stack = []

#push 
stack.append(10)
stack.append(20)
stack.append(30)

print("stack:", stack)


#Contoh Penggunaan Stack Reverse String
def reverse_string(text):
    stack = []

    for char in text:
        stack.append(char)
    
    reversed_text = ""
    while stack:
        reversed_text += stack.pop()

    return reversed_text

print(reverse_string("Pemimpin Di Esok Hari, Adakah yang Cukup Mampu"))


#Penggunaan Stack untuk Cek Kurung Seimbang
def is_balance(expression):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack.pop() != pairs[char]:
                return False

    return len(stack) == 0

print(is_balance("(a+b)")) #True