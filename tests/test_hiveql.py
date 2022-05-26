import subprocess
from pathlib import Path

from pycmd.utils import Console


EXPECT_FORMAT = """
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
"""


class TestHiveQL:
    test_file = "./tests/data/test.hql"

    def test_file_not_exist(self):
        not_exist_file = Path("./tests/data/not_exist_file.hql")
        assert not not_exist_file.is_file()
        result = subprocess.run(["python", "-m", "pycmd.hiveql", str(not_exist_file)], capture_output=True)
        assert Console.escape(result.stdout) == f"✗ File '{Path(not_exist_file).as_posix()}' not exit"

    def test_format_success(self):
        to_file = "./tests/data/test_copy_00.hql"
        if Path(to_file).is_file():
            Path(to_file).unlink()
            assert not Path(to_file).is_file()
        subprocess.run(["python", "-m", "pycmd.hiveql", self.test_file, "-o", to_file], stdout=subprocess.DEVNULL)
        with Path(to_file).open("r", encoding="utf-8") as f:
            result = f.read()
        assert result.strip() == EXPECT_FORMAT.strip()

    def test_format_online_success(self):
        to_file = "./tests/data/test_copy_01.hql"
        if Path(to_file).is_file():
            Path(to_file).unlink()
            assert not Path(to_file).is_file()
        subprocess.run(
            ["python", "-m", "pycmd.hiveql", self.test_file, "-u", "-o", to_file], stdout=subprocess.DEVNULL, check=True
        )

        with Path(to_file).open("r", encoding="utf-8") as f:
            result = f.read()
        assert result.strip() == EXPECT_FORMAT.strip()

    def test_reserve_success(self):
        to_file = "./tests/data/test_copy_02.hql"
        if Path(to_file).is_file():
            Path(to_file).unlink()
            assert not Path(to_file).is_file()
        subprocess.run(
            ["python", "-m", "pycmd.hiveql", self.test_file, "-r", "string", "-o", to_file], stdout=subprocess.DEVNULL
        )
        with Path(to_file).open("r", encoding="utf-8") as f:
            result = f.read()
        assert "STRING" not in result
