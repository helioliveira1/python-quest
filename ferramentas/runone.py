import sys, json, importlib.util
sys.path.insert(0,'.')
from validate import check
for p in sys.argv[1:]:
    spec=importlib.util.spec_from_file_location("c",p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    T=m.TOPIC; assert len(T['ex'])==15, (p,len(T['ex']))
    print('==',T['name']); check([T])
