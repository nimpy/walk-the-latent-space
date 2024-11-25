import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set page config for better appearance
st.set_page_config(
    page_title="3D Space Visualization",
    layout="wide",
)

# Function to generate sample data
def generate_sample_data(n_points=50):
    # Random coordinates
    np.random.seed(42)
    x = np.random.normal(0, 2, n_points)
    y = np.random.normal(0, 2, n_points)
    z = np.random.normal(0, 2, n_points)
    
    # Sample cuisine types
    cuisines = ['Italian', 'Japanese', 'Indian', 'Mexican', 'French']
    dishes = []
    
    for i in range(n_points):
        cuisine = np.random.choice(cuisines)
        if cuisine == 'Italian':
            dishes.append(np.random.choice(['Pizza', 'Pasta', 'Risotto', 'Lasagna', 'Tiramisu']))
        elif cuisine == 'Japanese':
            dishes.append(np.random.choice(['Sushi', 'Ramen', 'Tempura', 'Udon', 'Miso Soup']))
        elif cuisine == 'Indian':
            dishes.append(np.random.choice(['Curry', 'Biryani', 'Dosa', 'Samosa', 'Naan']))
        elif cuisine == 'Mexican':
            dishes.append(np.random.choice(['Tacos', 'Enchiladas', 'Guacamole', 'Quesadilla', 'Burrito']))
        else:  # French
            dishes.append(np.random.choice(['Croissant', 'Ratatouille', 'Coq au Vin', 'Quiche', 'Crêpe']))
    
    return pd.DataFrame({
        'x': x,
        'y': y,
        'z': z,
        'label': dishes,
        'cuisine': cuisines * (n_points // len(cuisines)) + cuisines[:n_points % len(cuisines)]
    })

# Generate sample data
df = generate_sample_data()

# Create the 3D scatter plot
def create_3d_scatter(df):
    # Create a color map for cuisines
    cuisine_types = df['cuisine'].unique()
    colors = {cuisine: f'hsl({i * 360/len(cuisine_types)}, 70%, 50%)'
              for i, cuisine in enumerate(cuisine_types)}
    
    fig = go.Figure(data=[
        go.Scatter3d(
            x=df[df['cuisine'] == cuisine]['x'],
            y=df[df['cuisine'] == cuisine]['y'],
            z=df[df['cuisine'] == cuisine]['z'],
            mode='markers',
            name=cuisine,
            marker=dict(
                size=8,
                color=colors[cuisine],
                opacity=0.8
            ),
            text=df[df['cuisine'] == cuisine]['label'],
            hoverinfo='text',
            hovertemplate="Dish: %{text}<br>" +
                         "x: %{x:.2f}<br>" +
                         "y: %{y:.2f}<br>" +
                         "z: %{z:.2f}<br>" +
                         "<extra></extra>"  # This removes the secondary box
        ) for cuisine in cuisine_types
    ])
    
    # Update the layout for better visualization
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            # Make the background transparent
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
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

# Add title and description
st.title("3D Latent Space Visualization")
st.markdown("""
This visualization shows different dishes positioned in a 3D latent space. 
- Hover over points to see dish names
- Click and drag to rotate the view
- Scroll to zoom in/out
- Double click to reset the view
""")

# Create two columns for layout
col1, col2 = st.columns([3, 1])

with col1:
    # Display the plot
    st.plotly_chart(create_3d_scatter(df), use_container_width=True)

with col2:
    # Add some controls
    st.subheader("Visualization Controls")
    
    # Filter by cuisine
    selected_cuisines = st.multiselect(
        "Filter by Cuisine",
        options=sorted(df['cuisine'].unique()),
        default=sorted(df['cuisine'].unique())
    )
    
    # Point size slider
    point_size = st.slider("Point Size", min_value=4, max_value=20, value=8)
    
    # Update the plot based on filters
    if selected_cuisines:
        filtered_df = df[df['cuisine'].isin(selected_cuisines)]
        st.plotly_chart(create_3d_scatter(filtered_df), use_container_width=True)