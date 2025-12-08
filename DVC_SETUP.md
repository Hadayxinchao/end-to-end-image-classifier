# DVC Setup Instructions

## Initial Setup

1. Initialize DVC in your project:
```bash
dvc init
```

2. Track your data directory:
```bash
dvc add data/raw
```

3. Add remote storage (choose one):

### Option 1: Google Drive
```bash
dvc remote add -d storage gdrive://YOUR_FOLDER_ID
```

### Option 2: Local storage (for testing)
```bash
dvc remote add -d storage /tmp/dvc-storage
```

### Option 3: AWS S3
```bash
dvc remote add -d storage s3://mybucket/path
```

4. Commit DVC files to Git:
```bash
git add data/raw.dvc .dvc/config .dvcignore
git commit -m "Add data tracking with DVC"
```

5. Push data to remote storage:
```bash
dvc push
```

## Using DVC

### Pull data from remote
```bash
dvc pull
```

### Update data
```bash
# Modify your data
dvc add data/raw
git add data/raw.dvc
git commit -m "Update dataset"
dvc push
```

### Check data status
```bash
dvc status
```

### Get data version from specific commit
```bash
git checkout <commit-hash>
dvc pull
```

## Remote Storage Configuration

The `.dvc/config` file will be created automatically. Example:

```ini
[core]
    remote = storage
['remote "storage"']
    url = gdrive://YOUR_FOLDER_ID
```

For private repositories or authentication:
```bash
dvc remote modify storage gdrive_use_service_account true
```
