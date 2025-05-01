import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from logging_setup import setup_logging
from home_range.kde_img_ploter import kde, dist
from home_range.minimum_convex_polygon import MCP

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='src/static')
app.config['UPLOAD_FOLDER'] = 'src/static/uploads'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Setup logging
logger = setup_logging()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def file_selection():
    return render_template('file_selection.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('file_selection'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('file_selection'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logger.info(f"File uploaded: {file_path}")
        return redirect(url_for('processing', filename=filename))
    else:
        flash('Invalid file format. Only CSV files are allowed.')
        return redirect(url_for('file_selection'))

@app.route('/processing/<filename>', methods=['GET', 'POST'])
def processing(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        flash('File not found')
        return redirect(url_for('file_selection'))

    if request.method == 'POST':
        algorithm = request.form.get('algorithm')
        if not algorithm or algorithm not in ['KDE', 'MCP']:
            flash('Please select an algorithm')
            return redirect(url_for('processing', filename=filename))

        if algorithm == 'KDE':
            bandwidth = request.form.get('bandwidth')
            if not bandwidth:
                flash('Please enter a bandwidth value (0-1)')
                return redirect(url_for('processing', filename=filename))
            try:
                bandwidth = float(bandwidth)
                if not (0 <= bandwidth <= 1):
                    flash('Bandwidth must be between 0 and 1')
                    return redirect(url_for('processing', filename=filename))
            except ValueError:
                flash('Invalid bandwidth value')
                return redirect(url_for('processing', filename=filename))
            
            try:
                logger.info(f"Processing KDE with file: {file_path}, bandwidth: {bandwidth}")
                day_kde, night_kde = kde(file_path, bandwidth)
                day_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'day_kde.tiff')
                night_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'night_kde.tiff')
                
                # Save images
                with open(day_img_path, 'wb') as f:
                    f.write(day_kde.getvalue() if hasattr(day_kde, 'getvalue') else day_kde)
                with open(night_img_path, 'wb') as f:
                    f.write(night_kde.getvalue() if hasattr(night_kde, 'getvalue') else night_kde)
                
                # Prepare data for table
                data = dist(file_path)
                df = pd.DataFrame(data)
                table_html = df.to_html(classes='table table-striped', index=False)
                
                logger.info("KDE processing completed")
                return render_template('processing.html', 
                                     filename=filename, 
                                     algorithm=algorithm, 
                                     day_img='uploads/day_kde.tiff', 
                                     night_img='uploads/night_kde.tiff', 
                                     table=table_html)
            except Exception as e:
                flash(f"Error processing KDE: {str(e)}")
                logger.error(f"KDE processing error: {str(e)}")
                return redirect(url_for('processing', filename=filename))

        elif algorithm == 'MCP':
            confidence = request.form.get('confidence')
            if not confidence:
                flash('Please enter a confidence value (7-100)')
                return redirect(url_for('processing', filename=filename))
            try:
                confidence = float(confidence)
                if not (7 <= confidence <= 100):
                    flash('Confidence must be between 7 and 100')
                    return redirect(url_for('processing', filename=filename))
            except ValueError:
                flash('Invalid confidence value')
                return redirect(url_for('processing', filename=filename))
            
            try:
                logger.info(f"Processing MCP with file: {file_path}, confidence: {confidence}")
                day_mcp, night_mcp, day_area, night_area, total_area = MCP(file_path, 0.5, confidence)
                day_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'day_mcp.tiff')
                night_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'night_mcp.tiff')
                
                # Save images
                with open(day_img_path, 'wb') as f:
                    f.write(day_mcp.getvalue() if hasattr(day_mcp, 'getvalue') else day_mcp)
                with open(night_img_path, 'wb') as f:
                    f.write(night_mcp.getvalue() if hasattr(night_mcp, 'getvalue') else night_mcp)
                
                # Save Excel file
                data = dist(file_path)
                df = pd.DataFrame(data)
                excel_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.xlsx')
                df.to_excel(excel_path, index=False)
                
                table_html = df.to_html(classes='table table-striped', index=False)
                
                logger.info("MCP processing completed")
                return render_template('processing.html', 
                                     filename=filename, 
                                     algorithm=algorithm, 
                                     day_img='uploads/day_mcp.tiff', 
                                     night_img='uploads/night_mcp.tiff', 
                                     day_area=day_area, 
                                     night_area=night_area, 
                                     total_area=total_area, 
                                     table=table_html, 
                                     excel_file='uploads/output.xlsx')
            except Exception as e:
                flash(f"Error processing MCP: {str(e)}")
                logger.error(f"MCP processing error: {str(e)}")
                return redirect(url_for('processing', filename=filename))
    
    # GET request: display processing form
    return render_template('processing.html', filename=filename)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)