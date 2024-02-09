'''Implementacion para conversión a AFD a partir del AFN'''
from collections import deque
from AFN import AFNnodo
from AST import NodoAST
from graphviz import Digraph


epsi = 'ε'


#clase representatnte del nodo
class AFDNode:
    contador = 0
    def __init__(self, subset = set()):
        self.nombre = f's{AFDNode.contador}'
        self.transiciones = {}
        self.isAceptacion = False
        self.subset = subset
        AFDNode.contador += 1

    def agregar_transicion(self, simbolo, estado_destino):
        if simbolo in self.transiciones.keys():
            if estado_destino not in self.transiciones[simbolo]:    
                self.transiciones[simbolo].append(estado_destino)
        else:
            self.transiciones[simbolo] = [estado_destino]

'''metodo que recibe de input los estados finales e iniciales del AFN
    estado_inical, estado_final nodos AFN
    simbolos = simbolos del alfabeto para la gramatica
'''


'''obtenner la cerradura epsilon del estado s0'''

def afd_directo(nodo_ast:NodoAST):
    AFDNode.contador = 0
    followPosTable = NodoAST.followPos
    indexDict = NodoAST.posdict
    States = list() 
    acceptances = []
    #obtener el pos final
    for pos , _set in followPosTable.items():
        if len(_set) == 0:
            acceptances.append(pos)


    #crear el primer estado a partir del top en follow pos
    S0 = AFDNode(followPosTable['1'])
    if NodoAST.index_pos in S0.subset:
        S0.isAceptacion = True
    States.append(S0)
    
    for D in States:
        #recorrer con cada symbolo
        for symbol , indexes in indexDict.items():
            U = set()
            _S = set(indexes)

            #obtener las pos mediante intersección de conjuntos
            occurences = D.subset & _S 
            if len(occurences) > 0:
                for pos in occurences:
                    #obtetenr todos los follow pos relacionados al simbolo
                    U = U.union(followPosTable[str(pos)])
                
                #verificar si existe
                if any(state.subset == U for state in States):
                    for state in States:
                        if state.subset == U:
                            if symbol != '#':
                                D.agregar_transicion(symbol,state)
                else:
                    #crear uno nuevo
                    _U = AFDNode(U)
                    if NodoAST.index_pos - 1 in U:
                        _U.isAceptacion = True
                    States.append(_U)
                    if symbol != '#':
                        D.agregar_transicion(symbol,_U)

    return S0

def ceraddura_e(S):
    e = set()
    for state in S:
        e = e.union(_cerradure_e(state))
    return e

def _cerradure_e(estado:AFNnodo,checked = None):
    if checked is None:
        checked = set()
    if estado in checked:
        return
    
    checked.add(estado)

    if epsi in estado.transiciones.keys():
        for next in estado.transiciones[epsi]:
            _cerradure_e(next,checked)
    
    return checked

def get_symbol_transitions(estados, simbolo):
    visited = set()
    #obtener los estados con el simbolo 
    for estado in estados:
        if simbolo in estado.transiciones.keys():
            visited = visited.union(estado.transiciones[simbolo])
    
    #aplicar cerradura lambda
    return visited
        
def get_simbolos(afn_node: AFNnodo,simbolos_entrada= set(), estados_visitados= []):
    if afn_node and afn_node.nombre not in estados_visitados:
        estados_visitados.append(afn_node.nombre)
        for simbolo in afn_node.transiciones:
            if simbolo != 'ε' and simbolo not in simbolos_entrada:  # Exclude epsilon transitions
                simbolos_entrada.add(simbolo)
            for estado in afn_node.transiciones[simbolo]:
                get_simbolos(estado,simbolos_entrada,estados_visitados)
    return simbolos_entrada

