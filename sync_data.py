#!/usr/bin/env python3
"""
Data synchronization script for TrustVoice Analytics
Downloads vector store and data files from Google Drive
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from google_drive_client import GoogleDriveClient
from config import create_directories

def main():
    """Main function to sync data from Google Drive"""
    print("🔄 TrustVoice Analytics - Data Synchronization")
    print("=" * 50)
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Initialize Google Drive client
    print("\n🔐 Initializing Google Drive client...")
    client = GoogleDriveClient()
    
    # Sync all files
    print("\n📥 Starting data synchronization...")
    success = client.sync_all_files()
    
    if success:
        print("\n✅ Data synchronization completed successfully!")
        print("\n📋 Next steps:")
        print("1. Set up Google Drive credentials (if not already done)")
        print("2. Run the RAG pipeline: python src/rag_pipeline.py")
        print("3. Start the Streamlit app: streamlit run src/app.py")
    else:
        print("\n❌ Data synchronization failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Check your Google Drive credentials")
        print("2. Ensure the folder ID is correct")
        print("3. Verify internet connection")
        print("4. Check file permissions")

if __name__ == "__main__":
    main() 