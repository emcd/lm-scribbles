import detextive

content = b'test content'

# Configure behaviors to disable all charset detection methods
behaviors = detextive.Behaviors(
    charset_detect = detextive.BehaviorTristate.Never,
    charset_on_detect_failure = detextive.DetectFailureActions.Error )

print(f"Behaviors: {behaviors}")
print(f"charset_detect: {behaviors.charset_detect}")
print(f"charset_on_detect_failure: {behaviors.charset_on_detect_failure}")

try:
    result = detextive.inference.infer_mimetype_charset_confidence(
        content,
        behaviors = behaviors,
        charset_default = '' )  # Empty default to prevent fallback
    print(f"Unexpected success: {result}")
except detextive.exceptions.CharsetInferFailure as e:
    print(f"Got expected CharsetInferFailure: {e}")
except Exception as e:
    print(f"Got unexpected exception: {type(e).__name__}: {e}")