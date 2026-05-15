import os
import re
import json

# Directory containing chapter files
CHAPTERS_DIR = "./Chapitres"

# Output JavaScript file
OUTPUT_JS = "./chapter-titles.js"

def extract_title(text):
    """Extract the first line as the title"""
    first_line = text.strip().split('\n')[0]
    
    # Extract text between ** markers (bold text) if present
    title_match = re.search(r'\*\*([^\*]+)\*\*', first_line)
    if title_match:
        return title_match.group(1).strip()
    return first_line.strip()

def main():
    chapters_titles = {}
    
    # Check if directory exists
    if not os.path.exists(CHAPTERS_DIR):
        print(f"Error: Directory '{CHAPTERS_DIR}' not found.")
        return
    
    # Get list of chapter files
    files = [f for f in os.listdir(CHAPTERS_DIR) if f.startswith("Chapitre_") and f.endswith(".txt")]
    files.sort()  # Sort files to ensure correct order
    
    print(f"Found {len(files)} chapter files.")
    
    # Extract titles from each file
    for file_name in files:
        try:
            file_path = os.path.join(CHAPTERS_DIR, file_name)
            
            # Extract chapter number from filename
            chapter_match = re.search(r'Chapitre_(\d+)', file_name)
            if not chapter_match:
                continue
                
            chapter_num = int(chapter_match.group(1))
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                title = extract_title(content)
                chapters_titles[chapter_num] = title
                print(f"Chapter {chapter_num}: {title}")
                
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
    
    # Write titles to JavaScript file
    with open(OUTPUT_JS, 'w', encoding='utf-8') as js_file:
        js_file.write(f"// Auto-generated chapter titles\n")
        js_file.write(f"const chapterTitlesData = {json.dumps(chapters_titles, ensure_ascii=False, indent=2)};\n")
    
    print(f"\nSuccess! {len(chapters_titles)} chapter titles saved to {OUTPUT_JS}")

if __name__ == "__main__":
    main()