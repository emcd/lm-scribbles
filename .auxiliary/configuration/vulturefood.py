from lmscribbles.commands import ClassifyResult, IngestResult, SearchResult
from lmscribbles.exceptions import (
    DuplicateDetectionFailure,
    FileIngestionFailure,
    Omniexception,
    SecretDetectionFailure,
)


ComparisonResult  # unused variable
NominativeArguments  # unused variable
PositionalArguments  # unused variable
package_name  # unused variable

# --- BEGIN: Injected by Copier ---
Omnierror  # unused base exception class for derivation
# --- END: Injected by Copier ---

# Self-rendering methods that will be called dynamically.
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
