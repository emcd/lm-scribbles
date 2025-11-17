import sphinxmcps.processors.sphinx as module

result = module.normalize_base_url('/home/user/test.inv')
print(f'Result: {result}')

result2 = module.normalize_base_url('/home/user/objects.inv')  
print(f'Result2: {result2}')

result3 = module.normalize_base_url('https://docs.python.org/3/objects.inv')
print(f'Result3: {result3}')