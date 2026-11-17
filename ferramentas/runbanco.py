import sys, json, importlib.util
sys.path.insert(0,'.')
from validate import check
for p in sys.argv[1:]:
    spec=importlib.util.spec_from_file_location("c",p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    T=m.TOPIC; print('==',T['name'],len(T['ex']),'exercícios', [sum(1 for x in T['ex'] if x['d']==k) for k in (0,1,2)]); check([T])
