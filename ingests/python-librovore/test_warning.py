#!/usr/bin/env python3

import warnings
warnings.filterwarnings('error', category=RuntimeWarning, module='dynadoc')

try:
    import librovore
    print('Import successful')
except Exception as e:
    print(f'Error during import: {e}')
    import traceback
    traceback.print_exc()