def low_attendance_template(data):
    """Low attendance alert template"""
    attendance_color = '#ef4444' if data['percentage'] < 60 else '#f59e0b'
    
    content = f"""
        <h2 style="color: #ef4444; margin-bottom: 10px;">⚠️ Low Attendance Alert</h2>
        <p style="font-size: 16px; color: #333;">Dear <strong>{data['name']}</strong>,</p>
        
        <p style="color: #666;">We noticed that your attendance has fallen below the required threshold. Immediate action is required to avoid academic penalties.</p>
        
        <div class="alert-box alert-critical">
            <h3 style="margin: 0 0 10px 0; color: #dc3545;">⚠️ URGENT: Action Required</h3>
            <p style="margin: 0; color: #721c24;">Your attendance is critically low. Please contact the administration office immediately.</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" style="color: {attendance_color};">{data['percentage']}%</div>
                <div class="stat-label">Current Attendance</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #10b981;">75%</div>
                <div class="stat-label">Required Minimum</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{data['present']}</div>
                <div class="stat-label">Classes Attended</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{data['total']}</div>
                <div class="stat-label">Total Classes</div>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {data['percentage']}%;">{data['percentage']}%</div>
        </div>
        
        <div class="message-box">
            <h4 style="margin-top: 0; color: #667eea;">📋 What You Need to Do:</h4>
            <ul style="color: #666; line-height: 1.8;">
                <li>Attend all upcoming classes regularly</li>
                <li>Submit medical certificates for genuine absences</li>
                <li>Meet with your class teacher within 3 days</li>
                <li>Improve attendance to minimum 75% within 2 weeks</li>
            </ul>
        </div>
        
        <div style="text-align:center; margin-top: 25px;">
            <a href="#" class="btn">View Attendance Report</a>
        </div>
    """
    
    return get_base_template(content)
