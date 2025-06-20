import xml.etree.ElementTree as ET
import sys
from datetime import datetime, timedelta
import csv

def get_user_input():
    xml_path = input("Enter path to Nijika XML file: ")
    email = input("Enter your Toggl email address: ")
    return xml_path, email

def parse_xml_to_csv(xml_path, email, output_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    sources = {}
    for source in root.findall('.//sources'):
        source_id = source.find('sourceId').text
        sources[source_id] = {
            'name': source.find('sourceName').text,
            'project': source.find('sourceType').text
        }
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Email', 'Description', 'Start date', 'Start time', 'Duration', 'Project'])
        
        for log in root.findall('.//logs'):
            source_id = log.find('sourceId').text
            created_at = datetime.fromisoformat(log.find('createdAt').text.replace(' +00:00', '+00:00'))
            duration_minutes = int(log.find('duration').text)
            start_time = created_at - timedelta(minutes=duration_minutes)
            duration_formatted = str(timedelta(minutes=duration_minutes))
            
            start_date = start_time.strftime('%Y-%m-%d')
            start_time_formatted = start_time.strftime('%H:%M:%S')
            
            writer.writerow([
                email,
                sources[source_id]['name'],
                start_date,
                start_time_formatted,
                duration_formatted,
                sources[source_id]['project']
            ])
    
    print(f"CSV file created at: {output_path}")

def main():
    xml_path, email = get_user_input()
    
    output_path = 'toggl_import.csv'
    try:
        parse_xml_to_csv(xml_path, email, output_path)
        print("\nSuccessfully created Toggl import CSV.")
        print("You can now import this file through the Toggl website:")
        print("1. Go to https://track.toggl.com")
        print("2. Click on 'Settings' -> 'CSV import'")
        print("3. Drag and drop the CSV file into the import window")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()