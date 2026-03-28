const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

// Enhanced drop zone
dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.style.background = "rgba(56,189,248,0.3)";
    dropZone.style.borderColor = "rgba(56,189,248,0.8)";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.background = "rgba(56,189,248,0.02)";
    dropZone.style.borderColor = "var(--border-color)";
});

dropZone.addEventListener("drop", e => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    dropZone.style.background = "rgba(56,189,248,0.02)";
    dropZone.style.borderColor = "var(--border-color)";
});

// God mode - Enhanced upload with validation
async function upload() {
    const file = fileInput.files[0];
    if (!file) return showToast("Please upload a CSV file", "error");

    if (!file.name.endsWith('.csv')) {
        return showToast("Only CSV files are supported", "error");
    }

    // Show results section with loading
    document.getElementById("resultsSection").classList.remove("hidden");
    document.getElementById("loader").classList.remove("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        document.getElementById("loader").classList.add("hidden");

        if (data.status === "success") {
            showToast("🤖 AI Analysis Complete!", "success");
            displayResults(data);
        } else {
            showToast("Analysis failed: " + data.message, "error");
        }
    } catch (error) {
        document.getElementById("loader").classList.add("hidden");
        showToast("Backend connection error. Make sure Flask is running on http://127.0.0.1:5000", "error");
        console.error("Error:", error);
    }
}

// Display god-mode results
function displayResults(data) {
    // Update KPI Cards with rich data
    const totalCard = document.getElementById("totalCard");
    totalCard.innerHTML = `
        <div class="kpi-icon">💰</div>
        <div class="kpi-content">
            <span>Total Revenue</span>
            <div class="kpi-value">$${data.summary.total_revenue.toLocaleString()}</div>
            <div class="kpi-meta">Avg Growth: ${data.summary.avg_growth}%</div>
        </div>
    `;

    const bestCard = document.getElementById("bestCard");
    const bestProduct = data.results[0];
    bestCard.innerHTML = `
        <div class="kpi-icon">🏆</div>
        <div class="kpi-content">
            <span>Top Product</span>
            <div class="kpi-value">${bestProduct.product}</div>
            <div class="kpi-meta">Confidence: ${bestProduct.confidence}%</div>
        </div>
    `;

    // Draw advanced chart
    drawAdvancedChart(data.results);

    // Show table with god-mode metrics
    displayMetricsTable(data.results);

    // Generate AI insights
    typeInsights(data.insights);

    // Display summary metrics
    displaySummaryMetrics(data.summary);
}

// Display metrics table with god-mode features
function displayMetricsTable(results) {
    const container = document.getElementById("insights");
    
    // Create table section
    const tableSection = document.createElement("div");
    tableSection.className = "metrics-table-section";
    tableSection.innerHTML = `
        <h3>📊 Detailed Metrics (God Mode)</h3>
        <div class="metrics-table-wrapper">
            <table class="metrics-table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Prediction</th>
                        <th>Growth</th>
                        <th>Confidence</th>
                        <th>Risk</th>
                        <th>Trend</th>
                    </tr>
                </thead>
                <tbody>
                    ${results.map(r => `
                        <tr>
                            <td><strong>${r.product}</strong></td>
                            <td>$${r.prediction.toLocaleString()}</td>
                            <td><span class="growth-badge ${r.growth > 0 ? 'positive' : 'negative'}">${r.growth > 0 ? '+' : ''}${r.growth}%</span></td>
                            <td><span class="confidence-badge">${r.confidence}%</span></td>
                            <td>${r.risk}</td>
                            <td>${r.trend}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    container.appendChild(tableSection);
}

// Display summary metrics
function displaySummaryMetrics(summary) {
    const container = document.getElementById("insights");
    
    const metricsSection = document.createElement("div");
    metricsSection.className = "summary-metrics";
    metricsSection.innerHTML = `
        <h3>🎯 Portfolio Summary</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Products</div>
                <div class="metric-value">${summary.products_analyzed}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Avg Confidence</div>
                <div class="metric-value">${summary.avg_confidence}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Low Risk</div>
                <div class="metric-value" style="color: #10b981;">${summary.risk_distribution.low}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Medium Risk</div>
                <div class="metric-value" style="color: #f59e0b;">${summary.risk_distribution.medium}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">High Risk</div>
                <div class="metric-value" style="color: #ef4444;">${summary.risk_distribution.high}</div>
            </div>
        </div>
    `;
    
    container.appendChild(metricsSection);
}

// Advanced chart with predictions
function drawAdvancedChart(results) {
    const ctx = document.getElementById("chart");
    
    if (window.chartInstance) {
        window.chartInstance.destroy();
    }

    const products = results.map(r => r.product);
    const predictions = results.map(r => r.prediction);
    const growth = results.map(r => r.growth);

    window.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: products,
            datasets: [
                {
                    label: 'Predicted Revenue',
                    data: predictions,
                    backgroundColor: 'rgba(56, 189, 248, 0.8)',
                    borderColor: 'rgba(56, 189, 248, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Growth %',
                    data: growth,
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Revenue ($)' },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'Growth (%)' },
                    grid: { drawOnChartArea: false }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#cbd5f5', font: { size: 12 } }
                }
            }
        }
    });
}

// Type insights with animation
function typeInsights(insights) {
    const container = document.getElementById("insights");
    
    // Add header if not already there
    if (!container.querySelector('h2')) {
        const header = document.createElement("h2");
        header.style.marginTop = "20px";
        header.style.marginBottom = "16px";
        header.innerHTML = "🤖 AI Insights";
        container.insertBefore(header, container.firstChild);
    }

    let i = 0;
    function showNext() {
        if (i < insights.length) {
            const p = document.createElement("p");
            p.className = "insight-item";
            p.innerText = insights[i];
            container.appendChild(p);
            i++;
            setTimeout(showNext, 400);
        }
    }
    showNext();
}

// Toast notification
function showToast(message, type = 'info') {
    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'info': 'fa-info-circle'
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type]}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}