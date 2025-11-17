#!/usr/bin/env python3

from librovore.xtnsmgr import importation
try:
    module = importation.import_processor_module('librovore.structures.mkdocs')
    print('MkDocs module imported successfully:', module)
    print('Has register function:', hasattr(module, 'register'))
    if hasattr(module, 'register'):
        print('Calling register...')
        module.register({})
        print('Register completed successfully')
except Exception as e:
    print('Error importing MkDocs module:', e)
    import traceback
    traceback.print_exc()