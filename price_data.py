import pandas as pd
import xml.etree.ElementTree as ET

class PriceDataXML:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
    
    def create_xml_feed(self, output_file):
        root = ET.Element('AmazonEnvelope')
        header = ET.SubElement(root, 'Header')
        ET.SubElement(header, 'DocumentVersion').text = '4'
        ET.SubElement(root, 'MessageType').text = 'Price'
        
        # Iterate through each row in the DataFrame
        for i, row in self.df.iterrows():
            message = ET.SubElement(root, 'Message')
            ET.SubElement(message, 'MessageID').text = str(i + 1)
            ET.SubElement(message, 'OperationType').text = 'Update'
            
            price = ET.SubElement(message, 'Price')
            ET.SubElement(price, 'SKU').text = row['SKU']
            ET.SubElement(price, 'StandardPrice', currency="USD").text = str(row['Selling Price'])
            
            # Check if 'BusinessPrice' column exists and is not NaN and if it's different from 'Selling Price'
            if 'Business Price' in self.df.columns and not pd.isna(row.get('Business Price')) and row['Business Price'] != row['Selling Price']:
                ET.SubElement(price, 'BusinessPrice').text = str(row['Business Price'])
        
        # Create XML tree and write to file
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-16', xml_declaration=True)

# Generate XML feed from "Price Data.xlsx"
price_data = PriceDataXML('Price Data.xlsx')
price_data.create_xml_feed('Price_Data.xml')
