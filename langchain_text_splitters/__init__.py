"""Minimal RecursiveCharacterTextSplitter compatibility layer.

The production dependency is declared in requirements.txt as langchain-text-splitters.
This local module keeps the ingestion workflow testable in constrained environments
where that package cannot be fetched while preserving the same public class used by
LangChain document ingestion pipelines.
"""


class RecursiveCharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: list[str] | None = None,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> list[str]:
        if not text:
            return []
        chunks: list[str] = []
        remaining = text.strip()
        while remaining:
            if len(remaining) <= self.chunk_size:
                chunks.append(remaining)
                break
            split_at = self._find_split_position(remaining[: self.chunk_size])
            chunk = remaining[:split_at].strip()
            if chunk:
                chunks.append(chunk)
            next_start = max(split_at - self.chunk_overlap, 0)
            if next_start <= 0 or next_start >= split_at:
                next_start = split_at
            remaining = remaining[next_start:].strip()
        return chunks

    def _find_split_position(self, text: str) -> int:
        for separator in self.separators:
            if separator == "":
                continue
            position = text.rfind(separator)
            if position > 0:
                return position + len(separator)
        return len(text)
