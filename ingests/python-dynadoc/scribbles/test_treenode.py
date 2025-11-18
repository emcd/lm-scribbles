#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dynadoc
from typing import Annotated

@dynadoc.with_docstring()
class TreeNode:
    ''' Binary tree node with parent and child references. '''
    value: Annotated[int, dynadoc.Doc("Node value")]
    parent: Annotated['TreeNode | None', dynadoc.Doc("Parent node reference")]
    left: Annotated['TreeNode | None', dynadoc.Doc("Left child node")]
    right: Annotated['TreeNode | None', dynadoc.Doc("Right child node")]

print("TreeNode.__doc__:")
print(repr(TreeNode.__doc__))