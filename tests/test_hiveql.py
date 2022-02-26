from pathlib import Path
import subprocess
from pycmd.utils import Console


EXPECT_FORMAT = '''
CREATE TABLE IF NOT EXISTS test.test (
    string_col STRING COMMENT 'string_col',
    bigint_col BIGINT COMMENT 'bigint_col',
    double_col DOUBLE COMMENT 'double_col',
    map_string_string_col MAP<STRING,STRING> COMMENT 'map_string_string_col',
    map_string_bigint_col MAP<STRING,BIGINT> COMMENT 'map_string_bigint_col'
)
COMMENT 'table'
PARTITIONED BY (
    pt STRING COMMENT 'pt'
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
STORED AS textfile
;
'''


class TestHiveQL:
    def test_file_not_exist(self):
        not_exist_file = 'tests/data/not_exist_file.hql'
        result = subprocess.run(['python', '-m', 'pycmd.hiveql', not_exist_file], capture_output=True)
        assert Console.escape(result.stdout) == f"✗✗✗ File '{Path(not_exist_file).as_posix()}' not exit"

    def test_format_success(self):
        test_file = 'tests/data/test.hql'
        path = Path(test_file)
        path_copy = Path(path.parent, f"{path.stem}_copy{path.suffix}")
        if path_copy.is_file():
            path_copy.unlink()
            assert not path_copy.is_file()
        subprocess.run(['python', '-m', 'pycmd.hiveql', test_file], stdout=subprocess.DEVNULL)
        assert path_copy.is_file()
        with path_copy.open("r", encoding="utf-8") as f:
            result = f.read()
        assert result.strip() == EXPECT_FORMAT.strip()

    def test_reserve_success(self):
        test_file = 'tests/data/test.hql'
        path = Path(test_file)
        path_copy = Path(path.parent, f"{path.stem}_copy{path.suffix}")
        if path_copy.is_file():
            path_copy.unlink()
            assert not path_copy.is_file()
        subprocess.run(['python', '-m', 'pycmd.hiveql', test_file, '-r', 'string'], stdout=subprocess.DEVNULL)
        with path_copy.open("r", encoding="utf-8") as f:
            result = f.read()
        assert 'STRING' not in result
