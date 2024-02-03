from AST import construir_arbol_postfix, graficar_arbol
from Posfix import PostFix
# Asegúrate de que AFD y las funciones relacionadas están definidas correctamente
from AFD import AFD, convertir_arbol_a_afd
import os

# Especifica la ruta al ejecutable de Graphviz manualmente
os.environ["PATH"] += os.pathsep + 'C:/Users/marce/Downloads/windows_10_msbuild_Release_graphviz-9.0.0-win32/Graphviz/bin'

# Realizar las conversiones
with open("./PostfixData.txt", 'r') as f:
    for i, line in enumerate(f):
        expresion_infix = line.strip()
        # Convertir la expresión infix a postfix
        expresion_postfix = PostFix(expresion_infix)
        # Construir el AST a partir de la expresión postfix
        arbol = construir_arbol_postfix(expresion_postfix)

        # Usar la función convertir_arbol_a_afd para generar el AFD directamente desde el AST
        afd = convertir_arbol_a_afd(arbol)
        
        # Graficar y visualizar el AFD generado
        afd_grafico = afd.graficar()
        afd_grafico.view(filename=f'AFD_directo_{i}')
