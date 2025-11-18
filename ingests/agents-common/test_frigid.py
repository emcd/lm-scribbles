#!/usr/bin/env python3

import frigid

print("=== frigid.Dataclass ===")
help(frigid.Dataclass)
print("\n=== frigid.DataclassObject ===")
help(frigid.DataclassObject)
print("\n=== All frigid attributes ===")
print([attr for attr in dir(frigid) if 'Dataclass' in attr])