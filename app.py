from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import os
import pandas as pd
import io
import numpy as np
from functions import (
    missing_data_summary,
    handle_missing_data,
    duplicate_summary,
    remove_duplicates,
    generate_profile_report,
    split_train_test,
    detect_outliers_iqr,
    remove_outliers_iqr
)

app = Flask(__name__)
app.secret_key = '1925'
app.config["UPLOAD_FOLDER"] = "uploads"
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

data_storage = {}

def make_json_serializable(obj):
    """Convert numpy/pandas types to native Python types for JSON serialization"""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {str(k): make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    else:
        return obj

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", df_exists=False, columns=[], train_shape=None, test_shape=None)

# API Endpoints for AJAX requests
@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file selected"})
    
    uploaded_file = request.files["file"]
    if not uploaded_file or uploaded_file.filename == "":
        return jsonify({"success": False, "message": "No file selected"})
    
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
    uploaded_file.save(filepath)
    
    try:
        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        elif filepath.endswith(".xlsx"):
            df = pd.read_excel(filepath)
        else:
            return jsonify({"success": False, "message": "Unsupported file format! Only CSV or Excel allowed."})
        
        data_storage["df"] = df
        missing_summary = missing_data_summary(df).to_html(classes="table table-striped")
        duplicate_count, _ = duplicate_summary(df)
        
        response_data = {
            "success": True,
            "preview": df.head().to_html(classes="table table-bordered"),
            "shape": [df.shape[0], df.shape[1]],
            "missing_summary": missing_summary,
            "duplicate_count": duplicate_count,
            "show_missing_options": True,
            "show_duplicate_options": duplicate_count > 0,
            "columns": df.columns.tolist(),
            "message": "Dataset uploaded successfully!"
        }
        
        return jsonify(make_json_serializable(response_data))
    except Exception as e:
        return jsonify({"success": False, "message": f"Error reading file: {e}"})

@app.route("/api/handle_missing", methods=["POST"])
def api_handle_missing():
    df = data_storage.get("df")
    if df is None:
        return jsonify({"success": False, "message": "No dataset found."})
    
    method = request.json.get("missing_method")
    fill_value = request.json.get("fill_value")
    
    try:
        if method == "fill_value":
            df = handle_missing_data(df, method=method, fill_value=fill_value)
        else:
            df = handle_missing_data(df, method=method)
        
        data_storage["df"] = df
        duplicate_count, _ = duplicate_summary(df)
        
        response_data = {
            "success": True,
            "preview": df.head().to_html(classes="table table-bordered"),
            "shape": [df.shape[0], df.shape[1]],
            "duplicate_count": duplicate_count,
            "show_duplicate_options": duplicate_count > 0,
            "columns": df.columns.tolist(),
            "message": "Missing data handled successfully!"
        }
        
        return jsonify(make_json_serializable(response_data))
    except Exception as e:
        return jsonify({"success": False, "message": f"Error handling missing data: {e}"})

@app.route("/api/remove_duplicates", methods=["POST"])
def api_remove_duplicates():
    df = data_storage.get("df")
    if df is None:
        return jsonify({"success": False, "message": "No dataset found."})
    
    try:
        df = remove_duplicates(df)
        data_storage["df"] = df
        missing_summary = missing_data_summary(df).to_html(classes="table table-striped")
        duplicate_count, _ = duplicate_summary(df)
        
        response_data = {
            "success": True,
            "preview": df.head().to_html(classes="table table-bordered"),
            "shape": [df.shape[0], df.shape[1]],
            "missing_summary": missing_summary,
            "duplicate_count": duplicate_count,
            "show_duplicate_options": duplicate_count > 0,
            "columns": df.columns.tolist(),
            "message": "Duplicate rows removed successfully!"
        }
        
        return jsonify(make_json_serializable(response_data))
    except Exception as e:
        return jsonify({"success": False, "message": f"Error removing duplicates: {e}"})

@app.route("/api/detect_outliers", methods=["POST"])
def api_detect_outliers():
    df = data_storage.get("df")
    if df is None:
        return jsonify({"success": False, "message": "No dataset found."})
    
    try:
        flags, summary = detect_outliers_iqr(df)
        # Convert numpy/pandas integers to Python integers
        summary_converted = {str(k): int(v) for k, v in summary.items()}
        outlier_summary_html = pd.DataFrame.from_dict(summary_converted, orient='index', columns=['Outlier Count']).to_html(classes="table table-striped")
        
        data_storage["outlier_flags"] = flags
        
        if sum(summary_converted.values()) == 0:
            response_data = {
                "success": True,
                "show_outlier_summary": False,
                "message": "No outliers detected in numeric columns."
            }
        else:
            response_data = {
                "success": True,
                "show_outlier_summary": True,
                "outlier_summary": outlier_summary_html,
                "message": "Outliers detected successfully!"
            }
        
        return jsonify(make_json_serializable(response_data))
    except Exception as e:
        return jsonify({"success": False, "message": f"Error detecting outliers: {e}"})

@app.route("/api/remove_outliers", methods=["POST"])
def api_remove_outliers():
    df = data_storage.get("df")
    if df is None:
        return jsonify({"success": False, "message": "No dataset found."})
    
    try:
        df_cleaned = remove_outliers_iqr(df)
        data_storage["df"] = df_cleaned
        
        missing_summary = missing_data_summary(df_cleaned).to_html(classes="table table-striped")
        duplicate_count, _ = duplicate_summary(df_cleaned)
        
        response_data = {
            "success": True,
            "preview": df_cleaned.head().to_html(classes="table table-bordered"),
            "shape": [df_cleaned.shape[0], df_cleaned.shape[1]],
            "missing_summary": missing_summary,
            "duplicate_count": duplicate_count,
            "show_missing_options": True,
            "show_duplicate_options": duplicate_count > 0,
            "columns": df_cleaned.columns.tolist(),
            "message": "Outliers removed successfully!"
        }
        
        return jsonify(make_json_serializable(response_data))
    except Exception as e:
        return jsonify({"success": False, "message": f"Error removing outliers: {e}"})

@app.route("/api/train_test_split", methods=["POST"])
def api_train_test_split():
    df = data_storage.get("df")
    if df is None:
        return jsonify({"success": False, "message": "Please upload and clean your dataset before splitting."})
    
    target_col = request.json.get("target_column")
    test_size = request.json.get("test_size", 0.2)
    stratify_option = request.json.get("stratify", "yes")
    
    if target_col not in df.columns:
        return jsonify({"success": False, "message": f"Target column '{target_col}' not found."})
    
    try:
        test_size = float(test_size)
        if not (0 < test_size < 1):
            return jsonify({"success": False, "message": "Test size must be between 0 and 1."})
    except ValueError:
        return jsonify({"success": False, "message": "Invalid test size value."})
    
    is_continuous_target = pd.api.types.is_numeric_dtype(df[target_col]) and len(df[target_col].unique()) > 10
    stratify = None if is_continuous_target else (df[target_col] if stratify_option.lower() == "yes" else None)
    
    try:
        train_df, test_df = split_train_test(df, target_col, test_size=test_size, stratify=stratify)
        data_storage["train_df"] = train_df
        data_storage["test_df"] = test_df
        
        response_data = {
            "success": True,
            "train_shape": [train_df.shape[0], train_df.shape[1]],
            "test_shape": [test_df.shape[0], test_df.shape[1]],
            "message": "Dataset split successfully!"
        }
        
        return jsonify(make_json_serializable(response_data))
    except Exception as e:
        return jsonify({"success": False, "message": f"Error during split: {str(e)}"})

# Keep the original route for backward compatibility but simplified
@app.route("/old", methods=["GET", "POST"])
def old_index():
    # This is the old implementation - keeping for reference
    return render_template("index.html", df_exists=False, columns=[], train_shape=None, test_shape=None)

# ---------------- Generate Profiling Report ----------------
@app.route("/profile_report", methods=["GET"])
def profile_report_route():
    df = data_storage.get("df")
    if df is None:
        flash("No dataset uploaded.")
        return redirect(url_for("index"))
    
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], "profile_report.html")
    generate_profile_report(df, output_path)
    return send_file(output_path, mimetype="text/html")

# ---------------- Download Cleaned Dataset ----------------
@app.route("/download", methods=["GET"])
def download_file():
    df = data_storage.get("df")
    if df is None:
        flash("No data to download.")
        return redirect(url_for("index"))

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(io.BytesIO(buffer.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="cleaned_data.csv")

# ---------------- Download Train/Test Dataset ----------------
@app.route("/download/<dataset>", methods=["GET"])
def download_dataset(dataset):
    if dataset not in ["train", "test"]:
        flash("Invalid dataset requested.")
        return redirect(url_for("index"))

    df = data_storage.get(f"{dataset}_df")
    if df is None:
        flash(f"No {dataset} dataset available to download.")
        return redirect(url_for("index"))

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(io.BytesIO(buffer.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name=f"{dataset}_dataset.csv")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
