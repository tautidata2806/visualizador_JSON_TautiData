import io
import unittest
import zipfile
import json
from unittest.mock import patch
import pandas as pd
from streamlit.testing.v1 import AppTest
from tautidata.json_tools import parse_json, sections, to_table, csv_bytes, excel_bytes

class DataTests(unittest.TestCase):
    def test_resource_limits(self):
        with self.assertRaises(ValueError):
            parse_json(b'[' * 52 + b'0' + b']' * 52)
        with self.assertRaises(ValueError):
            parse_json(b'{"a":1,"a":2}')
        with self.assertRaises(ValueError):
            parse_json(b'1e999')
        with patch('tautidata.json_tools.MAX_NODES', 5):
            with self.assertRaises(ValueError):
                parse_json(b'[1,2,3,4,5]')
        with patch('tautidata.json_tools.MAX_ROWS', 2):
            with self.assertRaises(ValueError):
                to_table([1, 2, 3])
        with patch('tautidata.json_tools.MAX_COLUMNS', 2):
            with self.assertRaises(ValueError):
                to_table({'a': 1, 'b': 2, 'c': 3})
        with patch('tautidata.json_tools.MAX_CELLS', 3):
            with self.assertRaises(ValueError):
                to_table([{'a': 1}, {'b': 2}])
    def test_public_contact(self):
        app = AppTest.from_file(str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'visualizador_json_TautiData.py')).run()
        text = [item.value for item in app.text]
        self.assertIn('David Fellipe Tautiva', text)
        self.assertIn('tautidata2806@gmail.com', text)
        self.assertFalse(any('Los archivos se procesan' in item.value for item in app.caption))
    def test_validation(self):
        self.assertEqual(parse_json(b'\xef\xbb\xbf{"x":1}'), {'x': 1})
        for raw in [b'{', b'NaN', b'\xff']:
            with self.assertRaises(ValueError):
                parse_json(raw)
    def test_shapes_and_collisions(self):
        self.assertEqual(len(to_table([])), 0)
        self.assertEqual(len(to_table([1, None, 'x'])), 3)
        frame = to_table({'a.b': 1, 'a': {'b': 2}, 'list': [1, 2]})
        self.assertEqual(len(frame.columns), 3)
        self.assertIn('$["ventas"]', sections({'ventas': [{'x': 1}]}))
    def test_exports(self):
        frame = pd.DataFrame({'texto': ['=1+1', 'Bogotá'], 'id': [1234567890123456789, 2]}, dtype=object)
        self.assertIn("'=1+1", csv_bytes(frame).decode('utf-8-sig'))
        payload = excel_bytes(frame)
        with zipfile.ZipFile(io.BytesIO(payload)) as book:
            sheet = book.read('xl/worksheets/sheet1.xml').decode()
            strings = book.read('xl/sharedStrings.xml').decode()
            self.assertNotIn('<f>', sheet)
            self.assertIn('1234567890123456789', strings)
            self.assertIn('Bogotá', strings)
    def test_app(self):
        app = AppTest.from_file(str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'visualizador_json_TautiData.py')).run()
        self.assertFalse(app.exception)
        app.radio[0].set_value('Probar ejemplo').run()
        self.assertFalse(app.exception)
        app.selectbox[0].set_value('$["ventas"]').run()
        self.assertEqual(app.metric[0].value, '4')
        app.text_input[0].set_value('Ana').run()
        self.assertEqual(len(app.dataframe[0].value), 1)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        app.radio[0].set_value('Pegar JSON').run()
        app.text_area[0].set_value('{').run()
        self.assertTrue(app.error)
        app.text_area[0].set_value('[]').run()
        self.assertFalse(app.exception)
        app.text_input[0].set_value('abc').run()
        self.assertFalse(app.exception)

if __name__ == '__main__':
    unittest.main()

