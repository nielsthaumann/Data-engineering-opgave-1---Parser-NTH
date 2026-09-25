# Data engineering opgave 1 - Parser NTH

Building, testing, and running a table data parser, 'Tabble', for converting CVS-file to JSON-file.  


# Step 1. Read table data and out as binary data and a string
    
        Syntax:     raw, string = readtable(filepath)


# Step 2. Detect character encoding standard
        
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


# Step 3. Select character encoding standard
        
        Syntax: 
            
            data = select_charcode(raw, charecs, charec, language)
            
            
        Input: 
            
            raw:        Raw data as bytes (output from readtable)
            
            charecs:    List with possible character encoding standards (e.g., ['UTF-8', 'ISO 8859-1', 'Windows-1252', 'UTF-16', 'UTF-32'])
        
            charec:     Detected character encoding standard (e.g., 'UTF-8')
            
            language:   Name of detected language
            
        
        Output: 
            
            data_decoded:       Decoded data


# Step 4. Select the column delimiter
    
        Syntax:   coldim, n_coldims = detect_coldim(string, coldims)
        
        Input:   
            
                  string:    Raw data as string (output from readtable)
                  
                  coldims:   2d list with possible column delimiter types and character sequences (e.g., [['tab', 'comma', 'double quotes', 'backslash', 'semicolon', 'pipe', 'space'], [r'\t', r',', r'"', r'\\', r';', r'\|', r'\s']])
            
        Output:   
            
                  coldim:       Detected column delimiter type
                  
                  n_coldims:    Number of column delimiter character sequences

# Step 5: Header in first line?
    
        Syntax:   dataframe = select_header(data_cells)
        
# Step 6: Select cell data format
        
        Syntax:   dataframe = select_cellform(dataframe)



Testing 


Running



<img width="1935" height="982" alt="image" src="https://github.com/user-attachments/assets/41dd46ee-1649-42c8-9db2-c4d07b1b49c8" />
