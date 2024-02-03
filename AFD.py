from graphviz import Digraph


class NodoAFD:
    def init(self, id, estado_final=False):
        self.id = id
        self.estado_final = estado_final
        self.transiciones = {}


def convertir_arbol_a_afd(arbol):
    afd = AFD()
    estado_actual = afd.crear_estado()
    _convertir_arbol_a_afd(arbol, estado_actual, afd)
    return afd


def _convertir_arbol_a_afd(arbol, estado_actual, afd):
    if arbol is None:
        return

    if isinstance(arbol, str):
        # Operando
        afd.agregar_transicion(estado_actual, afd.estado_final, arbol)
    else:
        # Operador
        nuevo_estado = afd.crear_estado()
        afd.agregar_transicion(estado_actual, nuevo_estado, arbol.valor)
        _convertir_arbol_a_afd(arbol.izquierda, nuevo_estado, afd)
        _convertir_arbol_a_afd(arbol.derecha, nuevo_estado, afd)


class AFD:
    def init(self):
        self.estados = {}
        self.estado_inicial = None
        self.estado_final = None

    def crear_estado(self, estado_final=False):
        nuevo_estado = NodoAFD(len(self.estados), estado_final)
        self.estados[nuevo_estado.id] = nuevo_estado
        if not self.estado_inicial:
            self.estado_inicial = nuevo_estado
        if estado_final:
            self.estado_final = nuevo_estado
        return nuevo_estado

    def agregar_transicion(self, estado_origen, estado_destino, etiqueta):
        transiciones = self.estados[estado_origen.id].transiciones
        if etiqueta not in transiciones:
            transiciones[etiqueta] = []
        transiciones[etiqueta].append(estado_destino)

    def graficar(self):
        dot = Digraph(format='png')
        for estado in self.estados.values():
            dot.node(str(estado.id), label=f"{estado.id}" + ("*" if estado.estado_final else ""))
            for etiqueta, estados_destino in estado.transiciones.items():
                for estado_destino in estados_destino:
                    dot.edge(str(estado.id), str(estado_destino.id), label=etiqueta)
        return dot