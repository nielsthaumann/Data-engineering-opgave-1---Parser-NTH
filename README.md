# Data engineering project 1 - Parser

[parser.py](https://github.com/nielsthaumann/Data-engineering-opgave-1---Parser-NTH/blob/main/parser.py)

**Building, testing, and running a table data parser, 'Tabble', for converting CVS-file to JSON-file.**

<p align="center">
    <img width="217" height="220" alt="image" src="https://github.com/user-attachments/assets/e1b11f80-0efc-4338-ac4a-9a98c6254c21" />
</p>

# Building the table data parser

**Import required libaries**

```python
import numpy as np
import pandas as pd
import pycld2 as cld2
import re
from datetime import datetime
import unittest
import pathvalidate
```

**Read table data and out as binary data and a string**

Syntax:
```python
        raw, string = readtable(filepath)
```

**Detect character encoding standard**
        
> Using Google's CLD2 language detection for Python ([pycld2 on PyPI](https://pypi.org/project/pycld2))

Syntax:
```python
        charec, percent, language = detect_charcode(raw, charecs)
```            
            
        Input: 
            
            raw:        Raw data as bytes (output from readtable)
            
            charecs:    List with possible character encoding standards (e.g., ['UTF-8', 'ISO 8859-1', 'Windows-1252', 'UTF-16', 'UTF-32'])
        
        
        Output: 
            
            charec:     Detected character encoding standard (e.g., 'UTF-8')
            
            percent:    Percentage of text detected
            
            language:   Name of detected language


**Select character encoding standard**
        
Syntax:
```python
        data_decoded = select_charcode(raw, charecs, charec, language)
```            
            
        Input: 
            
            raw:        Raw data as bytes (output from readtable)
            
            charecs:    List with possible character encoding standards (e.g., ['UTF-8', 'ISO 8859-1', 'Windows-1252', 'UTF-16', 'UTF-32'])
        
            charec:     Detected character encoding standard (e.g., 'UTF-8')
            
            language:   Name of detected language
            
        
        Output: 
            
            data_decoded:       Decoded data


**Detect line breaks**

Syntax:   
```python
        linebreak, n_linebreaks = detect_linebreaks(string, linebreaks)
```      
        Input: 
                
                string:        Raw data as string (output from readtable)
                
                linebreaks:    2d list with possible line break types and character sequences (e.g., [['carriage return line feed', 'carriage return', 'new line / line feed'], ['\\r\\n', '\\r', '\\n']])
            
        Outut: 
            
                linebreak:     Detect line break type
                    
                n_linebreaks:  Number of line break character sequences

**Select line breaks**

Syntax:   
```python
        lines = select_linebreaks(data_decoded, linebreaks, linebreak, n_linebreaks)
```        
        Input: 
                
                data_decoded:  Decoded data
                
                linebreaks:    2d list with possible line break types and character sequences (e.g., [['carriage return line feed', 'carriage return', 'new line / line feed'], ['\\r\\n', '\\r', '\\n']])
                
                linebreak:     Detect line break type
                    
                n_linebreaks:  Number of line break character sequences
                
        Outut: 
            
                lines:         Data parsed into strings of lines 


**Detect the column delimiter**
    
Syntax:
```python
        coldim, n_coldims = detect_coldim(string, coldims)
```        
        Input:   
            
                  string:    Raw data as string (output from readtable)
                  
                  coldims:   2d list with possible column delimiter types and character sequences (e.g., [['tab', 'comma', 'double quotes', 'backslash', 'semicolon', 'pipe', 'space'], [r'\t', r',', r'"', r'\\', r';', r'\|', r'\s']])
            
        Output:   
            
                  coldim:       Detected column delimiter type
                  
                  n_coldims:    Number of column delimiter character sequences

**Select the column delimiter**
    
Syntax:
```python
        data_cells = select_coldim(lines, coldims, coldim, n_coldims)
```
        Input: 
            
                  lines:        Data parsed into strings of lines 
            
                  coldims:      2d list with possible column delimiter types and character sequences (e.g., [['tab', 'comma', 'double quotes', 'backslash', 'semicolon', 'pipe', 'space'], [r'\t', r',', r'"', r'\\', r';', r'\|', r'\s']])
                  
                  coldim:       Detected column delimiter type
                  
                  n_coldims:    Number of column delimiter character sequences
            
        Output: 
            
                  data_cells:   Data parsed into cells of lines and columns ( data_cells[line or row][column] )

**Header in first line?**
    
Syntax:   
```python
        dataframe = select_header(data_cells)
```          

**Select cell data format**
        
Syntax:   
 ```python        
        dataframe = select_cellform(dataframe)
```  

**Export to JSON**
```python
print(f'Saving table to {filename[0:-4]}.json')
dataframe.to_json(folderpath + '\\' + filename[0:-4] + '.json', date_format='iso')
```

# Unit tests

**Read table data as binary data and a string**

```python
class TestReadtable(unittest.TestCase): # (Inherits from unittest.TestCase, making it a test case class)
    
    Ensure the file path is a valid file path
    def test_filepath(self):
        folderpath = 'C:\\Users\\NielsHumann\\Documents\\Specialisterne Academy\\Opgave 1 - Parser'
        filename   = 'employees.ascii.csv'
        # filename = 'sogne.dawa.csv'
        filepath   = folderpath + '\\' + filename
        self.assertTrue(pathvalidate.is_valid_filepath(filepath, platform='auto'))
    
    Ensure the data can be read
    def test_fileread(self): 
        # raw output length is greater than zero
        self.assertGreater(len(readtable(filepath)[0]), 0)
    
    Ensure the raw bytes can be converted to a string
    def test_bytes2string(self): 
        # string output length is greater than zero
        self.assertGreater(len(readtable(filepath)[1]), 0)
```
**Select the character encoding standard**
```python
class TestDetect_charcode(unittest.TestCase):
    
    Ensure the character encoding standard can be detected
    def test_detect_charcode(self): 
        self.assertEqual(detect_charcode(raw, charecs)[0], 'UTF-8')
    
    Ensure the character encoding standard can be selected
    def test_select_charcode(self): 
        # data output length is greater than zero
        self.assertGreater(len(select_charcode(raw, charecs, charec, language)), 0)   
```
**Select the line break delimiter**
```python
class TestLinebreaks(unittest.TestCase):
    
    Ensure the line break delimiter can be detected
    def test_detect_linebreaks(self): 
        self.assertEqual(detect_linebreaks(string, linebreaks)[0], 'new line / line feed')
    
    Ensure the line break delimiter can be selected
    lines output length is greater than zero
    def test_select_linebreaks(self): 
        self.assertGreater(len(select_linebreaks(data_decoded, linebreaks, linebreak, n_linebreaks)), 0)   
```
**Select the column delimiter**
```python
class TestColdim(unittest.TestCase):
    
    Ensure the column delimiter can be detected
    def test_detect_coldim(self): 
        self.assertEqual(detect_coldim(string, coldims)[0], 'comma')
    
    Ensure the column delimiter can be selected
    data output length is greater than zero
    def test_select_linebreaks(self): 
        self.assertGreater(len(select_coldim(lines, coldims, coldim, n_coldims)), 0)   
```
**Header in first line?**
```python
class TestHeader(unittest.TestCase):
    
    Ensure the header can be selected
    def test_select_header(self): 
        self.assertEqual(list(select_header(data_cells)), ['"name', 'email', 'department', 'role', 'salary', 'start_date', 'office'])

if __name__ == '__main__':
    unittest.main()
 ```

# Running 'Tabble'


<img width="1935" height="982" alt="Running Tabble" src="https://github.com/user-attachments/assets/c29a8df8-e9cc-44c1-8f6d-d438dc555e2d" />

