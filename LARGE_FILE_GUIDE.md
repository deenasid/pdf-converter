# Large File Handling Guide

## Overview

This guide explains the improvements made to handle large files in the PDF Converter application. The application now supports files up to 100MB with better error handling, progress tracking, and timeout management.

## Key Improvements

### 1. Increased File Size Limit
- **Previous limit**: 16MB
- **New limit**: 100MB
- **Configuration**: Updated `MAX_CONTENT_LENGTH` in `app.py`

### 2. File Size Validation
- **Frontend validation**: Files over 100MB are rejected before upload
- **Backend validation**: Additional server-side checks
- **User feedback**: Clear error messages for oversized files

### 3. Progress Tracking
- **Visual progress bar**: Shows for files larger than 10MB
- **File size warnings**: Different messages for medium (10-50MB) and large (50MB+) files
- **Real-time feedback**: Users know when processing large files

### 4. Timeout Management
- **Adaptive timeouts**: Longer timeouts for larger files
  - Default: 5 minutes (300 seconds)
  - 20-50MB: 7.5 minutes (450 seconds)
  - 50MB+: 10 minutes (600 seconds)
- **Thread-based execution**: Prevents hanging conversions
- **Automatic cleanup**: Removes partial files on timeout

### 5. Improved Download Handling
- **Streaming downloads**: For files larger than 50MB
- **Conditional requests**: Better caching and resume support
- **Error recovery**: Graceful handling of download failures

## File Size Categories

| File Size | Category | Timeout | User Warning |
|-----------|----------|---------|--------------|
| < 10MB | Small | 5 min | None |
| 10-50MB | Medium | 7.5 min | "Please be patient during conversion" |
| 50-100MB | Large | 10 min | "Conversion may take several minutes" |
| > 100MB | Too Large | Rejected | "File size exceeds 100MB limit" |

## Technical Implementation

### Backend Changes

1. **Timeout Handler** (`app.py`):
```python
def run_with_timeout(func, args, timeout_seconds=300):
    # Thread-based execution with timeout
```

2. **File Size Validation**:
```python
if file_size > 100 * 1024 * 1024:
    raise Exception("File size exceeds 100MB limit")
```

3. **Adaptive Timeouts**:
```python
if file_size > 50 * 1024 * 1024:
    timeout_seconds = 600  # 10 minutes
elif file_size > 20 * 1024 * 1024:
    timeout_seconds = 450  # 7.5 minutes
```

### Frontend Changes

1. **File Size Validation** (`select_file.html`):
```javascript
const maxSize = 100 * 1024 * 1024; // 100MB
if (file.size > maxSize) {
    showError('File size exceeds 100MB limit');
    return false;
}
```

2. **Progress Bar**:
```javascript
if (file.size > 10 * 1024 * 1024) {
    progressBar = createProgressBar();
}
```

3. **File Size Warnings**:
```javascript
if (file.size > 50 * 1024 * 1024) {
    fileSizeWarning.textContent = '⚠️ Large file detected...';
}
```

## Usage Instructions

### For Users

1. **Upload Large Files**:
   - Select files up to 100MB
   - Wait for size validation
   - Monitor progress for files > 10MB

2. **Monitor Progress**:
   - Small files: Quick conversion
   - Medium files: Watch for progress bar
   - Large files: Be patient, may take several minutes

3. **Download Results**:
   - Small files: Direct download
   - Large files: Streaming download with resume support

### For Developers

1. **Testing Large Files**:
```bash
python test_large_files.py
```

2. **Monitoring Logs**:
```bash
# Check for timeout and size validation messages
tail -f app.log
```

3. **Adjusting Limits**:
```python
# In app.py
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

## Troubleshooting

### Common Issues

1. **"File size exceeds 100MB limit"**
   - **Solution**: Use a smaller file or split the document

2. **"Conversion timed out"**
   - **Solution**: Try with a smaller file or check server resources

3. **"Download failed"**
   - **Solution**: Check network connection and try again

4. **"File not found"**
   - **Solution**: File may have been cleaned up, upload again

### Performance Tips

1. **For Very Large Files**:
   - Consider splitting documents before conversion
   - Use during off-peak hours
   - Ensure stable internet connection

2. **Server Optimization**:
   - Monitor memory usage during large conversions
   - Consider increasing server resources for high traffic
   - Implement file cleanup to prevent disk space issues

## Configuration Options

### Timeout Settings
```python
# Default timeout (5 minutes)
timeout_seconds = 300

# Medium files (7.5 minutes)
timeout_seconds = 450

# Large files (10 minutes)
timeout_seconds = 600
```

### File Size Limits
```python
# Maximum upload size
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

# Progress bar threshold
PROGRESS_THRESHOLD = 10 * 1024 * 1024  # 10MB

# Streaming download threshold
STREAMING_THRESHOLD = 50 * 1024 * 1024  # 50MB
```

## Security Considerations

1. **File Validation**: All files are validated for type and size
2. **Path Security**: Filenames are sanitized using `secure_filename()`
3. **Resource Limits**: Timeouts prevent resource exhaustion
4. **Cleanup**: Temporary files are automatically removed

## Future Improvements

1. **Chunked Uploads**: Support for files larger than 100MB
2. **Background Processing**: Queue-based conversion for very large files
3. **Progress API**: Real-time progress updates via WebSocket
4. **Resume Support**: Resume interrupted uploads
5. **Compression**: Automatic compression for large output files

## Support

For issues with large file handling:
1. Check the application logs
2. Verify file size and format
3. Test with smaller files first
4. Contact support with error messages and file details 