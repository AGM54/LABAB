from graphviz import Digraph
class NodoAST:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


def construir_arbol_postfix(expresion):
    pila = []
    i = 0
    while i < len(expresion):
        caracter = expresion[i]
        if caracter in ['*', '+', '?', '.', '|']:
            nodo = NodoAST(caracter)
            nodo.derecha = pila.pop()
            if caracter != '*':
                nodo.izquierda = pila.pop()
            pila.append(nodo)
        else:
            if caracter == '\\':
                # Handle escape sequence
                if i + 1 < len(expresion):
                    i += 1  # Move to the next character
                    escape_sequence = caracter + expresion[i]
                    nodo = NodoAST(escape_sequence)
            else:
                nodo = NodoAST(caracter)
            pila.append(nodo)

        i += 1  # Move to the next character
    return pila[0] if pila else None


# Función para mostrar el árbol utilizando Graphviz
def graficar_arbol(nodo):
    dot = Digraph(format='png')
    _graficar_arbol(dot, nodo)
    return dot

def _graficar_arbol(dot, nodo):
    if nodo:
        dot.node(str(id(nodo)), label=nodo.valor)
        if nodo.izquierda:
            dot.node(str(id(nodo.izquierda)), label=nodo.izquierda.valor)
            dot.edge(str(id(nodo)), str(id(nodo.izquierda)))
            _graficar_arbol(dot, nodo.izquierda)
        if nodo.derecha:
            dot.node(str(id(nodo.derecha)), label=nodo.derecha.valor)
            dot.edge(str(id(nodo)), str(id(nodo.derecha)))
            _graficar_arbol(dot, nodo.derecha)
