#!/usr/bin/env python3
"""
CLI Mixin Pattern Experiments

Exploring different approaches to providing ergonomic CLI base functionality
while maintaining compatibility with Tyro and immutable dataclass semantics.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../sources'))

from appcore.cli import __
from appcore.cli import foundation as _foundation
from appcore.cli import preparation as _preparation
import tyro as _tyro


# Experiment 1: Basic Mixin with Common CLI Patterns
class CliMixin(__.immut.DataclassObject):
    """Mixin providing common CLI patterns and utilities."""

    configfile: __.typx.Optional[__.Path] = None
    inscription: _foundation.CliInscriptionControl = _foundation.CliInscriptionControl()

    async def prepare_globals(self) -> __.state.Globals:
        """Convenience method for preparing appcore globals."""
        async with __.ctxl.AsyncExitStack() as exits:
            nomargs: __.NominativeArguments = {}
            if self.configfile is not None:
                nomargs['configfile'] = self.configfile
            return await _preparation.prepare_from_cli(
                exits, self.inscription, **nomargs)

    async def execute_with_globals(self, command_func):
        """Execute a command function with prepared globals."""
        auxdata = await self.prepare_globals()
        # Assuming command_func takes (auxdata, display)
        if hasattr(self, 'display'):
            await command_func(auxdata, self.display)
        else:
            await command_func(auxdata)


# Experiment 2: Generic Mixin with Type Parameters
from typing import TypeVar, Generic

DisplayType = TypeVar('DisplayType', bound=_foundation.DisplayOptions)

class GenericCliMixin(__.immut.DataclassObject, Generic[DisplayType]):
    """Generic mixin that can work with different display types."""

    configfile: __.typx.Optional[__.Path] = None
    inscription: _foundation.CliInscriptionControl = _foundation.CliInscriptionControl()

    async def prepare_and_execute(self, command, display: DisplayType):
        """Prepare globals and execute command with proper display type."""
        async with __.ctxl.AsyncExitStack() as exits:
            nomargs: __.NominativeArguments = {}
            if self.configfile is not None:
                nomargs['configfile'] = self.configfile
            auxdata = await _preparation.prepare_from_cli(
                exits, self.inscription, **nomargs)
            await command(auxdata, display)


# Experiment 3: Protocol-based Mixin
class CliProtocolMixin(__.immut.DataclassObject):
    """Mixin using protocols for flexible typing."""

    configfile: __.typx.Optional[__.Path] = None
    inscription: _foundation.CliInscriptionControl = _foundation.CliInscriptionControl()

    # Define what we expect from the implementing class
    def get_display_options(self) -> _foundation.DisplayOptions:
        """Protocol method - must be implemented by concrete class."""
        raise NotImplementedError("Concrete class must implement get_display_options")

    async def run_command(self, command: _foundation.CliCommand):
        """Execute a command with proper preparation."""
        async with __.ctxl.AsyncExitStack() as exits:
            nomargs: __.NominativeArguments = {}
            if self.configfile is not None:
                nomargs['configfile'] = self.configfile
            auxdata = await _preparation.prepare_from_cli(
                exits, self.inscription, **nomargs)
            await command(auxdata, self.get_display_options())


# Experiment 4: Composition-based Helper
class CliExecutor:
    """Helper class for CLI execution - composition instead of inheritance."""

    def __init__(self, configfile=None, inscription=None):
        self.configfile = configfile
        self.inscription = inscription or _foundation.CliInscriptionControl()

    async def execute(self, command: _foundation.CliCommand, display: _foundation.DisplayOptions):
        """Execute command with preparation."""
        async with __.ctxl.AsyncExitStack() as exits:
            nomargs: __.NominativeArguments = {}
            if self.configfile is not None:
                nomargs['configfile'] = self.configfile
            auxdata = await _preparation.prepare_from_cli(
                exits, self.inscription, **nomargs)
            await command(auxdata, display)


# Test implementations to see how they work with Tyro

# Test 1: Using Basic Mixin
class ExampleCliWithMixin(CliMixin):
    """Example CLI using basic mixin."""

    display: _foundation.DisplayOptions = _foundation.DisplayOptions()
    verbose: bool = False

    async def __call__(self):
        """Execute the CLI."""
        # Can use mixin methods
        auxdata = await self.prepare_globals()
        print(f"Prepared globals for {auxdata.application.name}")


# Test 2: Using Protocol Mixin
class ExampleCliWithProtocol(CliProtocolMixin):
    """Example CLI using protocol mixin."""

    display: _foundation.DisplayOptions = _foundation.DisplayOptions()
    debug: bool = False

    def get_display_options(self) -> _foundation.DisplayOptions:
        """Implement the protocol method."""
        return self.display

    async def __call__(self):
        """Execute the CLI."""
        # Simulated command
        class MockCommand(_foundation.CliCommand):
            async def __call__(self, auxdata, display):
                print(f"Mock command executed with {type(display).__name__}")

        await self.run_command(MockCommand())


# Test 3: Using Composition
class ExampleCliWithComposition(__.immut.DataclassObject):
    """Example CLI using composition pattern."""

    display: _foundation.DisplayOptions = _foundation.DisplayOptions()
    configfile: __.typx.Optional[__.Path] = None
    debug: bool = False

    async def __call__(self):
        """Execute the CLI."""
        executor = CliExecutor(self.configfile)

        class MockCommand(_foundation.CliCommand):
            async def __call__(self, auxdata, display):
                print(f"Composition command executed")

        await executor.execute(MockCommand(), self.display)


if __name__ == "__main__":
    print("CLI Mixin Experiments")
    print("====================")

    print("\n1. Basic Mixin Approach:")
    print("   - Pros: Simple, provides common functionality")
    print("   - Cons: Fixed field names, potential conflicts")

    print("\n2. Generic Mixin Approach:")
    print("   - Pros: Type-safe, flexible display types")
    print("   - Cons: Complex typing, may confuse Tyro")

    print("\n3. Protocol Mixin Approach:")
    print("   - Pros: Flexible, clear contracts")
    print("   - Cons: Requires implementation, indirection")

    print("\n4. Composition Approach:")
    print("   - Pros: No inheritance conflicts, clear separation")
    print("   - Cons: More verbose, manual wiring")

    print("\nEach approach would need testing with Tyro for real-world viability.")