import sys
import re
from typing import Callable, Iterable, Generator

class TextChunk(str):
    """Custom string wrapper providing fluent transformation primitives."""
    def clean(self) -> 'TextChunk':
        return TextChunk(' '.join(self.split()))

    def mask_secrets(self) -> 'TextChunk':
        pattern = r'(api[_-]?key|password|token)\s*=\s*\S+'
        return TextChunk(re.sub(pattern, r'\1=***', self, flags=re.IGNORECASE))

    def wrap_cli(self, prefix: str = "[OUT]") -> 'TextChunk':
        return TextChunk("\n".join(f"{prefix} {line}" for line in self.splitlines()))

class StreamProcessor:
    """Dynamic generator-based CLI output processor pipeline."""
    def __init__(self, *steps: Callable[[TextChunk], TextChunk]):
        self._steps = steps or (TextChunk.clean, TextChunk.mask_secrets)

    def __rshift__(self, next_step: Callable[[TextChunk], TextChunk]) -> 'StreamProcessor':
        """Overload >> operator to append processing steps."""
        return StreamProcessor(*self._steps, next_step)

    def process(self, stream: Iterable[str]) -> Generator[str, None, None]:
        for raw_item in stream:
            chunk = TextChunk(str(raw_item))
            for step in self._steps:
                chunk = step(chunk)
            yield str(chunk)

def process_cli_output(data_stream: Iterable[str]) -> None:
    pipeline = StreamProcessor() >> (lambda c: c.wrap_cli(">>>"))
    for output in pipeline.process(data_stream):
        sys.stdout.write(f"{output}\n")
