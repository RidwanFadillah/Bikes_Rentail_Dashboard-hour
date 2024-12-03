import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('/workspaces/Bikes_Rentail_Dashboard-hour/dashboard/main_data.csv')

# Sidebar configuration
with st.sidebar:
    st.title("Bike Sharing Dashboard")
    st.image("https://i.ibb.co.com/Qdg7dNK/Free-Bike-rental-logo-template-Dibuat-dengan-Poster-My-Wall.png",use_column_width=True, width=300)
    st.caption("Data Source: Bike Sharing Dataset")


# Title of the app
st.title("Bike Sharing Data Dashboard")
st.markdown("This dashboard visualizes bike rental data with a focus on weather conditions, hourly rentals, and clustering busy hours.")

# 1. Weather condition analysis
st.subheader("Average Bike Rentals by Weather Condition")
weather_rentals = data.groupby('weathersit')['cnt'].mean().reset_index()

# Mapping weather conditions
weather_conditions = {
    1: 'Clear/Partly Cloudy', 
    2: 'Mist/Cloudy', 
    3: 'Light Snow/Rain', 
    4: 'Heavy Rain/Snow'
}
weather_rentals['weathersit'] = weather_rentals['weathersit'].map(weather_conditions)

# Plot weather rentals
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_rentals, palette='Blues_d', ax=ax)
ax.set_title('Average Bike Rentals by Weather Condition', fontsize=16)
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Average Bike Rentals')
st.pyplot(fig)

# 2. Hourly bike rentals analysis with time range filter
st.subheader("Average Bike Rentals by Hour of the Day")

# Add a slider for selecting time range
hour_range = st.slider("Select hour range:", min_value=0, max_value=23, value=(0, 23), step=1)

# Filter data based on selected hour range
filtered_data = data[(data['hr'] >= hour_range[0]) & (data['hr'] <= hour_range[1])]
hourly_rentals = filtered_data.groupby('hr')['cnt'].mean().reset_index()

# Plot hourly rentals based on selected range
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_rentals, marker='o', color='green', ax=ax)
ax.set_title(f'Average Bike Rentals from Hour {hour_range[0]} to {hour_range[1]}', fontsize=16)
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Average Bike Rentals')
plt.xticks(range(hour_range[0], hour_range[1]+1))
st.pyplot(fig)

# 3. Clustering busy vs quiet hours with time range filter
st.subheader("Clustering of Busy and Quiet Hours Based on Bike Rentals")

# Calculate median rentals for clustering
median_rentals = data['cnt'].median()

# Filter the same data based on hour range for clustering
filtered_data['time_of_day'] = filtered_data['cnt'].apply(lambda x: 'Busy Hours' if x >= median_rentals else 'Quiet Hours')

# Plot busy vs quiet hours based on selected range
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(x='hr', hue='time_of_day', data=filtered_data, palette='coolwarm', ax=ax)
ax.set_title(f'Busy vs Quiet Hours from Hour {hour_range[0]} to {hour_range[1]}', fontsize=16)
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Frequency of Rentals')
plt.xticks(range(hour_range[0], hour_range[1]+1))
st.pyplot(fig)


