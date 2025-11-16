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
from pathlib import Path as _Path
from shutil import copy2 as _copy_file

from . import __, exceptions


# Type Aliases
Location: __.typx.TypeAlias = str | __.typx.Any  # Path-like
PathPair: __.typx.TypeAlias = tuple[ _Path, _Path ]


class IngestResult( __.immut.DataclassObject ):
    ''' Results of ingestion operation. '''

    copied: __.immut.Dictionary[ _Path, _Path ]
    skipped: __.immut.Dictionary[ _Path, str ]
    renamed: __.immut.Dictionary[ _Path, PathPair ]
    failed: __.immut.Dictionary[ _Path, str ]
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

    project_name: str = __.tyro.conf.arg(  # pyright: ignore
        help = "Target project name for ingests/<project-name>/" )
    source_paths: __.cabc.Sequence[ Location ] = __.tyro.conf.arg(  # pyright: ignore
        help = "Source file(s) or directory to ingest" )
    target_base: Location = "ingests"
    check_secrets: bool = True
    dry_run: bool = False

    async def __call__( self ) -> int:
        ''' Executes ingestion command. '''
        target_dir = _Path( self.target_base ) / self.project_name

        # Collect source files
        source_files = list( self._discover_source_files( ) )
        if not source_files:
            print( "No files found to ingest." )
            return 0

        # Ensure target directory exists (unless dry-run)
        if not self.dry_run:
            target_dir.mkdir( parents = True, exist_ok = True )

        # Process files
        copied: dict[ _Path, _Path ] = { }
        skipped: dict[ _Path, str ] = { }
        renamed: dict[ _Path, PathPair ] = { }
        failed: dict[ _Path, str ] = { }
        warnings: list[ str ] = [ ]

        for source in source_files:
            try:
                result = await self._process_file(
                    source, target_dir, warnings )
            except Exception as exception:
                failed[ source ] = str( exception )
                continue

            if result is None:  # skipped
                skipped[ source ] = "Same content already exists"
            elif isinstance( result, tuple ):  # renamed
                renamed[ source ] = result
            else:  # copied
                copied[ source ] = result

        # Create and render result
        result_obj = IngestResult(
            copied = __.immut.Dictionary( copied ),
            skipped = __.immut.Dictionary( skipped ),
            renamed = __.immut.Dictionary( renamed ),
            failed = __.immut.Dictionary( failed ),
            warnings = tuple( warnings ),
        )

        print( result_obj.render_as_text( ) )
        return 1 if failed else 0

    def _discover_source_files( self ) -> __.cabc.Iterator[ _Path ]:
        ''' Discovers all source files to ingest. '''
        for location in self.source_paths:
            path = _Path( location )
            if path.is_file( ):
                yield path
            elif path.is_dir( ):
                yield from path.rglob( '*' )
                # Only yield actual files, not directories
                for item in path.rglob( '*' ):
                    if item.is_file( ):
                        yield item
            else:
                raise exceptions.FileIngestionFailure( str( path ) )

    async def _process_file(
        self,
        source: _Path,
        target_dir: _Path,
        warnings: list[ str ],
    ) -> _Path | PathPair | None:
        ''' Processes single file for ingestion.

            Returns:
                - Path: Successfully copied to this destination
                - PathPair: Renamed due to duplicate
                - None: Skipped (duplicate content)
        '''
        # Check for secrets
        if self.check_secrets:
            await self._check_secrets( source, warnings )

        # Determine target path
        target_path = target_dir / source.name

        # Check for duplicate name
        if target_path.exists( ):
            source_hash = self._compute_hash( source )
            target_hash = self._compute_hash( target_path )

            if source_hash == target_hash:
                return None  # Skip - same content

            # Different content - rename with hash suffix
            stem = target_path.stem
            suffix = target_path.suffix
            hash_suffix = source_hash[ :6 ]
            renamed_path = target_dir / f"{stem}-{hash_suffix}{suffix}"

            if not self.dry_run:
                _copy_file( source, renamed_path )

            return ( target_path, renamed_path )

        # No duplicate - copy normally
        if not self.dry_run:
            _copy_file( source, target_path )

        return target_path

    def _compute_hash( self, file_path: _Path ) -> str:
        ''' Computes SHA-256 hash of file contents. '''
        hasher = _sha256( )
        try:
            with file_path.open( 'rb' ) as file:
                while chunk := file.read( 8192 ):
                    hasher.update( chunk )
        except OSError as exception:
            raise exceptions.DuplicateDetectionFailure(
                str( file_path ) ) from exception
        return hasher.hexdigest( )

    async def _check_secrets(
        self,
        file_path: _Path,
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
            raise exceptions.SecretDetectionFailure(
                str( file_path ) ) from exception


class ClassifyCommand( __.immut.DataclassObject ):
    ''' Classifies and labels ingested scribbles (stub for Phase 2). '''

    async def __call__( self ) -> int:
        ''' Stub implementation. '''
        print( "ClassifyCommand not yet implemented (Phase 2+)" )
        return 0


class SearchCommand( __.immut.DataclassObject ):
    ''' Searches and queries scribbles catalog (stub for Phase 2). '''

    async def __call__( self ) -> int:
        ''' Stub implementation. '''
        print( "SearchCommand not yet implemented (Phase 2+)" )
        return 0