def convertir_afn_a_afd(afn_node_inicial, afn_node_final):
    AFDNode.contador = 0 #colocar el contador siempre en 0
    simbolos_entrada = get_simbolos(afn_node_inicial) 
    estados_afd = []
    accepted_afd = []
    s0 = ceraddura_e(set({afn_node_inicial}))
    S0 = AFDNode(s0)

    if any(node.nombre == afn_node_final.nombre for node in s0):
        S0.isAceptacion = True
    estados_afd.append(S0)
    
    for estado in estados_afd:
        for entrada in simbolos_entrada:
            subc = ceraddura_e(get_symbol_transitions(estado.subset, entrada))
            
            if any(set(estado_afd.subset) == set(subc) for estado_afd in estados_afd):
                for estado_afd in estados_afd:
                    if set(estado_afd.subset) == set(subc):
                        estado.agregar_transicion(entrada, estado_afd)
                        break
            else:
                if len(subc) > 0:
                    new_subc = AFDNode(subc)
                    estado.agregar_transicion(entrada, new_subc)
                    if any(node.nombre == afn_node_final.nombre for node in subc):
                        new_subc.isAceptacion = True
                        accepted_afd.append(new_subc)
                    estados_afd.append(new_subc)

    return {"root" : estados_afd[0] , "alfabeto" : simbolos_entrada,"estados":set(estados_afd),"acceptance":set(accepted_afd)}

def renderAfd(root):
    dot = Digraph(format='png')
    dot.attr(rankdir='LR')  # Establecer la orientación horizontal
    visited = set()  # Crear un conjunto para llevar un registro de estados visitados
    dot.node('_start', shape='point')
    dot.edge('_start', root.nombre,)
    _renderAfd(dot, root ,visited)
    return dot

def _renderAfd(dot, estado , visited):
    if estado:
        if estado in visited:
            return

        visited.add(estado)

        if estado.isAceptacion:
            dot.node(estado.nombre, label=estado.nombre, shape='doublecircle')
        else:
            dot.node(estado.nombre, label=estado.nombre, shape='circle')

        for entrada, destino in estado.transiciones.items():
            for dest in destino:
                dot.edge(estado.nombre, dest.nombre, label=entrada)

        for entrada, destino in estado.transiciones.items():
            for dest in destino:
                _renderAfd(dot, dest, visited)

def afd_min(afd:dict):
    #particiones iniciales
    #p0 : estados de aceptacion , p1: no aceptacion
    partitions = [afd["acceptance"],afd["estados"]-afd["acceptance"]]
    
    isNewpartition = True
    
    #REALIZAR PARTICIONES
    #realizar iteraciones en búsqueda de particion
    #detener si la nueva particion es igual a la inical
    while isNewpartition:
        next_partitions = [] #siguientes particiones 
        for partition in partitions:
            next_partition = {} #subgrupos de la siguiente iteracion
            for state in partition: #hallar transiciones de los estados por token
                state_transitions = []
                for token in afd["alfabeto"]:
                    token_transition = state.transiciones.get(token ,[]) #todos los estados que hay desde el token, si no existe, dar lista vacía
                    found_grupo = False
                    #ver a cual grupo pertenece cada estado de transicion
                    for s in partitions:
                        for token_s in token_transition:
                            if token_s in s:
                                found_grupo = True
                                state_transitions.append((token, tuple(s))) #añadir como tupla el token y estados de trancision hallados
                                #se halló el grupo de pertenencia
                                break
                        #se halló el grupo, no revisar los siguientes
                        if found_grupo:
                            break

                    #no existe el grupo  a trancisionar
                    if not found_grupo:
                        state_transitions.append((token, None))
                #convertir a tupla , donde si mismo es llave y valor, 
                #esto para las demás iteraciones poder accesarlo como si fuese llave el subconjunto
                state_transitions = tuple(state_transitions)
                #agregar el subconjunto
                next_partition.setdefault(state_transitions, set()).add(state)
            next_partitions.extend(next_partition.values()) #solo los valores ( el subconjunto es llave y valor)
        if next_partitions == partitions:
            break
        else:
            partitions = next_partitions
    
    #BUSCAR LAS TRANCISIONES PARA CADA ESTADO
    AFDNode.contador = 0

    state_transitions = {}

    min_states = []
    min_root = None
    for sub in partitions:
        sub_state = AFDNode(sub)
        
        #si alguno del subconjunto es aceptacion , todo el conjunto lo es
        if any(state.isAceptacion for state in sub):
            sub_state.isAceptacion = True

        #si el inicial está en el conjunto, el conjunto es el inicial
        if afd["root"] in sub:
            min_root = sub_state

        min_states.append(sub_state)
        
        #relacionar cada elemento con el nuevo
        for state in sub:
            state_transitions[state] = sub_state

    #recorrer cada nodo afd para relacionar los elementos de cada uno
    for state,min_state in state_transitions.items():
        #revisar cada transición 
        for token, destination in state.transiciones.items():
            for dest in destination:
                min_state.agregar_transicion(token,state_transitions[dest])

    return min_root

