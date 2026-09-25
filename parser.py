'''

--- Data engineering opgave 1: Parser ---
    
    X Read table data as binary data and a string
    
    X Select the character encoding standard
    
    X Select the line break delimiter
    
    X Select the column delimiter
    
    X Header in first line?
    
    X Export to JSON for API comptabality
    
'''

# X Skriv og kør unit tests.  
# 
# Sammenligne resultat af Excels text/csv parser med restultat fra egen kode:
# 
# X Der bruges en line break sekvens i sogne.dawa, som parseren ikke genkender. 
#   > Brug '\\' til at definere hver escape sekvens, istedet for r'\'.
#   X Erstat r'\r\n' med '\\r\\n'. 
#   X Til autodetection optælnings index, søg først efter længste character sequences, 
#     der kan være sammensat af mindre character sequences. 
# 
# X Timestamps og koordinater i sogne.dawa parses anderledes af Excel. 
#   > Excel parser forkert. Behold geotag koordinater i float format: 
#     https://web.archive.org/web/20080513102502/http://geotags.com/geo/geotags2.html
# 
# X Vis brugeren resultatet og se om det giver mening (se hvor meget detection kan nås). 
# 

# Import required libaries
import numpy as np
import pandas as pd
import pycld2 as cld2
import re
from datetime import datetime
import unittest
import pathvalidate


# %% Read table data as binary data and a string

# Input file path
folderpath = 'C:\\Users\\NielsHumann\\Documents\\Specialisterne Academy\\Opgave 1 - Parser'
filename   = 'employees.ascii.csv'
# filename = 'sogne.dawa.csv'
filepath   = folderpath + '\\' + filename

def readtable(filepath): 
    '''
        Syntax:     raw, string = readtable(filepath)
    '''
    
    # Open input file as bytes
    print(f'\nImporting table data from {filepath}')
    
    file_opened = False
    try:
        file = open(filepath, 'rb')
        file_opened = True
        
        raw = file.read()
            
        # Store the raw bytes as a string
        string = str(raw)
        
    except FileNotFoundError:
        print('The file was not found.')
    except ValueError:
        print('The file is not open.')
    except UnicodeDecodeError as e:
        print(f'Python cannot decode bytes into text using the expected encoding: {e}')
    finally:
        if file_opened:
            file.close()
    
    return raw, string

raw, string = readtable(filepath)


# %% Select the text character encoding standard

# List with possible character encoding standards
# (UTF-8 is also backwards compatible with ASCII.) 
charecs = ['UTF-8', 'ISO 8859-1', 'Windows-1252', 'UTF-16', 'UTF-32']

def detect_charcode(raw, charecs):
    '''
        Detect character encoding standard. 
        
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
        
    '''
    
    # Prepare empty output variables
    percent = [0]*len(charecs) # Percentage of text detected
    language = ['\b']*len(charecs) # Name of detected language
    
    # Loop over possible character encoding standards
    for cid, _ in enumerate(charecs):
        
        try: 
            
            # Parse characters
            charec = raw.decode(charecs[cid])
            
            # Use CLD2 language detection
            # (Note that CLD2 extracts text data, so no text preprocessing is necessary)
            isReliable, textBytesFound, details = cld2.detect(charec)
            
            if isReliable: # If detection was reliable store the ...
                
                percent[cid] = details[0][2] # Percentage of text detected
                language[cid] = details[0][0].capitalize() # Name of detected language
              
        except UnicodeDecodeError as e:
            
            print(e.encoding, e.start, e.end, e.reason)
            
            continue
        
        except:
            
            continue
    
    # Find the best match
    # (If nothing is detected, the first from the charecs list will be used as output)
    charec_id = np.argmax(percent)
    
    # Output the best match
    charec = charecs[charec_id]     # Detected character encoding standard
    percent = percent[charec_id]    # Percentage of text detected
    language = language[charec_id]  # Name of detected language
    
    return charec, percent, language


# Detect character encoding standard
charec, percent, language = detect_charcode(raw, charecs)


