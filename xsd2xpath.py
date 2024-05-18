import lxml.etree as ET
from typing import List
import sys

def generate_xpaths_from_xsd(file_path: str, root_element: str) -> List[str]:
    
    try:
        schema_tree: ET.ElementTree = ET.parse(file_path)
        schema_root: ET.Element = schema_tree.getroot()
        
        ns_map: dict = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        
        xpaths: List[str] = []
        
        def get_xpath(element: ET.Element, current_path: str = '') -> None:
            
            choice: ET.Element = element.find('xs:choice', namespaces=ns_map)
            if choice is not None:
                for child in choice.findall('xs:element',  namespaces=ns_map):
                    get_xpath(child, f"{current_path}/{child.get('name', '')}")
                    
            sequence: ET.Element = element.find('xs:sequence', namespaces=ns_map)
            if sequence is not None:
                for child in sequence.findall('xs:element', namespaces=ns_map):
                    get_xpath(child, f"{current_path}/{child.get('name', '')}")
            
            unnamed_complex_type: ET.Element = element.find('xs:complexType', namespaces=ns_map)
            if unnamed_complex_type is not None:
                get_xpath(unnamed_complex_type, current_path)
            
            custom_type: ET.Element = None
            custom_type_name: str = element.get('type', '')
#            print(f".//xs:complexType[@name='{custom_type_name}']")
            custom_complex_type:ET.Element = schema_root.find(f".//xs:complexType[@name='{custom_type_name}']", namespaces=ns_map)
#            print(f".//xs:simpleType[@name='{custom_type_name}']")
            custom_simple_type:ET.Element = schema_root.find(f".//xs:simpleType[@name='{custom_type_name}']", namespaces=ns_map)
            
            if custom_simple_type is not None:
                custom_type = custom_simple_type
            
            if custom_complex_type is not None:
                custom_type = custom_complex_type
                
            if custom_type is not None:
                get_xpath(custom_type, current_path)
            else:
                restriction: ET.Element = element.find('xs:restriction', namespaces=ns_map)
                element_type: str = ""
                type_values: List[str] = []
                if restriction is not None:
                    for item in restriction:
                        type_values.append(item.get('value', ''))
                    element_type = f"{element.get('name', '')}::{restriction.get('base', '')} <= [{type_values}]"
                else:
                    element_type = element.get('type', '')
                if element_type != "":
                    xpaths.append(f"{current_path} [@type='{element_type}']")
            
#        print(f".//xs:element[@name='{root_element}']")
        document_root: ET.Element = schema_root.find(f".//xs:element[@name='{root_element}']", namespaces=ns_map)
        if document_root is not None:
            get_xpath(document_root, f"/{root_element}")
        return xpaths

    except ET.XMLSyntaxError as e:
        print(f"Error parsing XSD file : {e}")
        return []
    except Exception as e:
        print(f"Error unmanaged : {e}")
        return []
    
if __name__ == "__main__":
    print(sys.argv)
    for xpath in generate_xpaths_from_xsd(sys.argv[1], sys.argv[2]):
        print(xpath)
        
