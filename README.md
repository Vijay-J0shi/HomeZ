
<br/>

  <p>
    <a href="https://github.com/Vijay-J0shi/HomeZ" target="_blank">
      <img width="100%" src="docs/assets/images/banner-homez.png"></a>
  </p>

<br/>

**Project Report** -> https://drive.google.com/file/d/1Hlg9GqbIr7KhoL2xkuKvghPBDt698qLX/view?usp=drive_link

**Download Application from Here** -> https://drive.google.com/drive/folders/14VNw261UIGDu9GAaL9EH1bntbg5zQ14I?usp=sharing

### ▶ Click the image below to watch the video on YouTube!
<a href="https://youtu.be/15NYxZJi7tU">
  <img src="https://img.youtube.com/vi/15NYxZJi7tU/0.jpg" width="800" height="400" alt="Click to watch">
</a>  


# HomeZ: Kernel Density Estimation and Minimum Convex Polygon

## Overview

This project provides implementations for Kernel Density Estimation (KDE) and Minimum Convex Polygon (MCP) algorithms. These methods are used for spatial analysis and visualization of geographical data points, offering insights into density distributions and convex boundary approximations for datasets. Both algorithms are equipped with visualization features that output results as `.tiff` images.

## Features

1. **Kernel Density Estimation (KDE)**:
   - Visualizes the density of data points using Gaussian Kernel Density Estimation.
   - Supports configurable bandwidth for kernel smoothing.
   - Generates a density plot that is saved in `.tiff` format.

2. **Minimum Convex Polygon (MCP)**:
   - Computes the convex hull that encloses a given set of points.
   - Visualizes the convex polygon and the points, and saves the result as a `.tiff` image.

<div align="center">

  
<br/>

<br/>





</div>

### Scope
HomeZ is a PyQt6-based desktop application that enables users to:
- Upload CSV files containing geospatial data (longitude, latitude, timestamps).
- Perform KDE and MCP analyses with customizable parameters (bandwidth, confidence intervals).
- Visualize day/night movement patterns as TIFF images.
- Export results (images, Excel reports) and view data tables.
- Provide robust error handling and logging for reliability.

### Definitions, Acronyms, and Abbreviations
- **KDE**: Kernel Density Estimation
- **MCP**: Minimum Convex Polygon
- **PyQt6**: Python GUI framework
- **GeoPandas**: Library for geospatial data processing
- **Matplotlib**: Plotting library for visualizations
- **TIFF**: Tagged Image File Format
- **CSV**: Comma-Separated Values

### References
- PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- GeoPandas Documentation: https://geopandas.org/
- Matplotlib Documentation: https://matplotlib.org/

### Product Perspective
HomeZ is a standalone desktop application for ecological researchers, operating independently on user machines. It integrates geospatial data processing (GeoPandas), statistical analysis (SciPy), and visualization (Matplotlib) within a PyQt6 GUI, providing a specialized tool for home range analysis.

### Product Functions
- **File Upload**: Import CSV files with geospatial data (longitude, latitude, timestamps).
- **Data Processing**: Separate day/night coordinates and compute distances/displacements.
- **KDE Analysis**: Generate density maps for day/night data with customizable bandwidth (0-1).
- **MCP Analysis**: Calculate convex hulls with confidence intervals (7-100%) and compute areas.
- **Visualization**: Display day/night KDE/MCP plots as TIFF images in the GUI.
- **Export**: Save TIFF images and Excel reports with distance data.
- **Data View**: Show processed data in a table view.
- **Logging**: Log errors and process steps for debugging.

### User Classes and Characteristics
- **Ecological Researchers**: Primary users analyzing animal movement data, requiring intuitive GUI and reliable outputs.
- **Developers**: Maintainers who debug and extend the application using logs and modular code.

### Operating Environment
- **Platform**: Windows, macOS, Linux (Python 3.10)
- **Libraries**: PyQt6, GeoPandas, Matplotlib, Pandas, NumPy, SciPy
- **Hardware**: Standard desktop/laptop with sufficient memory for geospatial processing

### Design and Implementation Constraints
- Input files must be CSV with columns for longitude, latitude, and timestamps (NST Time).
- KDE requires at least 2 points; MCP requires at least 3 points.
- Visualizations are limited to TIFF format.
- Non-interactive Matplotlib backend (`Agg`) for compatibility.

### Assumptions and Dependencies
- **Assumptions**:
  - Users provide valid CSV files with required columns.
  - System has sufficient memory for large datasets.
- **Dependencies**:
  - Python libraries: `pyqt6`, `geopandas`, `matplotlib`, `pandas`, `numpy`, `scipy`
  - System: Python 3.10, compatible OS

HomeZ has a MIT-style license, as found in the MIT License file.

- **MIT Licence**: This [OSI-approved](https://opensource.org/licenses/) open-source license is ideal for students and enthusiasts, promoting open collabaration and knowledge sharing. See the [MIT License](https://github.com/Vijay-J0shi/HomeZ/blob/main/LICENSE) file for more details.