def select_charcode(raw, charecs, charec, language): 
    '''
        Select character encoding standard. 
        
        Syntax: 
            
            data = select_charcode(raw, charecs, charec, language)
            
            
        Input: 
            
            raw:        Raw data as bytes (output from readtable)
            
            charecs:    List with possible character encoding standards (e.g., ['UTF-8', 'ISO 8859-1', 'Windows-1252', 'UTF-16', 'UTF-32'])
        
            charec:     Detected character encoding standard (e.g., 'UTF-8')
            
            language:   Name of detected language
            
        
        Output: 
            
            data_decoded:       Decoded data
    '''
    
    index = charecs.index(charec) # First use the detected index
    
    while True: 
        
        # Decode the data
        try: 
            
            data = repr(raw.decode(charecs[index]))
            
        except: 
            print('Something went wrong. Applying UTF-8 decoding.')
            index = 0
            data_decoded = raw.decode(charec)
        
        # Show the parsed data
        print('\n' + data)
        
        # Show the most likely character sequences
        print(f'\nDetected {language} text encoded with {charec}. See {charec} decoding example above. ⬆')
        
        print('\n[P]roceed or [s]elect another?')
        while True: 
            
            c = input('Press p or s and Enter to continue: ')
            
            # Continue on valid user input
            if c in ['p', 's']: 
                
                break
        
        # Select another
        if c=='s': 
            
            while True: 
                
                print('')
                print(pd.DataFrame(charecs, columns=['Select another: ']))
                
                c = input('\nEnter a valid integer and press Enter to continue: ')
                
                # Continue on valid user input
                if int(c) in range(len(charecs)): 
                    
                    index = int(c) # Update the index
                    break
        
        # Proceed
        if c=='p': 
            break
    
    # Decode the data
    data_decoded = repr(raw.decode(charecs[index]))
    
    return data_decoded


# Select character encoding standard
data_decoded = select_charcode(raw, charecs, charec, language)


# %% Select line breaks

# List with possible line break types and character sequences
linebreaks = [['carriage return line feed', 'carriage return', 'new line / line feed'], 
            ['\\r\\n'                    , '\\r',             '\\n'                ]]

# ( https://en.wikipedia.org/wiki/Newline )


def detect_linebreaks(data, linebreaks): 
    '''
        Syntax:   linebreak, n_linebreaks = detect_linebreaks(string, linebreaks)
        
        Input: 
                
                string:        Raw data as string (output from readtable)
                
                linebreaks:    2d list with possible line break types and character sequences (e.g., [['carriage return line feed', 'carriage return', 'new line / line feed'], ['\\r\\n', '\\r', '\\n']])
            
        Outut: 
            
                linebreak:     Detect line break type
                    
                n_linebreaks:  Number of line break character sequences
                
    '''
    
    # Count number of occurences of each possible line break character sequence
    n_linebreaks = [None]*len(linebreaks[1])
    for i, linebreaktype in enumerate(linebreaks[1]):
        
        n_linebreaks[i] = string.count(linebreaktype)
    
    linebreak_id = np.argmax(n_linebreaks) # Separator index
    
    linebreak = linebreaks[0][linebreak_id]

    n_linebreaks = n_linebreaks[linebreak_id]

    return linebreak, n_linebreaks


# Detect line breaks
linebreak, n_linebreaks = detect_linebreaks(string, linebreaks)


