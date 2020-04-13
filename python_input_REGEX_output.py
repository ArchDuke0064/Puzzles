# Regular Expression Substitution Input/Output Python Script
import re
# define file input/output
_file_in_  = r"c:\py_A\1a.ZZZ" #csv" #tab" #dat" #txt"
_file_out_ = r"c:\py_A\1b.ZZZ" #csv" #tab" #dat" #txt"
# cmd.exe -- c:\python.3.7.2\python.exe c:\py_A\ZZZ.py
_non_char_ = r"([^|[]{}<>%`~!@_=:;',/\.\"\?\$\^\&\*\(\)\+\-\\a-zA-Z0-9\t\r\n])"
_symbol_   =  r"([|[]{}<>%`~!@_=:;',/\.\"\?\$\^\&\*\(\)\+\-\\]+)"
_word_     = r"([a-zA-Z][a-zA-Z0-9]*)"
# read input file
       _i=open(_file_in_,"r",encoding="utf-8")
text = _i.read()
       _i.close()
# REGEX substitution
text = re.sub(_non_char_,r'',text)
text = re.sub(r'ZZZZZZ1',r'Z1',text)
text = re.sub(r'ZZZZZZ2',r'Z2',text)
text = re.sub(r'ZZZZZZ3',r'Z3',text)
# write output file
_o=open(_file_out_,"w+")
_o.write(text)
_o.close()
# 
