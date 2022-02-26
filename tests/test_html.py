from pathlib import Path
import subprocess
from pycmd.utils import Console


class TestHTML:
    def test_no_table_found(self):
        html_file = 'tests/data/no_table.html'
        result = subprocess.run(['python', '-m', 'pycmd.html', html_file], capture_output=True)
        assert Console.escape(result.stdout) == "!!! No tables found"

    def test_one_table(self):
        html_file = 'tests/data/one_table.html'
        result = subprocess.run(['python', '-m', 'pycmd.html', html_file], capture_output=True)
        assert "Crawl 1 tables" in Console.escape(result.stdout)

    def test_two_table(self):
        html_file = 'tests/data/two_table.html'
        result = subprocess.run(['python', '-m', 'pycmd.html', html_file], capture_output=True)
        assert "Crawl 2 tables" in Console.escape(result.stdout)

    def test_save_one_table(self):
        html_file = 'tests/data/one_table.html'
        csv_file = 'tests/data/table.csv'
        csv_path = Path(csv_file)
        if csv_path.is_file():
            csv_path.unlink()
            assert not csv_path.is_file()
        subprocess.run(['python', '-m', 'pycmd.html', html_file, '-o', csv_file], stdout=subprocess.DEVNULL)
        assert csv_path.is_file()

    def test_save_two_table(self):
        html_file = 'tests/data/two_table.html'
        csv_file = 'tests/data/table.csv'
        csv_path = Path(csv_file)
        if csv_path.is_file():
            csv_path.unlink()
            assert not csv_path.is_file()
        if Path(csv_path.parent, f"{csv_path.stem}_00{csv_path.suffix}").is_file():
            Path(csv_path.parent, f"{csv_path.stem}_00{csv_path.suffix}").unlink()
            assert not Path(csv_path.parent, f"{csv_path.stem}_00{csv_path.suffix}").is_file()
        if Path(csv_path.parent, f"{csv_path.stem}_01{csv_path.suffix}").is_file():
            Path(csv_path.parent, f"{csv_path.stem}_01{csv_path.suffix}").unlink()
            assert not Path(csv_path.parent, f"{csv_path.stem}_01{csv_path.suffix}").is_file()
        subprocess.run(['python', '-m', 'pycmd.html', html_file, '-o', csv_file], stdout=subprocess.DEVNULL)
        assert not csv_path.is_file()
        assert Path(csv_path.parent, f"{csv_path.stem}_00{csv_path.suffix}").is_file()
        assert Path(csv_path.parent, f"{csv_path.stem}_01{csv_path.suffix}").is_file()

    def test_match(self):
        html_file = 'tests/data/two_table.html'
        result = subprocess.run(['python', '-m', 'pycmd.html', html_file, '-m', 'Lily'], capture_output=True)
        assert "Crawl 1 tables" in Console.escape(result.stdout)

    def test_attrs(self):
        html_file = 'tests/data/two_table.html'
        result = subprocess.run(['python', '-m', 'pycmd.html', html_file, '-a', 'id=table1'], capture_output=True)
        assert "Crawl 1 tables" in Console.escape(result.stdout)
