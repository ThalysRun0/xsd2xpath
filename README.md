# xsd2xpath
A simple tool that generate xpath from XSD file, might be useful for mapping purposes

# xsd2xpath.py
This is a way to generate xpath to point information on xml files  
to generate the list of xpath you need the XSD file from wich the XML file derives  
exemples : https://www.iso20022.org/iso-20022-message-definitions

in order to use it properly, you must prior build a virtual env  
```bash
cd <whatever>

python -m venv xsd2xpath

source xsd2xpath/bin/activate  
# if on windows it might be 
xsd2xpath/Scripts/activate

python -m pip install --upgrade pip
pip install lxml

``` 

now you are ready to get some xpath produced  

The python script managed 2 arguments  
- file_path : is a valid path to XSD file
- root_element : is a point in the XML hyerarchy from wich you want to get xpath   

call the python script with :  
```bash
python xsd2xpath.py <file_path> <root_element>
```

This will produce in stdOut the list of xpath that can be defines within the XSD syntax  
and some other properties that might be useful or not  
