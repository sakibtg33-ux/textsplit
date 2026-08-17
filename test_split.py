from pathlib import Path
from tempfile import TemporaryDirectory

from bot import split_txt_file


with TemporaryDirectory() as temp:
    root = Path(temp)
    source = root / "source.txt"
    source.write_text("".join(f"line-{i}\n" for i in range(123)), encoding="utf-8")
    outputs = split_txt_file(source, root / "parts")

    assert [len(path.read_text(encoding="utf-8").splitlines()) for path in outputs] == [50, 50, 23]
    assert [path.name for path in outputs] == ["split_001.txt", "split_002.txt", "split_003.txt"]
    print("split test passed")
