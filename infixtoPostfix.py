def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
    stack = []  # Pila para almacenar operadores
    postfix = []  # Lista para construir la salida postfix
    # Convertir la expresión en una lista para manejar mejor los operandos y operadores
    expression = list(expression)
    for char in expression:
        if char.isalnum():  # Si es un operando, añadir directamente a la salida
            postfix.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Remover el '(' abierto de la pila
        else:
            # Mientras haya un operador de mayor o igual precedencia en la cima de la pila, sacarlo
            while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                postfix.append(stack.pop())
            stack.append(char)
    # Vaciar cualquier operador restante en la pila
    while stack:
        postfix.append(stack.pop())
    return ''.join(postfix)


expression = "a+b*"
postfix_expression = infix_to_postfix(expression)
print("Expresión en notación postfix:", postfix_expression)
