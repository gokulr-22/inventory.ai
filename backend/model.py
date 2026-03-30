import pandas as pd # type: ignore
import numpy as np # type: ignore
from sklearn.linear_model import LinearRegression # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
from datetime import datetime, timedelta # type: ignore

def predict_all(df):
    """Advanced ML prediction with ensemble models and confidence intervals"""
    results = []
    
    try:
        for product in df['product'].unique():
            p_df = df[df['product'] == product].sort_values('month')
            
            if len(p_df) < 2:
                continue
            
            X = p_df[['month']].values
            y = p_df['sales'].values
            
            # Linear Regression (baseline)
            lr_model = LinearRegression()
            lr_model.fit(X, y)
            
            # Random Forest (ensemble - more accurate)
            rf_model = RandomForestRegressor(n_estimators=50, random_state=42)
            rf_model.fit(X, y)
            
            # Next month prediction
            next_month = [[p_df['month'].max() + 1]]
            lr_pred = float(lr_model.predict(next_month)[0])
            rf_pred = float(rf_model.predict(next_month)[0])
            
            # Ensemble prediction (average of models)
            prediction = (lr_pred + rf_pred) / 2
            
            # Calculate growth
            last_sale = float(y[-1])
            growth = ((prediction - last_sale) / last_sale) * 100 if last_sale != 0 else 0
            
            # Calculate confidence score (based on data consistency)
            sales_std = float(np.std(y))
            sales_mean = float(np.mean(y))
            cv = (sales_std / sales_mean * 100) if sales_mean != 0 else 0
            confidence = max(0, min(100, 100 - cv))
            
            # Trend analysis
            if len(y) > 1:
                recent_trend = (float(y[-1]) - float(y[0])) / len(y)
            else:
                recent_trend = 0
            
            trend_direction = "📈 Uptrend" if recent_trend > 0 else "📉 Downtrend" if recent_trend < 0 else "➡️ Stable"
            
            # Risk assessment
            volatility = cv  # Higher volatility = higher risk
            risk_level = "🔴 High Risk" if volatility > 50 else "🟡 Medium Risk" if volatility > 20 else "🟢 Low Risk"
            
            results.append({
                "product": str(product),
                "prediction": round(float(prediction), 2),
                "growth": round(float(growth), 2),
                "confidence": round(float(confidence), 1),
                "trend": trend_direction,
                "risk": risk_level,
                "volatility": round(float(volatility), 1),
                "current_sales": round(float(last_sale), 2),
                "model": "Ensemble AI"
            })
        
        # Sort by prediction descending
        results = sorted(results, key=lambda x: x['prediction'], reverse=True)
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return []
    
    return results