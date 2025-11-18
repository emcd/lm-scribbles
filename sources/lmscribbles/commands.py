# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Commands for CLI interface. '''


from hashlib import sha256 as _sha256
from json import dumps as _json_dumps
from shutil import copy2 as _copy_file

from . import __
from . import exceptions as _exceptions


# Type Aliases
Location: __.typx.TypeAlias = str | __.Path  # Path-like
PathPair: __.typx.TypeAlias = tuple[ __.Path, __.Path ]
# Base path and file path tuple for preserving directory structure
SourceFileTuple: __.typx.TypeAlias = tuple[ __.Path, __.Path ]


def _discover_source_files(
    source_paths: __.cabc.Sequence[ Location ],
) -> __.cabc.Iterator[ SourceFileTuple ]:
    ''' Discovers all source files with their base paths.

        Returns tuples of (base_path, file_path) where base_path is used
        to calculate relative paths for preserving directory structure.
    '''
    for location in source_paths:
        path = __.Path( location )
        if path.is_file( ):
            yield ( path.parent, path )
        elif path.is_dir( ):
            for item in path.rglob( '*' ):
                if item.is_file( ):
                    yield ( path, item )
        else:
            raise _exceptions.FileIngestionFailure( str( path ) )


def _compute_hash( file_path: __.Path ) -> str:
    ''' Computes SHA-256 hash of file contents. '''
    hasher = _sha256( )
    try:
        with file_path.open( 'rb' ) as file:
            while chunk := file.read( 8192 ):
                hasher.update( chunk )
    except OSError as exception:
        raise _exceptions.DuplicateDetectionFailure(
            str( file_path ) ) from exception
    return hasher.hexdigest( )


async def _check_secrets(
    file_path: __.Path,
    warnings: list[ str ],
) -> None:
    ''' Checks file for secrets and adds warnings. '''
    try:
        from detect_secrets import SecretsCollection
        from detect_secrets.settings import default_settings
        secrets = SecretsCollection( )
        with default_settings( ):
            secrets.scan_file( str( file_path ) )
        if secrets.data:
            secret_count = sum(
                len( file_secrets )
                for file_secrets in secrets.data.values( )
            )
            msg = f"Secrets in {file_path}: {secret_count} found"
            warnings.append( msg )
    except Exception as exception:
        raise _exceptions.SecretDetectionFailure(
            str( file_path ) ) from exception


async def _process_file(  # noqa: PLR0913
    base_path: __.Path,
    source: __.Path,
    target_dir: __.Path,
    warnings: list[ str ],
    check_secrets: bool,
    dry_run: bool,
) -> __.Path | PathPair | None:
    ''' Processes single file for ingestion.

        Preserves directory structure relative to base_path.

        Returns:
            - Path: Successfully copied to this destination
            - PathPair: Renamed due to duplicate
            - None: Skipped (duplicate content)
    '''
    if check_secrets:
        await _check_secrets( source, warnings )
    try:
        relative_path = source.relative_to( base_path )
    except ValueError as exception:
        raise _exceptions.FileIngestionFailure( str( source ) ) from exception
    target_path = target_dir / relative_path
    if not dry_run:
        target_path.parent.mkdir( parents = True, exist_ok = True )
    if target_path.exists( ):
        source_hash = _compute_hash( source )
        target_hash = _compute_hash( target_path )
        if source_hash == target_hash:
            return None
        stem = target_path.stem
        suffix = target_path.suffix
        hash_suffix = source_hash[ :6 ]
        renamed_path = target_path.parent / f"{stem}-{hash_suffix}{suffix}"
        if not dry_run:
            _copy_file( source, renamed_path )
        return ( target_path, renamed_path )
    if not dry_run:
        _copy_file( source, target_path )
    return target_path


