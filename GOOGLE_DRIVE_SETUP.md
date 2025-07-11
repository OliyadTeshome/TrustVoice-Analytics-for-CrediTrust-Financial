# Google Drive Setup Guide

This guide explains how to set up Google Drive integration for downloading your vector store and data files.

## 🔐 Prerequisites

1. **Google Account** - You need a Google account
2. **Google Drive API** - Enable the Google Drive API
3. **Credentials** - Create OAuth 2.0 credentials

## 📋 Step-by-Step Setup

### 1. Enable Google Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "Library"
4. Search for "Google Drive API"
5. Click on "Google Drive API" and enable it

### 2. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application" as the application type
4. Give it a name (e.g., "TrustVoice Analytics")
5. Click "Create"
6. Download the credentials JSON file

### 3. Set Up Credentials

#### Option A: Using Credentials File (Recommended)

1. Place the downloaded credentials file in `google_drive/credentials.json`
2. The file structure should be:
   ```
   google_drive/
   ├── credentials.json    # Your OAuth credentials
   └── token.json         # Will be created automatically
   ```

#### Option B: Using Environment Variables

Set these environment variables:
```bash
export GOOGLE_DRIVE_CLIENT_ID="your_client_id"
export GOOGLE_DRIVE_CLIENT_SECRET="your_client_secret"
export GOOGLE_DRIVE_REFRESH_TOKEN="your_refresh_token"
```

### 4. Update Folder ID

The folder ID is already configured in `config.py`:
```python
GOOGLE_DRIVE_FOLDER_ID = "1HBvnKK6oTGSu3XLZrofQCWdD18Siens0?usp=sharing"
```

If you need to change it, update this value in `config.py`.

## 🚀 Usage

### 1. Sync Data from Google Drive

```bash
# Run the sync script
python sync_data.py
```

### 2. Test the RAG Pipeline

```bash
# Test the pipeline
python src/rag_pipeline.py
```

### 3. Start the Application

```bash
# Start Streamlit app
streamlit run src/app.py
```

## 📁 File Structure

After setup, your project structure will be:

```
TrustVoice-Analytics-for-CrediTrust-Financial/
├── src/
│   ├── app.py                    # Streamlit application
│   ├── rag_pipeline.py          # RAG pipeline
│   └── google_drive_client.py   # Google Drive client
├── data/                         # Downloaded data files
│   ├── raw/                      # Raw data files
│   └── filtered/                 # Processed data
├── vector_store/                 # ChromaDB vector store
│   └── chromadb_sample_dataset/  # Downloaded from Google Drive
├── google_drive/                 # Google Drive credentials
│   ├── credentials.json          # OAuth credentials
│   └── token.json               # Access token (auto-generated)
├── config.py                     # Configuration
├── sync_data.py                  # Data sync script
└── GOOGLE_DRIVE_SETUP.md        # This file
```

## 🔧 Troubleshooting

### Authentication Issues

1. **"No Google Drive credentials found"**
   - Ensure `google_drive/credentials.json` exists
   - Check file permissions
   - Verify JSON format is correct

2. **"Authentication failed"**
   - Delete `google_drive/token.json` and try again
   - Check if credentials are valid
   - Ensure Google Drive API is enabled

3. **"Folder not found"**
   - Verify the folder ID is correct
   - Ensure the folder is shared with your account
   - Check folder permissions

### Download Issues

1. **"No files found"**
   - Check if files exist in the Google Drive folder
   - Verify folder ID is correct
   - Ensure files are not in subfolders

2. **"Download failed"**
   - Check internet connection
   - Verify file permissions
   - Try downloading individual files

### Vector Store Issues

1. **"ChromaDB collection not found"**
   - Run `python src/rag_pipeline.py` to create collection
   - Check if vector store files were downloaded correctly

2. **"Embedding model error"**
   - Ensure sentence-transformers is installed
   - Check internet connection for model download

## 🔒 Security Notes

- **Never commit credentials** to version control
- **Use environment variables** for production
- **Regularly rotate** OAuth tokens
- **Monitor API usage** in Google Cloud Console

## 📞 Support

If you encounter issues:

1. Check the logs in the console output
2. Verify all prerequisites are met
3. Test with a simple file first
4. Contact the development team

## 🎯 Next Steps

After successful setup:

1. **Test the pipeline** with your data
2. **Customize the RAG pipeline** for your specific needs
3. **Deploy the application** to your server
4. **Monitor performance** and optimize as needed

---

**Happy analyzing! 🚀** 