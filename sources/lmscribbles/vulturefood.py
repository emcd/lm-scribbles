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


''' Whitelist of intentionally unused code for vulture. '''


from .commands import ClassifyResult, IngestResult, SearchResult
from .exceptions import (
    DuplicateDetectionFailure,
    FileIngestionFailure,
    Omniexception,
    SecretDetectionFailure,
)


# Self-rendering methods that will be called dynamically
IngestResult.render_as_json
ClassifyResult.render_as_json
SearchResult.render_as_json
Omniexception.render_as_json
Omniexception.render_as_text
DuplicateDetectionFailure.render_as_json
DuplicateDetectionFailure.render_as_text
FileIngestionFailure.render_as_json
FileIngestionFailure.render_as_text
SecretDetectionFailure.render_as_json
SecretDetectionFailure.render_as_text