def select_linebreaks(data_decoded, linebreaks, linebreak, n_linebreaks): 
    
    '''
        Syntax:   lines = select_linebreaks(data, linebreaks, linebreak, n_linebreaks)
        
        Input: 
                
                data_decoded:  Decoded data
                
                linebreaks:    2d list with possible line break types and character sequences (e.g., [['carriage return line feed', 'carriage return', 'new line / line feed'], ['\\r\\n', '\\r', '\\n']])
                
                linebreak:     Detect line break type
                    
                n_linebreaks:  Number of line break character sequences
                
        Outut: 
            
                lines:         Data parsed into strings of lines 
        
    '''

    index = linebreaks[0].index(linebreak) # First use the detected index
    
    while True: 
        
        # Show the most likely character sequence
        print(f'\nDetected {n_linebreaks} line breaks with {linebreaks[0][index]} character sequence(s) ( {linebreaks[1][index]} ).')
        
        # Parse the data
        lines = data_decoded.split(linebreaks[1][index])
        
        # Show example of the parsed data
        print('\nExample output:')
        lines = pd.DataFrame(lines)
        print(lines.head())
        
        # Ask user to proceed or select another character sequence
        print('\n[P]roceed or [s]elect another?')
        while True: 
            
            c = input('Press p or s and Enter to continue: ')
            
            # Continue on valid user input
            if c in ['p', 's']: 
                
                break
        
        # Select another character sequence
        if c=='s': 
            
            while True: 
                
                print('')
                print(pd.DataFrame(linebreaks[0], columns=['Select another: ']))
                
                c = input('\nEnter a valid integer and press Enter to continue: ')
                
                # Continue on valid user input
                if int(c) in range(len(linebreaks[1])): 
                    
                    index = int(c) # Update the index
                    break
        
        # Proceed
        if c=='p': 
            break
    
    # Parse the table data
    lines = data_decoded.split(linebreaks[1][index])
    
    return lines


# Select line breaks
lines = select_linebreaks(data_decoded, linebreaks, linebreak, n_linebreaks)


# %% Select the column delimiter

# List with possible column delimiter types and character sequences
coldims = [['tab', 'comma', 'double quotes', 'backslash', 'semicolon', 'pipe', 'space'], 
          [r'\t', r',',     r'"'            r'\\',        r';',        r'\|', r'\s'  ]]



def detect_coldim(string, coldims): 
    '''
        
        Syntax:   coldim, n_coldims = detect_coldim(string, coldims)
        
        Input:   
            
                  string:    Raw data as string (output from readtable)
                  
                  coldims:   2d list with possible column delimiter types and character sequences (e.g., [['tab', 'comma', 'double quotes', 'backslash', 'semicolon', 'pipe', 'space'], [r'\t', r',', r'"', r'\\', r';', r'\|', r'\s']])
            
        Output:   
            
                  coldim:       Detected column delimiter type
                  
                  n_coldims:    Number of column delimiter character sequences
                  
    '''
    
    # Count number of occurences of each possible character sequence
    n_coldims = [None]*len(coldims[1])
    for i, coldimtype in enumerate(coldims[1]):
        
        n_coldims[i] = string.count(coldimtype)
    
    coldim_id = np.argmax(n_coldims) # Separator index
    
    coldim = coldims[0][coldim_id]
    
    n_coldims = n_coldims[coldim_id]
    
    return coldim, n_coldims


# Detect column delimiter
coldim, n_coldims = detect_coldim(string, coldims)



def select_coldim(lines, coldims, coldim, n_coldims): 
    '''
        Syntax:   data = select_coldim(lines, coldims, coldim, n_coldims)
            
        Input: 
            
                  lines:        Data parsed into strings of lines 
            
                  coldims:      2d list with possible column delimiter types and character sequences (e.g., [['tab', 'comma', 'double quotes', 'backslash', 'semicolon', 'pipe', 'space'], [r'\t', r',', r'"', r'\\', r';', r'\|', r'\s']])
                  
                  coldim:       Detected column delimiter type
                  
                  n_coldims:    Number of column delimiter character sequences
            
        Output: 
            
                  data_cells:   Data parsed into cells of lines and columns ( data_cells[line or row][column] )
            
    '''
    
    index = coldims[0].index(coldim) # First use the detected index
    while True: 
        
        # Show the most likely character sequence
        print(f'\nDetected {n_coldims} column separators with {coldim} character sequence(s) ( {coldims[1][index]} ).')
        
        # Parse the table data
        data_cells = [None]*len(lines)
        for i, _ in enumerate(lines): # Loop over lines/rows
        
            data_cells[i] = lines[i].split(coldims[1][index]) # data_cells[line or row][column]
        
        # Show example of the parsed data
        print('\nExample output:')
        data = pd.DataFrame(data_cells)
        print(data.head())
        
        print('\n[P]roceed or [s]elect another?')
        while True: 
            
            c = input('Press p or s and Enter to continue: ')
            
            # Continue on valid user input
            if c in ['p', 's']: 
                
                break
        
        # Select another
        if c=='s': 
            
            while True: 
                
                print('')
                print(pd.DataFrame(coldims[0], columns=['Select another: ']))
                
                c = input('\nEnter a valid integer and press Enter to continue: ')
                
                # Continue on valid user input
                if int(c) in range(len(coldims[1])): 
                    
                    index = int(c) # Update the index
                    break
        
        # Proceed
        if c=='p': 
            break
    
    
    # Parse the table data
    data_cells = [None]*len(lines)
    for i, _ in enumerate(lines): # Loop over lines/rows
    
        data_cells[i] = lines[i].split(coldims[1][index]) # data[line/row][column]
        
    return data_cells


