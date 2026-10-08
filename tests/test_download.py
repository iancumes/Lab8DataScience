"""Regresiones de integridad: nunca aceptar archivos parciales o sobrescribir existentes."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pyarrow as pa
import pyarrow.parquet as pq
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from download_data import download_one, inspect_file


class DownloadIntegrity(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.root=Path(self.directory.name)
        self.path=self.root/'yellow/2026/yellow_tripdata_2026-01.parquet'
        self.path.parent.mkdir(parents=True)

    def tearDown(self):
        self.directory.cleanup()

    def test_existing_valid_file_never_requests_network(self):
        pq.write_table(pa.table({'x':[1,2]}),self.path)
        before=(self.path.stat().st_mtime_ns,self.path.read_bytes())
        with patch('download_data.session',side_effect=AssertionError('No debe acceder a red')):
            result=download_one(('yellow',2026,1,self.root))
        self.assertEqual(result['status'],'existing')
        self.assertEqual(result['rows'],2)
        self.assertEqual(before,(self.path.stat().st_mtime_ns,self.path.read_bytes()))

    def test_corrupt_existing_file_is_reported_and_preserved(self):
        self.path.write_bytes(b'PAR1truncated')
        with patch('download_data.session',side_effect=AssertionError('No sobrescribir')):
            result=download_one(('yellow',2026,1,self.root))
        self.assertEqual(result['status'],'error')
        self.assertEqual(self.path.read_bytes(),b'PAR1truncated')

    def test_empty_parquet_is_rejected(self):
        pq.write_table(pa.table({'x':pa.array([],type=pa.int64())}),self.path)
        with self.assertRaises(ValueError):
            inspect_file(self.path)

    def test_interrupted_download_never_commits_partial_file(self):
        with patch('download_data.session',side_effect=ConnectionError('interrumpida')),patch('download_data.time.sleep'):
            result=download_one(('yellow',2026,1,self.root))
        self.assertEqual(result['status'],'error')
        self.assertFalse(self.path.exists())
        self.assertFalse(self.path.with_suffix('.parquet.part').exists())


if __name__=='__main__':
    unittest.main()
