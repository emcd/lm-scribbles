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


''' Command-line interface. '''


from . import __
from . import commands as _commands


def execute( ) -> None:
    ''' Entrypoint for CLI execution. '''
    from asyncio import run
    config = (
        __.tyro.conf.EnumChoicesFromValues,
        __.tyro.conf.HelptextFromCommentsOff,
    )
    try: run( __.tyro.cli( _main, config = config ) ) # pyright: ignore
    except SystemExit: raise
    except BaseException:
        # TODO: Log exception.
        raise SystemExit( 1 ) from None


async def _main(
    command: __.typx.Union[
        __.typx.Annotated[
            _commands.IngestCommand,
            __.tyro.conf.subcommand(
                'ingest', prefix_name = False, default = True ),
        ],
        __.typx.Annotated[
            _commands.ClassifyCommand,
            __.tyro.conf.subcommand( 'classify', prefix_name = False ),
        ],
        __.typx.Annotated[
            _commands.SearchCommand,
            __.tyro.conf.subcommand( 'search', prefix_name = False ),
        ],
    ],
) -> None:
    ''' Main CLI entrypoint with subcommands. '''
    result = await command( )
    print( result.render_as_text( ) )
