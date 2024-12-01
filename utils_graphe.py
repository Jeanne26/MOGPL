
def graphe_1():
    """Retourne le graphe de gauche de l'exemple 2

    Returns:
        tuple: G: V (list): ensemble des sommets du graphe
                  A (dict): ensemble des aretes du graphe
    """
    #liste des sommets
    V= ["a","b","c","d","e","f"]
    #dictionnaire des aretes
    A = dict()
    A[("a","b")]= [4,3]
    A[("a","c")]= [5,1]
    A[("b","c")]= [2,1]
    A[("b","e")]= [2,2]
    A[("b","f")]= [7,5]
    A[("b","d")]= [1,4]
    A[("c","e")]= [2,7]
    A[("c","d")]= [5,1]
    A[("d","f")]= [3,2]
    A[("e","f")]= [5,2]

    return (V, A)

def graphe_2():
    """Retourne le graphe de gauche de l'exemple 2

    Returns:
        tuple: G: V (list): ensemble des sommets du graphe
                  A (dict): ensemble des aretes du graphe
    """
    #liste des sommets
    V= ["a","b","c","d","e","f","g"]
    #dictionnaire des aretes
    A = dict()
    A[("a","b")]= [5, 3]
    A[("a","c")]= [10, 4]
    A[("a","d")]= [2, 6]
    A[("b","d")]= [1, 3]
    A[("b","c")]= [4, 2]
    A[("b","e")]= [4, 6]
    A[("c","e")]= [3, 1]
    A[("c","f")]= [1, 2]
    A[("d","c")]= [1, 4]
    A[("d","f")]= [3, 5]
    A[("e","g")]= [1, 1]
    A[("f","g")]= [1, 1]


    return (V, A)


def get_out(G,s):
    """retourne la liste de toutes les aretes sortantes de s

    Args:
        s (char): sommet
        G (dict) : graphe

    Returns:
        out (list) : liste de toutes les aretes sortantes de s
    """
    (V,A) = G
    out_s= []
    for (i,j) in A.keys():
        if i==s:
            out_s.append((i,j))

    return out_s





def get_in(G,s):
    """retourne la liste de toutes les aretes entrantes de s

    Args:
        s (char): sommet
        G (dict) : graphe

    Returns:
        out (list) : liste de toutes les aretes entrantes de s
    """
    (V,A) = G
    out_s= []
    for (i,j) in A.keys():
        if j==s:
            out_s.append((i,j))

    return out_s




