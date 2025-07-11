"""
Google Drive client for downloading vector store and data files
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Optional
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

from config import (
    GOOGLE_DRIVE_FOLDER_ID,
    GOOGLE_DRIVE_CREDENTIALS_FILE,
    GOOGLE_DRIVE_TOKEN_FILE,
    VECTOR_STORE_DIR,
    DATA_DIR
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleDriveClient:
    """Client for downloading files from Google Drive"""
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        
    def authenticate(self) -> bool:
        """Authenticate with Google Drive API"""
        try:
            # Load existing credentials
            if GOOGLE_DRIVE_TOKEN_FILE.exists():
                self.credentials = Credentials.from_authorized_user_file(
                    str(GOOGLE_DRIVE_TOKEN_FILE), self.SCOPES
                )
            
            # If no valid credentials, get new ones
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    # Try to load credentials from environment variables
                    credentials_info = self._get_credentials_from_env()
                    if credentials_info:
                        self.credentials = Credentials.from_authorized_user_info(
                            credentials_info, self.SCOPES
                        )
                    else:
                        # Fallback to credentials file
                        if GOOGLE_DRIVE_CREDENTIALS_FILE.exists():
                            flow = InstalledAppFlow.from_client_secrets_file(
                                str(GOOGLE_DRIVE_CREDENTIALS_FILE), self.SCOPES
                            )
                            self.credentials = flow.run_local_server(port=8080)
                        else:
                            logger.error("No Google Drive credentials found")
                            return False
                
                # Save credentials for next run
                with open(GOOGLE_DRIVE_TOKEN_FILE, 'w') as token:
                    token.write(self.credentials.to_json())
            
            # Build the service
            self.service = build('drive', 'v3', credentials=self.credentials)
            logger.info("✅ Google Drive authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Google Drive authentication failed: {e}")
            return False
    
    def _get_credentials_from_env(self) -> Optional[dict]:
        """Get credentials from environment variables"""
        client_id = os.getenv("GOOGLE_DRIVE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN")
        
        if client_id and client_secret and refresh_token:
            return {
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        return None
    
    def list_files_in_folder(self, folder_id: str) -> List[dict]:
        """List all files in a Google Drive folder"""
        try:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                pageSize=1000,
                fields="nextPageToken, files(id, name, mimeType, size)"
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"Found {len(files)} files in folder")
            return files
            
        except Exception as e:
            logger.error(f"❌ Error listing files: {e}")
            return []
    
    def download_file(self, file_id: str, file_name: str, destination_path: Path) -> bool:
        """Download a file from Google Drive"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.info(f"Downloading {file_name}: {int(status.progress() * 100)}%")
            
            # Save the file
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            with open(destination_path, 'wb') as f:
                f.write(file.getvalue())
            
            logger.info(f"✅ Downloaded: {file_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error downloading {file_name}: {e}")
            return False
    
    def download_vector_store(self) -> bool:
        """Download the ChromaDB vector store from Google Drive"""
        try:
            if not self.authenticate():
                return False
            
            # List files in the folder
            files = self.list_files_in_folder(GOOGLE_DRIVE_FOLDER_ID)
            
            # Find ChromaDB files
            chroma_files = [f for f in files if 'chroma' in f['name'].lower()]
            
            if not chroma_files:
                logger.warning("No ChromaDB files found in Google Drive folder")
                return False
            
            # Download ChromaDB files
            success_count = 0
            for file in chroma_files:
                file_path = VECTOR_STORE_DIR / file['name']
                if self.download_file(file['id'], file['name'], file_path):
                    success_count += 1
            
            logger.info(f"✅ Downloaded {success_count} ChromaDB files")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error downloading vector store: {e}")
            return False
    
    def download_data_files(self) -> bool:
        """Download data files from Google Drive"""
        try:
            if not self.authenticate():
                return False
            
            # List files in the folder
            files = self.list_files_in_folder(GOOGLE_DRIVE_FOLDER_ID)
            
            # Find data files (CSV, JSON, etc.)
            data_files = [f for f in files if f['name'].lower().endswith(('.csv', '.json', '.xlsx'))]
            
            if not data_files:
                logger.warning("No data files found in Google Drive folder")
                return False
            
            # Download data files
            success_count = 0
            for file in data_files:
                file_path = DATA_DIR / file['name']
                if self.download_file(file['id'], file['name'], file_path):
                    success_count += 1
            
            logger.info(f"✅ Downloaded {success_count} data files")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error downloading data files: {e}")
            return False
    
    def sync_all_files(self) -> bool:
        """Sync all files from Google Drive"""
        logger.info("🔄 Starting Google Drive sync...")
        
        # Download vector store
        vector_success = self.download_vector_store()
        
        # Download data files
        data_success = self.download_data_files()
        
        if vector_success or data_success:
            logger.info("✅ Google Drive sync completed")
            return True
        else:
            logger.error("❌ Google Drive sync failed")
            return False

def main():
    """Main function to test Google Drive client"""
    client = GoogleDriveClient()
    success = client.sync_all_files()
    
    if success:
        print("✅ Google Drive sync successful!")
    else:
        print("❌ Google Drive sync failed!")

if __name__ == "__main__":
    main() 