from pathlib import Path


class ResourceManager:

    def __init__(self, test_mode: bool = False):
        self._test_mode = test_mode

    def get(self, file_path: str) -> Path:
        return Path(self.resources(), file_path)

    def root(self) -> Path:
        index = [idx for idx, path in enumerate(list(Path().absolute().parts)) if 'service' in path][0] + 1
        return Path(*Path().absolute().parts[0:index])

    def resources(self):
        paths = Path("resources").absolute().parents
        if not self._test_mode and "tests" in paths[0].parts:
            dirs = paths[0].parts
            index = dirs.index("tests")
            root = dirs[index - 1].replace("-", "_")
            dirs = (*dirs[0:index], root)
            return Path(*dirs, "resources")
        else:
            return Path("resources")
