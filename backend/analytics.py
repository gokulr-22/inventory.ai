import statistics

def generate_insights(results):
    """Advanced AI-powered insights generation with god-mode features"""
    insights = []
    
    if not results:
        return ["⚠️ Insufficient data for analysis"]
    
    # Top performers
    best = max(results, key=lambda x: x['prediction'])
    worst = min(results, key=lambda x: x['prediction'])
    
    insights.append(f"🏆 {best['product']} is your TOP PERFORMER (Predicted: ${best['prediction']})")
    
    # Growth analysis
    high_growth = [r for r in results if r['growth'] > 20]
    if high_growth:
        for product in high_growth:
            insights.append(f"📈 STRONG MOMENTUM: {product['product']} with {product['growth']}% growth!")
    
    # Risk warnings
    high_risk = [r for r in results if 'High Risk' in r.get('risk', '')]
    if high_risk:
        for product in high_risk:
            insights.append(f"⚠️ VOLATILITY ALERT: {product['product']} is unstable (Volatility: {product.get('volatility', 0)}%)")
    
    # Confidence levels
    high_conf = [r for r in results if r['confidence'] > 80]
    if high_conf:
        insights.append(f"✅ HIGH CONFIDENCE: {len(high_conf)} products have strong prediction accuracy")
    
    # Market trends
    uptrend_count = len([r for r in results if '📈' in r.get('trend', '')])
    downtrend_count = len([r for r in results if '📉' in r.get('trend', '')])
    
    if uptrend_count > downtrend_count:
        insights.append(f"📊 MARKET MOMENTUM: {uptrend_count} products trending UP vs {downtrend_count} trending DOWN")
    elif downtrend_count > uptrend_count:
        insights.append(f"📊 MARKET CAUTION: {downtrend_count} products declining, {uptrend_count} recovering")
    
    # Revenue recommendations
    total_predicted = sum([r['prediction'] for r in results])
    insights.append(f"💰 TOTAL PREDICTED REVENUE: ${total_predicted:.2f}")
    
    # Top 3 opportunities
    top_3 = results[:3]
    insights.append(f"🎯 TOP OPPORTUNITIES: {', '.join([r['product'] for r in top_3])}")
    
    # Risk portfolio balance
    low_risk = len([r for r in results if '🟢' in r.get('risk', '')])
    med_risk = len([r for r in results if '🟡' in r.get('risk', '')])
    high_risk_count = len([r for r in results if '🔴' in r.get('risk', '')])
    
    if low_risk > med_risk and low_risk > high_risk_count:
        insights.append(f"✨ PORTFOLIO STABILITY: Well-balanced inventory with {low_risk} low-risk products")
    else:
        insights.append(f"⚡ PORTFOLIO OPTIMIZATION: Consider focusing on {low_risk} stable products")
    
    # Add model explanation
    insights.append(f"🤖 Analysis powered by Ensemble AI (Linear + Random Forest models)")
    
    return insights