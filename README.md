# Data engineering project 1 - Parser

Building, testing, and running a table data parser, 'Tabble', for converting CVS-file to JSON-file.  

<img width="434" height="440" alt="image" src="https://github.com/user-attachments/assets/e1b11f80-0efc-4338-ac4a-9a98c6254c21" />

# Building the table data parser, 'Tabble', for converting CVS-file to JSON-file

Step 1. Read table data and out as binary data and a string
    
        Syntax:     raw, string = readtable(filepath)


Step 2. Detect character encoding standard
        
        Using Google's CLD2 language detection for Python ( https://pypi.org/project/pycld2/ ) 
        
        
        Syntax: 
            
            charec, percent, language = detect_charcode(raw, charecs)
            
            
        Input: 
            
            raw:        Raw data as bytes (output from readtable)
            
            charecs:    List with possible character encoding standards (e.g., ['UTF-8', 'ISO 8859-1', 'Windows-1252', 'UTF-16', 'UTF-32'])
        
        
        Output: 
            
            charec:     Detected character encoding standard (e.g., 'UTF-8')
            
            percent:    Percentage of text detected
            
            language:   Name of detected language


Step 3. Select character encoding standard
        
        Syntax: 
            
            data = select_charcode(raw, charecs, charec, language)
            
            
        Input: 
            
            raw:        Raw data as bytes (output from readtable)
            
            charecs:    List with possible character encoding standards (e.g., ['UTF-8', 'ISO 8859-1', 'Windows-1252', 'UTF-16', 'UTF-32'])
        
            charec:     Detected character encoding standard (e.g., 'UTF-8')
            
            language:   Name of detected language
            
        
        Output: 
            
            data_decoded:       Decoded data


Step 4. Select the column delimiter
    
        Syntax:   coldim, n_coldims = detect_coldim(string, coldims)
        
        Input:   
            
                  string:    Raw data as string (output from readtable)
                  
                  coldims:   2d list with possible column delimiter types and character sequences (e.g., [['tab', 'comma', 'double quotes', 'backslash', 'semicolon', 'pipe', 'space'], [r'\t', r',', r'"', r'\\', r';', r'\|', r'\s']])
            
        Output:   
            
                  coldim:       Detected column delimiter type
                  
                  n_coldims:    Number of column delimiter character sequences

Step 5: Header in first line?
    
        Syntax:   dataframe = select_header(data_cells)
        
Step 6: Select cell data format
        
        Syntax:   dataframe = select_cellform(dataframe)



# Unit tests

Import table content as a string
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

Select the character encoding standard
class TestDetect_charcode(unittest.TestCase):
    
    Ensure the character encoding standard can be detected
    def test_detect_charcode(self): 
        self.assertEqual(detect_charcode(raw, charecs)[0], 'UTF-8')
    
    Ensure the character encoding standard can be selected
    def test_select_charcode(self): 
        # data output length is greater than zero
        self.assertGreater(len(select_charcode(raw, charecs, charec, language)), 0)   
    
Select the line break delimiter
class TestLinebreaks(unittest.TestCase):
    
    Ensure the line break delimiter can be detected
    def test_detect_linebreaks(self): 
        self.assertEqual(detect_linebreaks(string, linebreaks)[0], 'new line / line feed')
    
    Ensure the line break delimiter can be selected
    lines output length is greater than zero
    def test_select_linebreaks(self): 
        self.assertGreater(len(select_linebreaks(data_decoded, linebreaks, linebreak, n_linebreaks)), 0)   
    
Select the column delimiter
class TestColdim(unittest.TestCase):
    
    Ensure the column delimiter can be detected
    def test_detect_coldim(self): 
        self.assertEqual(detect_coldim(string, coldims)[0], 'comma')
    
    Ensure the column delimiter can be selected
    data output length is greater than zero
    def test_select_linebreaks(self): 
        self.assertGreater(len(select_coldim(lines, coldims, coldim, n_coldims)), 0)   

Header in first line?
class TestHeader(unittest.TestCase):
    
    Ensure the header can be selected
    def test_select_header(self): 
        self.assertEqual(list(select_header(data_cells)), ['"name', 'email', 'department', 'role', 'salary', 'start_date', 'office'])

if __name__ == '__main__':
    unittest.main()
 

# Running 'Tabble'


<img width="1935" height="982" alt="image" src="https://github.com/user-attachments/assets/41dd46ee-1649-42c8-9db2-c4d07b1b49c8" />
