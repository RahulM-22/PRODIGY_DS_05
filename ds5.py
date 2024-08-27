import pandas as pd

# Load the dataset
df = pd.read_csv('D:/MP 1 FINAL/DS 05/US_Accidents_March23.csv/US_Accidents_March23.csv')

# Display available columns
print(df.columns)

# Drop only the columns that exist in your DataFrame
columns_to_drop = ['ID', 'Description', 'Country']  # Removed 'Number' as it doesn't exist
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Display the first few rows
print(df.head())

# Check for missing values
print(df.isnull().sum())

# Clean up ".000000000" in time columns if present
df['Start_Time'] = df['Start_Time'].str.replace('.000000000', '', regex=False)
df['End_Time'] = df['End_Time'].str.replace('.000000000', '', regex=False)

# Convert time columns to datetime format, handling errors
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df['End_Time'] = pd.to_datetime(df['End_Time'], errors='coerce')

# Drop rows with missing critical data after conversion
df = df.dropna(subset=['Start_Time', 'End_Time', 'Weather_Condition', 'Visibility(mi)', 'Temperature(F)'])

# Extract features like hour, day of the week, and month
df['Hour'] = df['Start_Time'].dt.hour
df['Day_of_Week'] = df['Start_Time'].dt.day_name()
df['Month'] = df['Start_Time'].dt.month_name()

# Group weather conditions into broader categories
def categorize_weather(condition):
    if pd.isna(condition):
        return 'Other'
    if 'rain' in condition.lower():
        return 'Rain'
    elif 'snow' in condition.lower():
        return 'Snow'
    elif 'clear' in condition.lower() or 'fair' in condition.lower():
        return 'Clear'
    elif 'cloud' in condition.lower() or 'overcast' in condition.lower():
        return 'Cloudy'
    elif 'fog' in condition.lower() or 'mist' in condition.lower():
        return 'Fog/Mist'
    else:
        return 'Other'

df['Weather_Category'] = df['Weather_Condition'].apply(categorize_weather)

import seaborn as sns
import matplotlib.pyplot as plt

# Visualize accidents by hour
plt.figure(figsize=(10, 6))
sns.countplot(x='Hour', data=df, palette='viridis')
plt.title('Accidents by Hour of the Day')
plt.show()

# Visualize accidents by day of the week
plt.figure(figsize=(10, 6))
sns.countplot(x='Day_of_Week', data=df, palette='coolwarm', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title('Accidents by Day of the Week')
plt.show()

# Visualize accidents by weather condition
plt.figure(figsize=(10, 6))
sns.countplot(x='Weather_Category', data=df, palette='Set2')
plt.title('Accidents by Weather Condition')
plt.xticks(rotation=45)
plt.show()

import folium

# Create a map centered around the mean latitude and longitude
accident_map = folium.Map(location=[df['Start_Lat'].mean(), df['Start_Lng'].mean()], zoom_start=5)

# Add points to the map
for idx, row in df.iterrows():
    folium.CircleMarker([row['Start_Lat'], row['Start_Lng']],
                        radius=2,
                        color='red',
                        fill=True,
                        fill_color='red',
                        fill_opacity=0.5).add_to(accident_map)

# Save the map as an HTML file
accident_map.save('accident_hotspots.html')

# Plot a correlation heatmap between temperature, visibility, and hour
plt.figure(figsize=(10, 6))
sns.heatmap(df[['Temperature(F)', 'Visibility(mi)', 'Hour']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation between Temperature, Visibility, and Time of Day')
plt.show()
