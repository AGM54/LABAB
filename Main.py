from AST import construir_arbol_postfix, graficar_arbol,obtener_alfabeto,evaluate_tree
from Posfix import PostFix
from AFD import afd_directo,renderAfd,convertir_afn_a_afd ,afd_min
from AFN import createAFNF , renderAfn , evaluateString
#Realizar las conversiones
with open("./PostfixData.txt", 'r') as f:
    for i, line in enumerate(f):
        expresion_infix = line.strip()
        expresion_infix_direct = expresion_infix + '#'
        # Convertir la expresión infix a postfix
        
        expresion_postfix = PostFix(expresion_infix)
        # Construir el AST a partir de la expresión postfix
        
        arbol_root = construir_arbol_postfix(expresion_postfix)
        d_a = graficar_arbol(arbol_root)
        d_a.view(filename="AST from regrex")
 
        init,end= createAFNF(nodo=arbol_root)
        d_anf = renderAfn(init,end)
        d_anf.view(filename="AFN from regrex")

        afd = convertir_afn_a_afd(init,end)
        d_afd = renderAfd(afd["root"])
        d_afd.view(filename="AFD from regrex")

        #afd directo
        expresion_infix_direct = expresion_infix + '#'
        expresion_postfix_direct = PostFix(expresion_infix_direct)
        arbol_root_direct = construir_arbol_postfix(expresion_postfix_direct)
        
        d_a_direct = graficar_arbol(arbol_root_direct)
        d_a_direct.view(filename="AST from regrex for direct method")
 
        evaluate_tree(arbol_root_direct)

        afd_direct = afd_directo(arbol_root_direct)
        d_afd_direct = renderAfd(afd_direct)
        d_afd_direct.view(filename="AFD direct from regrex")

        min_dfa = afd_min(afd)
        d_min_dfa = renderAfd(min_dfa)
        d_min_dfa.view(filename="AFD MIN from regrex")

        evaluateString(line.strip(),init, end,afd["root"] ,afd["alfabeto"])
        i+=1
