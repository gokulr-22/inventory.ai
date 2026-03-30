from flask import Flask, request, jsonify, send_from_directory # type: ignore
from flask_cors import CORS # type: ignore
from model import predict_all
from analytics import generate_insights # pyright: ignore[reportMissingImports]
from utils import process_file # type: ignore
from datetime import datetime
import traceback
import os

# Serve frontend files
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Track analysis history
analysis_history = []

@app.route("/", methods=["GET"])
def index():
    """Serve login page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Serve dashboard page"""
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route("/<path:filename>", methods=["GET"])
def serve_static(filename):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory(app.static_folder, filename)

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": "2.0 God Mode",
        "timestamp": datetime.now().isoformat(),
        "ai_engine": "Ensemble (Linear + Random Forest)",
        "features": ["Advanced Predictions", "Risk Assessment", "Trend Analysis", "Confidence Scoring"]
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    """Advanced analysis endpoint with god-mode features"""
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"status": "error", "message": "No file provided"}), 400
        
        # Process file
        df = process_file(file)
        
        if df is None or df.empty:
            return jsonify({"status": "error", "message": "Invalid data format"}), 400
        
        # Advanced predictions
        results = predict_all(df)
        
        if not results:
            return jsonify({"status": "error", "message": "Insufficient data for analysis"}), 400
        
        # Generate insights
        insights = generate_insights(results)
        
        # Calculate totals
        total_revenue = sum([r['prediction'] for r in results])
        total_growth = sum([r['growth'] for r in results]) / len(results)
        avg_confidence = sum([r['confidence'] for r in results]) / len(results)
        
        # Count risk levels
        high_risk = len([r for r in results if '🔴' in r.get('risk', '')])
        med_risk = len([r for r in results if '🟡' in r.get('risk', '')])
        low_risk = len([r for r in results if '🟢' in r.get('risk', '')])
        
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "insights": insights,
            "summary": {
                "total_revenue": round(total_revenue, 2),
                "avg_growth": round(total_growth, 2),
                "avg_confidence": round(avg_confidence, 1),
                "products_analyzed": len(results),
                "risk_distribution": {
                    "low": low_risk,
                    "medium": med_risk,
                    "high": high_risk
                }
            },
            "ai_metrics": {
                "model": "Ensemble AI v2.0",
                "algorithms": ["Linear Regression", "Random Forest"],
                "processing_method": "God Mode Advanced Analysis"
            }
        }
        
        # Store in history
        analysis_history.append({
            "timestamp": datetime.now().isoformat(),
            "products_count": len(results),
            "total_revenue": total_revenue
        })
        
        return jsonify(response)

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error: {error_trace}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }), 500

@app.route("/stats", methods=["GET"])
def get_stats():
    """Get analysis history and statistics"""
    return jsonify({
        "status": "success",
        "total_analyses": len(analysis_history),
        "history": analysis_history[-10:] if analysis_history else [],
        "mode": "God Mode Active"
    })

@app.route("/models", methods=["GET"])
def get_models():
    """Get available AI models"""
    return jsonify({
        "status": "success",
        "models": [
            {
                "name": "Linear Regression",
                "description": "Baseline trend forecasting",
                "accuracy": "Good for linear trends"
            },
            {
                "name": "Random Forest",
                "description": "Advanced non-linear predictions",
                "accuracy": "Better for complex patterns"
            },
            {
                "name": "Ensemble AI",
                "description": "Combined model for best accuracy",
                "accuracy": "Optimal performance"
            }
        ],
        "active_model": "Ensemble AI",
        "features": [
            "Confidence Scoring",
            "Volatility Analysis",
            "Trend Detection",
            "Risk Assessment",
            "Growth Forecasting"
        ]
    })

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)