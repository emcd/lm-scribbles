#!/usr/bin/env python3

try:
    import appcore.cli
    print('Direct import works!')
    print('DisplayOptions available:', hasattr(appcore.cli, 'DisplayOptions'))
    if hasattr(appcore.cli, 'DisplayOptions'):
        print('DisplayOptions class:', appcore.cli.DisplayOptions)
except Exception as e:
    print('Error:', e)