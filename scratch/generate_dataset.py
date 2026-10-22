import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
n_records = 100000

# Define features
violation_types = ['NO_HELMET', 'NO_VEST', 'NO_HELMET_AND_VEST']
zone_types = ['GROUND_LEVEL', 'SCAFFOLDING', 'CRANE_AREA', 'EXCAVATION_SITE', 'ROOFTOP']
weather_conditions = ['CLEAR', 'RAIN', 'HIGH_WIND', 'FOG']

# Generate random data
data = {
    'incident_id': [f"INC_{i:06d}" for i in range(1, n_records + 1)],
    'violation_type': np.random.choice(violation_types, n_records, p=[0.4, 0.4, 0.2]),
    'zone_type': np.random.choice(zone_types, n_records),
    'weather': np.random.choice(weather_conditions, n_records, p=[0.6, 0.2, 0.1, 0.1]),
    'workers_involved': np.random.randint(1, 10, n_records),
    'height_meters': np.random.uniform(0, 50, n_records).round(1),
    'duration_minutes': np.random.randint(1, 120, n_records)
}

df = pd.DataFrame(data)

# Calculate Base Severity Score based on logical rules
def calculate_severity(row):
    score = 20  # base score
    
    # Violation Type weight
    if row['violation_type'] == 'NO_HELMET': score += 25
    elif row['violation_type'] == 'NO_VEST': score += 15
    elif row['violation_type'] == 'NO_HELMET_AND_VEST': score += 40
        
    # Zone weight
    if row['zone_type'] in ['SCAFFOLDING', 'ROOFTOP', 'CRANE_AREA']:
        score += 15
        
    # Height weight (exponential danger)
    if row['height_meters'] > 20: score += 20
    elif row['height_meters'] > 5: score += 10
        
    # Weather weight
    if row['weather'] in ['RAIN', 'HIGH_WIND']:
        score += 10
        
    # Number of workers (scale factor)
    score += (row['workers_involved'] * 1.5)
    
    # Duration factor
    if row['duration_minutes'] > 60: score += 5
    
    # Add some random noise for realism in ML training
    score += np.random.normal(0, 5)
    
    # Cap at 100
    return min(100, max(0, score))

print("Calculating severity scores (this may take a few seconds)...")
df['target_severity_score'] = df.apply(calculate_severity, axis=1).round(1)

# Generate Labels based on score
def assign_label(score):
    if score < 40: return 'LOW'
    elif score < 65: return 'MEDIUM'
    elif score < 85: return 'HIGH'
    else: return 'CRITICAL'

df['severity_label'] = df['target_severity_score'].apply(assign_label)

# Save to CSV
output_path = 'construction_risk_dataset_100k.csv'
df.to_csv(output_path, index=False)
print(f"Successfully generated {n_records} records and saved to {output_path}!")
