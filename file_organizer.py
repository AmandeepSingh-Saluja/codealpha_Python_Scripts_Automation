import os
import shutil
import logging
from pathlib import Path

class FileOrganizer:
    def __init__(self, source_dir=".....(path).....", log_file='file_organization.log'):
        self.source_dir = source_dir or str(Path.home() / "......")  # Set default downloads path if no directory specified
        logging.basicConfig(
            filename=log_file,                                                                 # Configure logging
            level=logging.INFO, 
            format='%(asctime)s - %(message)s'
        )
        
        self.categories = {                                                                     # Define file type categories
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'Music': ['.mp3', '.wav', '.flac', '.aac'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.json']
        }
    
    def organize_files(self):
        for category in self.categories:
            category_path = os.path.join(self.source_dir, category)   # Create category directories if they don't exist
            os.makedirs(category_path, exist_ok=True)
        
        files_processed = 0       # Track files processed and any errors
        errors = 0
        
        for filename in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, filename)      # Iterate through files in source directory
            
            if os.path.isdir(file_path):
                continue
            
            try:
                
                file_ext = os.path.splitext(filename)[1].lower()
                file_category = self._get_file_category(file_ext)
                
                if not file_category:
                    continue
                
                dest_path = os.path.join(self.source_dir, file_category, filename)
                shutil.move(file_path, dest_path)
                logging.info(f"Moved {filename} to {file_category}")
                files_processed += 1
                
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
                errors += 1
        
        # Print summary
        print(f"File Organization Complete")
        print(f"Files Processed: {files_processed}")
        print(f"Errors Encountered: {errors}")
    
    def _get_file_category(self, extension):
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        return None
    
    def cleanup_empty_files(self):
        zero_byte_files = [
            f for f in os.listdir(self.source_dir) 
            if os.path.isfile(os.path.join(self.source_dir, f)) 
            and os.path.getsize(os.path.join(self.source_dir, f)) == 0
        ]
        
        for file in zero_byte_files:
            file_path = os.path.join(self.source_dir, file)
            try:
                os.remove(file_path)
                logging.info(f"Removed zero-byte file: {file}")
            except Exception as e:
                logging.error(f"Could not remove {file}: {e}")

def main():
    organizer = FileOrganizer()
    organizer.organize_files()
    organizer.cleanup_empty_files()

if __name__ == "__main__":
    main()
