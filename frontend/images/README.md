# PDS Login Page Images

This directory contains images for the login page carousel.

## Setup Instructions

To use the PDS distribution system images in the login carousel:

### Option 1: Save Images Directly (Recommended)

1. Add your PDS distribution images to this folder:
   - `pds-distribution-1.jpg` - First carousel image
   - `pds-distribution-2.jpg` - Second carousel image

2. Images should be:
   - Format: JPG, PNG, or WebP
   - Dimensions: Minimum 400x300px, recommended 600x400px or larger
   - File size: Under 500KB (for optimal loading)
   - Content: Clear, professional photos of PDS operations, distribution centers, or fair price shops

### Option 2: Add More Images

To add more images to the carousel:

1. Save additional images as `pds-distribution-3.jpg`, `pds-distribution-4.jpg`, etc.

2. Edit `frontend/login.html` and update the `carouselImages` array:

```javascript
const carouselImages = [
  { src: 'images/pds-distribution-1.jpg', alt: 'PDS Rice Distribution Center' },
  { src: 'images/pds-distribution-2.jpg', alt: 'PDS Fair Price Shop Operations' },
  { src: 'images/pds-distribution-3.jpg', alt: 'PDS Stock Management' },
  // Add more as needed
];
```

### Image Optimization Tips

- Use compression tools like TinyPNG or ImageOptim
- Crop images to focus on the subject (remove unnecessary background)
- Ensure images have good lighting and clarity
- Use consistent aspect ratios for better carousel appearance

### Current Carousel Features

- Auto-rotation every 5 seconds
- Manual navigation with arrow buttons
- Indicator dots for slide selection
- Smooth fade transitions
- Responsive on all devices

  ### Placeholders

If images are not yet added, the carousel will display a message. Add the image files listed above to enable the carousel display.