# Custom Icons Guide

## How to Replace Icons with Your Own Images

The PDF Converter app now uses custom icons instead of Font Awesome icons. You can easily replace these with your own images.

### Current Icon Files

The app currently uses these SVG icons:
- `static/images/pdf-icon.svg` - PDF file icon
- `static/images/word-icon.svg` - Word document icon

### How to Replace Icons

#### Option 1: Replace SVG Files (Recommended)
1. **Create your own SVG icons** (48x48px recommended)
2. **Replace the existing files**:
   - Replace `static/images/pdf-icon.svg` with your PDF icon
   - Replace `static/images/word-icon.svg` with your Word icon
3. **Keep the same filenames** so the CSS references work

#### Option 2: Use PNG/JPG Images
1. **Create your image files** (48x48px recommended)
2. **Save them as**:
   - `static/images/pdf-icon.png` (or .jpg)
   - `static/images/word-icon.png` (or .jpg)
3. **Update the CSS** in the templates:
   - Change `background-image: url('/static/images/pdf-icon.svg')` to `background-image: url('/static/images/pdf-icon.png')`
   - Change `background-image: url('/static/images/word-icon.svg')` to `background-image: url('/static/images/word-icon.png')`

### Icon Sizes

- **Download page icons**: 48x48px
- **File selection page icons**: 64x64px  
- **Navigation icons**: 20x20px

### Supported Formats

- **SVG** (recommended - scalable, small file size)
- **PNG** (good quality, transparent background)
- **JPG** (smaller file size, no transparency)

### Tips for Good Icons

1. **Use transparent backgrounds** for better integration
2. **Keep file sizes small** (< 10KB per icon)
3. **Use consistent colors** that match your app theme
4. **Test on different screen sizes** to ensure they look good

### Example Custom Icon

Here's a simple example of a custom PDF icon you could create:

```svg
<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="8" fill="#FF4444"/>
  <path d="M12 12H36V16H12V12Z" fill="white"/>
  <path d="M12 20H36V24H12V20Z" fill="white"/>
  <path d="M12 28H32V32H12V28Z" fill="white"/>
  <path d="M12 36H24V40H12V36Z" fill="white"/>
  <text x="24" y="45" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="10" font-weight="bold">PDF</text>
</svg>
```

### Testing Your Icons

1. **Save your icon files** to the `static/images/` folder
2. **Restart the Flask app** if it's running
3. **Test the icons** on different pages:
   - Home page navigation
   - File selection page
   - Download page

The icons will automatically update across all pages once you replace the files! 