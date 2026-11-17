def E(d, t, p, sol, test, h, s=""):
    """Exercício do Banco: d = 0 fácil, 1 médio, 2 desafio."""
    return dict(d=d, t=t, p=p, s=s, sol=sol, test=test, h=h)

def ENT(*valores):
    """Gera o setup com as entradas simuladas do input()."""
    return "entradas = " + repr([str(v) for v in valores])
