
### ▶ Click the image below to watch the video on YouTube!
<a href="https://youtu.be/15NYxZJi7tU">
  <img src="https://img.youtube.com/vi/15NYxZJi7tU/0.jpg" width="800" height="400" alt="Click to watch">
</a>  



<div align="center">

  
<br/>

<br/>

<br/>

  <p>
    <a href="https://github.com/Vijay-J0shi/HomeZ" target="_blank">
      <img width="100%" src="docs/assets/images/banner-homez.png"></a>
  </p>

<br/>




</div>

# File Selector and Data Processing Tool

## Overview

This is a desktop application built using Python and PyQt5 that allows users to select CSV files, choose a data processing algorithm (Minimum Convex Polygon (MCP) or Kernel Density Estimation (KDE)), and visualize the results through image rendering. It is designed with a sleek, modern user interface that features data visualization, file selection, and result downloading functionalities.

## Features

1. **File Selection**: Allows users to select a CSV file for processing.
2. **Algorithm Selection**: Offers two algorithms for data processing:
   - MCP (Minimum Convex Polygon)
   - KDE (Kernel Density Estimation)
3. **Data Visualization**: Displays the processed images for day and night data.
4. **Error Handling**: Validates inputs and provides feedback for invalid selections.
5. **Download Functionality**: Allows users to save the processed images and data to their local machine.
6. **Back Navigation**: Option to go back to the file selection window.
7. **Resizable Layout**: Adapts to different screen sizes for improved user experience.

## Project Structure

```bash
.
app.py                        # Main entry point for the application
img_ploter.py                 # Contains functions for Kernel Density Estimation (KDE)
minimum_convex_polygon.py      # Contains functions for Minimum Convex Polygon (MCP) computation
requirements.txt               # List of dependencies
nature.jpg                   # Background image used in the application
README.md                     # This README file
assets/                       # Folder for assets (images, logos, etc.)
```

