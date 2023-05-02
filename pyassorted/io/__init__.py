from pathlib import Path
from typing import BinaryIO, Iterable, List, Optional, Text, TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import OpenTextMode


class AsyncTextIOWrapper():
    def __init__(self, path: Path, mode: "OpenTextMode" = "r", encoding: Optional[Text] = None):
        self.path = path
        self.mode = mode
        self.encoding = encoding

        self.file = None

    async def __aenter__(self):
        self.file = open(self.path, mode=self.mode, encoding=self.encoding)
        return self

    async def __aexit__(self, *args):
        self.file.close()

    async def __aiter__(self):
        return self.file.__aiter__()

    def detach(self) -> BinaryIO:raise NotImplementedError
    def read(self, __size: Optional[int] = ...) -> Text:raise NotImplementedError
    def readline(self, __size: int = -1) -> Text:raise NotImplementedError
    def readline(self, __size: int = ...) -> Text:raise NotImplementedError
    def readlines(self, __hint: int = -1) -> List[Text]:raise NotImplementedError
    def readlines(self, __hint: int = -1) -> List[Text]:raise NotImplementedError
    def seek(self, __cookie: int, __whence: int = 0) -> int:raise NotImplementedError
    def write(self, __s: Text) -> int:raise NotImplementedError
    def writelines(self, __lines: Iterable[Text]) -> None:raise NotImplementedError
    def writelines(self, __lines: Iterable[Text]) -> None:raise NotImplementedError

def aio_open(path: Path, mode: "OpenTextMode" = "r", encoding: Optional[Text] = None):
    return AsyncTextIOWrapper(path=path, mode=mode, encoding=encoding)


if __name__ == "__main__":
    import asyncio
    async def main():
        async with aio_open("text.txt", "w") as f:
            print(f)
    asyncio.run(main())
