import importlib.util as u
mods = ['openfast_toolbox', 'pyFAST', 'pCrunch', 'rosco', 'weis',
        'numpy', 'pandas', 'matplotlib', 'scipy']
for m in mods:
    spec = u.find_spec(m)
    print(f"  {m}: {'yes' if spec else 'no'}")
