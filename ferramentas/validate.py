"""Valida todas as soluções: solução de referência deve passar; editor vazio deve falhar.
Uso: python validate.py arquivo_topicos.json [indice_topico]"""
import sys, json, os, importlib.util, time
sys.setrecursionlimit(5000)
spec = importlib.util.spec_from_file_location("harness", os.path.join(os.path.dirname(__file__), "harness.py"))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)

def starter(x):
    return "# Escreva seu código abaixo.\n\n"

def check(topics, only=None):
    bad = 0
    for ti, t in enumerate(topics):
        if only is not None and ti != only: continue
        for ei, x in enumerate(t["ex"]):
            t0 = time.time()
            r = json.loads(H.run_json(json.dumps({"code": x["sol"], "setup": x.get("s", ""), "test": x["test"], "mode": "test", "imgs": False})))
            dt = time.time() - t0
            if not r["ok"]:
                bad += 1; print(f"FALHA SOL  [{t['name']}] {ei+1}. {x['t']}: {r.get('err')} {r.get('msg')} {r.get('fail')} | out={r['out'][:200]!r}")
            r2 = json.loads(H.run_json(json.dumps({"code": starter(x), "setup": x.get("s", ""), "test": x["test"], "mode": "test", "imgs": False})))
            if r2["ok"]:
                bad += 1; print(f"VAZIO PASSA [{t['name']}] {ei+1}. {x['t']}")
            if dt > 3: print(f"LENTO {dt:.1f}s [{t['name']}] {ei+1}")
            if len(x.get("h", [])) < 2: print(f"POUCAS DICAS [{t['name']}] {ei+1}")
    print("problemas:", bad)
    return bad

if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    topics = data if isinstance(data, list) else data["topics"]
    sys.exit(1 if check(topics, int(sys.argv[2]) if len(sys.argv) > 2 else None) else 0)
