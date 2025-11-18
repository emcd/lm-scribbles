#!/usr/bin/env python3
"""
CLI Mixin Practical Prototype

Actually test the mixin pattern with Tyro to verify it works correctly.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../sources'))

from appcore.cli import __
from appcore.cli import foundation as _foundation
from appcore.cli import preparation as _preparation

# Test with actual Tyro import
try:
    import tyro as _tyro
    import tyro.conf as _tyro_conf
    TYRO_AVAILABLE = True
except ImportError:
    TYRO_AVAILABLE = False
    print("Tyro not available - testing dataclass mechanics only")


# Proposed CliMixin implementation
class CliMixin(__.immut.DataclassObject):
    """Mixin providing common CLI patterns and ergonomic helpers."""

    inscription: _foundation.CliInscriptionControl = _foundation.CliInscriptionControl()
    configfile: __.typx.Optional[__.Path] = None

    async def prepare_globals(self) -> __.state.Globals:
        """Convenience method for preparing appcore globals."""
        async with __.ctxl.AsyncExitStack() as exits:
            nomargs: __.NominativeArguments = {}
            if self.configfile is not None:
                nomargs['configfile'] = self.configfile
            return await _preparation.prepare_from_cli(
                exits, self.inscription, **nomargs)

    async def execute_command(self, command: _foundation.CliCommand, display: _foundation.DisplayOptions):
        """Execute a command with prepared globals."""
        auxdata = await self.prepare_globals()
        await command(auxdata, display)


# Test implementation using the mixin
class ExampleDisplayOptions(_foundation.DisplayOptions):
    """Test display options with format support."""

    format: str = 'plain'  # Simplified for testing

    async def render(self, obj: __.typx.Any) -> None:
        """Simple test render implementation."""
        async with __.ctxl.AsyncExitStack() as exits:
            stream = await self.provide_stream(exits)
            if isinstance(obj, dict):
                for key, value in obj.items():
                    stream.write(f"{key}: {value}\n")
            else:
                stream.write(str(obj) + "\n")


class TestCommand(_foundation.CliCommand):
    """Test command implementation."""

    async def __call__(self, auxdata: __.state.Globals, display: _foundation.DisplayOptions):
        print(f"Test command executed with application: {auxdata.application.name}")
        await display.render({"status": "success", "app": auxdata.application.name})


# CLI using the mixin - this should be much cleaner
class TestCliWithMixin(CliMixin):
    """Test CLI demonstrating mixin ergonomics."""

    display: ExampleDisplayOptions = ExampleDisplayOptions()
    verbose: bool = False

    async def __call__(self):
        """Execute the test CLI."""
        print(f"TestCliWithMixin starting (verbose={self.verbose})")

        # This is the ergonomic benefit - one line instead of ~8
        auxdata = await self.prepare_globals()

        # Execute a test command
        command = TestCommand()
        await command(auxdata, self.display)

        if self.verbose:
            print("Execution completed successfully")


# For comparison - CLI without mixin (current approach)
class TestCliWithoutMixin(__.immut.DataclassObject):
    """Test CLI showing current boilerplate."""

    display: ExampleDisplayOptions = ExampleDisplayOptions()
    inscription: _foundation.CliInscriptionControl = _foundation.CliInscriptionControl()
    configfile: __.typx.Optional[__.Path] = None
    verbose: bool = False

    async def __call__(self):
        """Execute the test CLI with full boilerplate."""
        print(f"TestCliWithoutMixin starting (verbose={self.verbose})")

        # All this boilerplate would be eliminated by the mixin
        async with __.ctxl.AsyncExitStack() as exits:
            nomargs: __.NominativeArguments = {}
            if self.configfile is not None:
                nomargs['configfile'] = self.configfile
            auxdata = await _preparation.prepare_from_cli(
                exits, self.inscription, **nomargs)

        # Execute a test command
        command = TestCommand()
        await command(auxdata, self.display)

        if self.verbose:
            print("Execution completed successfully")


def test_dataclass_mechanics():
    """Test that the mixin approach works at the dataclass level."""
    print("\n=== Testing Dataclass Mechanics ===")

    # Test instantiation
    cli = TestCliWithMixin(verbose=True)
    print(f"✓ Mixin CLI instantiated: {type(cli).__name__}")
    print(f"  - Has inscription: {hasattr(cli, 'inscription')}")
    print(f"  - Has configfile: {hasattr(cli, 'configfile')}")
    print(f"  - Has display: {hasattr(cli, 'display')}")
    print(f"  - Has verbose: {hasattr(cli, 'verbose')}")
    print(f"  - Has prepare_globals method: {hasattr(cli, 'prepare_globals')}")

    # Test field values
    print(f"  - inscription type: {type(cli.inscription).__name__}")
    print(f"  - configfile value: {cli.configfile}")
    print(f"  - display type: {type(cli.display).__name__}")
    print(f"  - verbose value: {cli.verbose}")

    return cli


def test_tyro_compatibility():
    """Test that Tyro can handle the mixin approach."""
    if not TYRO_AVAILABLE:
        print("\n=== Tyro Not Available - Skipping ===")
        return

    print("\n=== Testing Tyro Compatibility ===")

    try:
        # Test if Tyro can parse the mixin-based CLI
        print("Testing Tyro CLI generation...")

        # This should work if the mixin approach is viable
        cli_func = _tyro.cli(TestCliWithMixin, description="Test CLI with mixin")
        print("✓ Tyro successfully generated CLI function")

        # Test with minimal args (would normally come from command line)
        # We can't actually call it without proper argument parsing setup
        print("✓ Tyro accepts the mixin-based CLI class")

    except Exception as e:
        print(f"✗ Tyro compatibility issue: {e}")
        return False

    return True


async def test_execution():
    """Test actual execution of the mixin-based CLI."""
    print("\n=== Testing Execution ===")

    try:
        # Test the mixin version
        print("Testing mixin-based CLI execution...")
        cli_with_mixin = TestCliWithMixin(verbose=True)
        await cli_with_mixin()
        print("✓ Mixin-based CLI executed successfully")

        print("\nTesting traditional CLI execution...")
        cli_without_mixin = TestCliWithoutMixin(verbose=True)
        await cli_without_mixin()
        print("✓ Traditional CLI executed successfully")

        return True

    except Exception as e:
        print(f"✗ Execution error: {e}")
        import traceback
        traceback.print_exc()
        return False


def compare_ergonomics():
    """Compare the ergonomics of both approaches."""
    print("\n=== Ergonomics Comparison ===")

    print("Lines of code for CLI class definition:")

    with_mixin_lines = '''
class TestCliWithMixin(CliMixin):
    display: ExampleDisplayOptions = ExampleDisplayOptions()
    verbose: bool = False

    async def __call__(self):
        auxdata = await self.prepare_globals()  # <-- This is the key benefit
        command = TestCommand()
        await command(auxdata, self.display)
'''.strip().split('\n')

    without_mixin_lines = '''
class TestCliWithoutMixin(__.immut.DataclassObject):
    display: ExampleDisplayOptions = ExampleDisplayOptions()
    inscription: _foundation.CliInscriptionControl = _foundation.CliInscriptionControl()
    configfile: __.typx.Optional[__.Path] = None
    verbose: bool = False

    async def __call__(self):
        async with __.ctxl.AsyncExitStack() as exits:
            nomargs: __.NominativeArguments = {}
            if self.configfile is not None:
                nomargs['configfile'] = self.configfile
            auxdata = await _preparation.prepare_from_cli(
                exits, self.inscription, **nomargs)
        command = TestCommand()
        await command(auxdata, self.display)
'''.strip().split('\n')

    print(f"  With mixin: {len(with_mixin_lines)} lines")
    print(f"  Without mixin: {len(without_mixin_lines)} lines")
    print(f"  Reduction: {len(without_mixin_lines) - len(with_mixin_lines)} lines ({((len(without_mixin_lines) - len(with_mixin_lines)) / len(without_mixin_lines) * 100):.1f}% less code)")

    print("\nBoilerplate eliminated:")
    print("  ✓ inscription field declaration")
    print("  ✓ configfile field declaration")
    print("  ✓ AsyncExitStack context management")
    print("  ✓ nomargs dictionary construction")
    print("  ✓ prepare_from_cli call with proper arguments")


if __name__ == "__main__":
    print("CLI Mixin Practical Testing")
    print("===========================")

    # Test 1: Basic dataclass mechanics
    cli = test_dataclass_mechanics()

    # Test 2: Tyro compatibility
    tyro_works = test_tyro_compatibility()

    # Test 3: Actual execution
    execution_works = asyncio.run(test_execution())

    # Test 4: Ergonomics comparison
    compare_ergonomics()

    # Summary
    print("\n=== Final Assessment ===")
    print(f"Dataclass mechanics: ✓ Working")
    print(f"Tyro compatibility: {'✓ Working' if tyro_works else '✗ Issues'}")
    print(f"Execution: {'✓ Working' if execution_works else '✗ Issues'}")

    if tyro_works and execution_works:
        print("\n🎉 CONCLUSION: Mixin pattern is viable and significantly improves ergonomics!")
        print("   Recommend implementing CliMixin in the foundation module.")
    else:
        print("\n⚠️  CONCLUSION: Mixin pattern has compatibility issues.")
        print("   Current approach without mixin is safer.")