class IngestResult( __.immut.DataclassObject ):
    ''' Results of ingestion operation. '''

    copied: __.immut.Dictionary[ __.Path, __.Path ]
    skipped: __.immut.Dictionary[ __.Path, str ]
    renamed: __.immut.Dictionary[ __.Path, PathPair ]
    failed: __.immut.Dictionary[ __.Path, str ]
    warnings: __.cabc.Sequence[ str ]

    def render_as_json( self ) -> str:
        ''' Renders result as JSON string. '''
        data: dict[ str, __.typx.Any ] = {
            'copied': { str( k ): str( v ) for k, v in self.copied.items( ) },
            'skipped': { str( k ): v for k, v in self.skipped.items( ) },
            'renamed': {
                str( k ): {
                    'original': str( v[ 0 ] ),
                    'renamed': str( v[ 1 ] ),
                }
                for k, v in self.renamed.items( )
            },
            'failed': { str( k ): v for k, v in self.failed.items( ) },
            'warnings': list( self.warnings ),
        }
        return _json_dumps( data, indent = 2 )

    def render_as_text( self ) -> str:
        ''' Renders result as human-readable text. '''
        lines: list[ str ] = [ ]
        if self.copied:
            lines.append( f"Copied {len( self.copied )} file(s):" )
            for src, dest in self.copied.items( ):
                lines.append( f"  {src} -> {dest}" )
        if self.skipped:
            lines.append( f"\nSkipped {len( self.skipped )} file(s):" )
            for src, reason in self.skipped.items( ):
                lines.append( f"  {src}: {reason}" )
        if self.renamed:
            count = len( self.renamed )
            lines.append( f"\nRenamed {count} file(s) (duplicate names):" )
            for src, ( orig, renamed ) in self.renamed.items( ):
                lines.append( f"  {src} -> {renamed} (was: {orig})" )
        if self.failed:
            lines.append( f"\nFailed {len( self.failed )} file(s):" )
            for src, error in self.failed.items( ):
                lines.append( f"  {src}: {error}" )
        if self.warnings:
            lines.append( f"\nWarnings ({len( self.warnings )}):" )
            lines.extend( f"  {warning}" for warning in self.warnings )
        if not any( [ self.copied, self.skipped, self.renamed, self.failed ] ):
            lines.append( "No files processed." )
        return '\n'.join( lines )


class IngestCommand( __.immut.DataclassObject ):
    ''' Ingests scribbles from source directory into organized archive.

        Performs project-based file copying with duplicate detection and
        secret screening.
    '''

    project_name: __.typx.Annotated[
        str,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Target project name for ingestion. ''' ),
    ]
    source_paths: __.typx.Annotated[
        __.cabc.Sequence[ Location ],
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Source file(s) or directory to ingest. ''' ),
    ]
    target_base: __.typx.Annotated[
        Location,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Base directory for ingestion. ''' ),
    ] = "ingests"
    check_secrets: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Enable secret detection (warnings only). ''' ),
    ] = True
    dry_run: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Preview operations without making changes. ''' ),
    ] = False

    async def __call__( self ) -> IngestResult:
        ''' Executes ingestion command. '''
        target_dir = __.Path( self.target_base ) / self.project_name
        source_files = list( _discover_source_files( self.source_paths ) )
        if not source_files:
            return IngestResult(
                copied = __.immut.Dictionary( ),
                skipped = __.immut.Dictionary( ),
                renamed = __.immut.Dictionary( ),
                failed = __.immut.Dictionary( ),
                warnings = ( ),
            )
        copied: dict[ __.Path, __.Path ] = { }
        skipped: dict[ __.Path, str ] = { }
        renamed: dict[ __.Path, PathPair ] = { }
        failed: dict[ __.Path, str ] = { }
        warnings: list[ str ] = [ ]
        for base_path, source in source_files:
            try:
                result = await _process_file(
                    base_path, source, target_dir, warnings,
                    self.check_secrets, self.dry_run )
            except Exception as exception:
                failed[ source ] = str( exception )
                continue
            if result is None:
                skipped[ source ] = "Same content already exists"
            elif isinstance( result, tuple ):
                renamed[ source ] = result
            else:
                copied[ source ] = result
        return IngestResult(
            copied = __.immut.Dictionary( copied ),
            skipped = __.immut.Dictionary( skipped ),
            renamed = __.immut.Dictionary( renamed ),
            failed = __.immut.Dictionary( failed ),
            warnings = tuple( warnings ),
        )


class ClassifyResult( __.immut.DataclassObject ):
    ''' Results of classification operation (stub). '''

    def render_as_json( self ) -> str:
        ''' Renders result as JSON string. '''
        return _json_dumps( { 'status': 'not implemented' }, indent = 2 )

    def render_as_text( self ) -> str:
        ''' Renders result as human-readable text. '''
        return "ClassifyCommand not yet implemented (Phase 2+)"


class ClassifyCommand( __.immut.DataclassObject ):
    ''' Classifies and labels ingested scribbles (stub for Phase 2). '''

    async def __call__( self ) -> ClassifyResult:
        ''' Stub implementation. '''
        return ClassifyResult( )


class SearchResult( __.immut.DataclassObject ):
    ''' Results of search operation (stub). '''

    def render_as_json( self ) -> str:
        ''' Renders result as JSON string. '''
        return _json_dumps( { 'status': 'not implemented' }, indent = 2 )

    def render_as_text( self ) -> str:
        ''' Renders result as human-readable text. '''
        return "SearchCommand not yet implemented (Phase 2+)"


class SearchCommand( __.immut.DataclassObject ):
    ''' Searches and queries scribbles catalog (stub for Phase 2). '''

    async def __call__( self ) -> SearchResult:
        ''' Stub implementation. '''
        return SearchResult( )