# Select column delimiter
data_cells = select_coldim(lines, coldims, coldim, n_coldims)


# %% Header in first line?

# Yes / No

def select_header(data_cells): 
    '''
        Syntax:   dataframe = select_header(data_cells)
    '''
    
    while True: 
        
        # Show example of the parsed data
        print('\nExample output:')
        print(pd.DataFrame(data_cells).head())
        
        print('\nHeader in first line: [Y]es or [no]?')
        c = input('Press y or n and Enter to continue: ')
        
        # Yes
        if c=='y': 
            
            dataframe = pd.DataFrame(data_cells[1:], columns=data_cells[0])
            return dataframe
            break
        
        # No
        elif c=='n':
            
            dataframe = pd.DataFrame(data_cells)
            return dataframe
            break


dataframe = select_header(data_cells)


# %% Select cell data format


# Use default string format for all cells or detect data format for each cell?

def select_cellform(dataframe): 
    '''
        Syntax:   dataframe = select_cellform(dataframe)
    '''
    
    while True: 
        
        print('\nDetect data format for each cell? [Y]es or [N]o? (NB: This can take a while.)\n')
        c = input('Press y or n and Enter to continue: ')
        
        # Yes
        if c=='y': 
            
            runformatting = True
            break
        
        elif c=='n':
            
            runformatting = False
            break
        
    
    if runformatting:
        
        # Timestamp patterns provided by Claude explained: 
            # ^\d{4}                        : Start with 4 digits year
            # -\d{2}                        : Followed by 2 digit month
            # -\d{2}$                       : Ending with 2 digit day
            # [T ]\d{2}:\d{2}:\d{2}(\.\d+)? : Proceed with 2 digits hour, 2 digits minutes, and 2 digits seconds, perhaps with decimals. 
            # (Z|[+-]\d{2}:?\d{2})?$        : Perhaps ending with time zone
        TIMESTAMP_PATTERNS = [
            r'^\d{4}-\d{2}-\d{2}$',                          # YYYY-MM-DD
            r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$',  # ISO 8601
            r'^\d{2}/\d{2}/\d{4}$',                          # MM/DD/YYYY
            r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$',        # MM/DD/YYYY HH:MM:SS
        ]
        
        # Float parsing provided by Claude explained: 
            # ^[+-]?          : The float pattern might start with + or - sign. 
            # \d+\.\d*        : It has an unknown number of digits with a decimal sign (.) in between digits.
            # |\.\d+          : OR it has a decimal sign (.) followed by an unknown number of digits.
            # \d+             : OR it has an unknown number of digits.
            # ([eE][+-]?\d+)? : It might end with scientific notation, e.g., E-13. 
        FLOAT_PATTERN = r'^[+-]?(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?$'
        
        
        # Detect
        dataframef = dataframe.copy().astype(object) # Copy table data to new table with formatted cells
        for i in range(dataframe.shape[0]): # Loop over lines
            
            print(f'Detecting cell data formats in line {i} of {dataframe.shape[0]}.')
            
            for j in range(dataframe.shape[1]): # Loop over columns
                
                celldata = str(dataframe.iloc[i,j]) # (In case of empty cells (nan), make sure to convert to a string)
                
                # String
                # (default format type)
                
                # If float pattern is detected
                if re.match(FLOAT_PATTERN, celldata):
                    
                    # Convert to float
                    try: 
                        dataframef.iloc[i,j] = float(celldata)
                    except ValueError:
                        pass
                
                #  If time stamp pattern is detected
                for pattern in TIMESTAMP_PATTERNS: 
                    
                    if re.match(pattern, celldata): 
                        
                        # Convert to time stamp using specific time format
                        if pattern==TIMESTAMP_PATTERNS[0]: # YYYY-MM-DD
                                
                                timeform = '%Y-%m-%d'
                                dataframef.iloc[i,j] = datetime.strptime(celldata, timeform)
                                
                        elif pattern==TIMESTAMP_PATTERNS[1]: # ISO 8601
                                
                                dataframef.iloc[i,j] = datetime.fromisoformat(celldata)
                                
                        elif pattern==TIMESTAMP_PATTERNS[2]: # MM/DD/YYYY
                            
                                timeform = '%m/%D/%Y'
                                dataframef.iloc[i,j] = datetime.strptime(celldata, timeform)
                                
                        elif pattern==TIMESTAMP_PATTERNS[3]: # MM/DD/YYYY HH:MM:SS
                            
                                timeform  = '%m/%D/%Y %H:%M:%S'
                                dataframef.iloc[i,j] = datetime.strptime(celldata, timeform)
                
                dataframe = dataframef
                
    # Show the parsed data
    print(dataframe)
    
    return dataframe

