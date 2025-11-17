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


''' Family of exceptions for package API. '''


from . import __


class Omniexception( __.immut.exceptions.Omniexception ):
    ''' Base for all exceptions raised by package API. '''

    def render_as_text( self ) -> str:
        ''' Renders exception as human-readable text. '''
        return f"{self.__class__.__name__}: {self}"

    def render_as_json( self ) -> str:
        ''' Renders exception as JSON string. '''
        from json import dumps as _json_dumps
        data: dict[ str, __.typx.Any ] = {
            'exception': self.__class__.__name__,
            'message': str( self ),
        }
        return _json_dumps( data, indent = 2 )


class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised by package API. '''


class DuplicateDetectionFailure( Omnierror, OSError ):
    ''' Duplicate detection failure. '''

    def render_as_text( self ) -> str:
        ''' Renders exception with file path details. '''
        return f"Duplicate detection failed for: {self}"

    def render_as_json( self ) -> str:
        ''' Renders exception with file path details as JSON. '''
        from json import dumps as _json_dumps
        data: dict[ str, __.typx.Any ] = {
            'exception': self.__class__.__name__,
            'file_path': str( self ),
            'message': 'Failed to compute file hash for duplicate detection',
        }
        return _json_dumps( data, indent = 2 )


class FileIngestionFailure( Omnierror, OSError ):
    ''' File ingestion failure. '''

    def render_as_text( self ) -> str:
        ''' Renders exception with file path details. '''
        return f"File ingestion failed for: {self}"

    def render_as_json( self ) -> str:
        ''' Renders exception with file path details as JSON. '''
        from json import dumps as _json_dumps
        data: dict[ str, __.typx.Any ] = {
            'exception': self.__class__.__name__,
            'file_path': str( self ),
            'message': 'Invalid file path (not a file or directory)',
        }
        return _json_dumps( data, indent = 2 )


class SecretDetectionFailure( Omnierror, RuntimeError ):
    ''' Secret detection failure. '''

    def render_as_text( self ) -> str:
        ''' Renders exception with file path details. '''
        return f"Secret detection failed for: {self}"

    def render_as_json( self ) -> str:
        ''' Renders exception with file path details as JSON. '''
        from json import dumps as _json_dumps
        data: dict[ str, __.typx.Any ] = {
            'exception': self.__class__.__name__,
            'file_path': str( self ),
            'message': 'Failed to scan file for secrets',
        }
        return _json_dumps( data, indent = 2 )
