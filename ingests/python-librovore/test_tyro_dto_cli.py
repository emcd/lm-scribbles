#!/usr/bin/env python3
# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

''' Test Tyro CLI generation with DTO vs individual parameters. '''

import tyro
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated


class MatchMode(Enum):
    EXACT = "exact"
    REGEX = "regex"
    FUZZY = "fuzzy"


class ExploreFilters(BaseModel):
    ''' Filters for explore function. '''
    domain: str = ""
    role: str = ""
    priority: str = ""
    match_mode: MatchMode = MatchMode.FUZZY
    fuzzy_threshold: int = 50


def explore_with_dto(
    source: str,
    query: str,
    filters: ExploreFilters = ExploreFilters(),
    max_objects: int = 5,
    include_documentation: bool = True,
) -> None:
    ''' Explore function using DTO for filters. '''
    print(f"DTO Approach:")
    print(f"  Source: {source}")
    print(f"  Query: {query}")
    print(f"  Domain: {filters.domain}")
    print(f"  Role: {filters.role}")
    print(f"  Priority: {filters.priority}")
    print(f"  Match Mode: {filters.match_mode.value}")
    print(f"  Fuzzy Threshold: {filters.fuzzy_threshold}")
    print(f"  Max Objects: {max_objects}")
    print(f"  Include Documentation: {include_documentation}")


def explore_with_params(
    source: str,
    query: str,
    domain: str = "",
    role: str = "",
    priority: str = "",
    match_mode: MatchMode = MatchMode.FUZZY,
    fuzzy_threshold: int = 50,
    max_objects: int = 5,
    include_documentation: bool = True,
) -> None:
    ''' Explore function using individual parameters. '''
    print(f"Individual Parameters Approach:")
    print(f"  Source: {source}")
    print(f"  Query: {query}")
    print(f"  Domain: {domain}")
    print(f"  Role: {role}")
    print(f"  Priority: {priority}")
    print(f"  Match Mode: {match_mode.value}")
    print(f"  Fuzzy Threshold: {fuzzy_threshold}")
    print(f"  Max Objects: {max_objects}")
    print(f"  Include Documentation: {include_documentation}")


if __name__ == "__main__":
    import sys
    
    print("Testing Tyro CLI generation...\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "dto":
        print("=== DTO APPROACH ===")
        # Remove the mode selector from argv before passing to tyro
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        tyro.cli(explore_with_dto)
    elif len(sys.argv) > 1 and sys.argv[1] == "params":
        print("=== INDIVIDUAL PARAMETERS APPROACH ===")
        # Remove the mode selector from argv before passing to tyro
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        tyro.cli(explore_with_params)
    else:
        print("Usage:")
        print("  python test_tyro_dto_cli.py dto --help     # Test DTO approach")
        print("  python test_tyro_dto_cli.py params --help  # Test individual params")
        print()
        print("Example calls:")
        print("  # DTO approach:")
        print("  python test_tyro_dto_cli.py dto --source 'https://example.com' --query 'Result' --filters.domain py --filters.match-mode FUZZY")
        print()
        print("  # Individual parameters:")
        print("  python test_tyro_dto_cli.py params --source 'https://example.com' --query 'Result' --domain py --match-mode FUZZY")