dataframe = select_cellform(dataframe)


# %% Export to JSON

print(f'Saving table to {filename[0:-4]}.json')
dataframe.to_json(folderpath + '\\' + filename[0:-4] + '.json', date_format='iso')


# %% Unit tests

# Import table content as a string
class TestReadtable(unittest.TestCase): # (Inherits from unittest.TestCase, making it a test case class)
    
    # Ensure the file path is a valid file path
    def test_filepath(self):
        folderpath = 'C:\\Users\\NielsHumann\\Documents\\Specialisterne Academy\\Opgave 1 - Parser'
        filename   = 'employees.ascii.csv'
        # filename = 'sogne.dawa.csv'
        filepath   = folderpath + '\\' + filename
        self.assertTrue(pathvalidate.is_valid_filepath(filepath, platform='auto'))
    
    # Ensure the data can be read
    def test_fileread(self): 
        # raw output length is greater than zero
        self.assertGreater(len(readtable(filepath)[0]), 0)
    
    # Ensure the raw bytes can be converted to a string
    def test_bytes2string(self): 
        # string output length is greater than zero
        self.assertGreater(len(readtable(filepath)[1]), 0)

# Select the character encoding standard
class TestDetect_charcode(unittest.TestCase):
    
    # Ensure the character encoding standard can be detected
    def test_detect_charcode(self): 
        self.assertEqual(detect_charcode(raw, charecs)[0], 'UTF-8')
    
    # Ensure the character encoding standard can be selected
    def test_select_charcode(self): 
        # data output length is greater than zero
        self.assertGreater(len(select_charcode(raw, charecs, charec, language)), 0)   
    
# Select the line break delimiter
class TestLinebreaks(unittest.TestCase):
    
    # Ensure the line break delimiter can be detected
    def test_detect_linebreaks(self): 
        self.assertEqual(detect_linebreaks(string, linebreaks)[0], 'new line / line feed')
    
    # Ensure the line break delimiter can be selected
    # lines output length is greater than zero
    def test_select_linebreaks(self): 
        self.assertGreater(len(select_linebreaks(data_decoded, linebreaks, linebreak, n_linebreaks)), 0)   
    
# Select the column delimiter
class TestColdim(unittest.TestCase):
    
    # Ensure the column delimiter can be detected
    def test_detect_coldim(self): 
        self.assertEqual(detect_coldim(string, coldims)[0], 'comma')
    
    # Ensure the column delimiter can be selected
    # data output length is greater than zero
    def test_select_linebreaks(self): 
        self.assertGreater(len(select_coldim(lines, coldims, coldim, n_coldims)), 0)   

# Header in first line?
class TestHeader(unittest.TestCase):
    
    # Ensure the header can be selected
    def test_select_header(self): 
        self.assertEqual(list(select_header(data_cells)), ['"name', 'email', 'department', 'role', 'salary', 'start_date', 'office'])

if __name__ == '__main__':
    unittest.main()

