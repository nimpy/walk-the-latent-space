import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set page config for better appearance
st.set_page_config(
    page_title="Macronutrient Space Visualisation",
    layout="wide",
)

# Read the CSV file
df = pd.read_csv('latent_space_data/Macronutrients.csv')

# Create the 3D scatter plot
def create_3d_scatter(df):
    # Calculate the ranges for each axis to help with scaling
    fat_range = df['Fat'].max() - df['Fat'].min()
    protein_range = df['Protein'].max() - df['Protein'].min()
    carb_range = df['Carohydrates'].max() - df['Carohydrates'].min()
    
    # Find the maximum range to scale others accordingly
    max_range = max(fat_range, protein_range, carb_range)
    
    # Calculate scaling factors
    fat_scale = max_range / fat_range if fat_range != 0 else 1
    protein_scale = max_range / protein_range if protein_range != 0 else 1
    carb_scale = max_range / carb_range if carb_range != 0 else 1
    
    fig = go.Figure(data=[
        go.Scatter3d(
            x=df['Fat'] * fat_scale,
            y=df['Protein'] * protein_scale,
            z=df['Carohydrates'] * carb_scale,
            mode='markers',
            marker=dict(
                size=10,
                color=df['Kilocalories'],
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(
                    title="Calories",
                    thickness=20
                )
            ),
            text=df['Ingredient'],
            hovertemplate=(
                "<b>%{text}</b><br>" +
                "Calories: %{marker.color:.0f} kcal<br>" +
                "Fat: %{customdata[0]:.1f}g<br>" +
                "Protein: %{customdata[1]:.1f}g<br>" +
                "Carbohydrates: %{customdata[2]:.1f}g<br>" +
                "<extra></extra>"
            ),
            customdata=df[['Fat', 'Protein', 'Carohydrates']].values
        )
    ])
    
    # Update the layout for better visualization
    fig.update_layout(
        scene=dict(
            xaxis_title='Fat',
            yaxis_title='Protein',
            zaxis_title='Carbohydrates',
            bgcolor='rgba(0,0,0,0)',
            # Make the visualization more cube-like
            aspectmode='cube',
            xaxis=dict(gridcolor='lightgray'),
            yaxis=dict(gridcolor='lightgray'),
            zaxis=dict(gridcolor='lightgray')
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        scene_camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.5, y=1.5, z=1.5)
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    
    return fig

# Add title
st.title("Macronutrient Space Visualization")

# Display the plot
st.plotly_chart(create_3d_scatter(df), use_container_width=True)

# Add calorie range filter below the plot
cal_range = st.slider(
    "Calorie Range",
    min_value=float(df['Kilocalories'].min()),
    max_value=float(df['Kilocalories'].max()),
    value=(float(df['Kilocalories'].min()), float(df['Kilocalories'].max()))
)

# Filter the data
filtered_df = df[
    (df['Kilocalories'] >= cal_range[0]) &
    (df['Kilocalories'] <= cal_range[1])
]

# Update the plot with filtered data
st.plotly_chart(create_3d_scatter(filtered_df), use_container_width=True)