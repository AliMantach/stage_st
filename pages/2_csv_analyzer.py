import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(
    page_title="CSV Analyzer",
    page_icon="",
    layout="wide"
)

st.title("CSV Data Analyzer")
st.markdown("Upload your CSV file to analyze and visualize the data")
st.markdown("Search for covid stats")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display basic info
        st.subheader("Dataset Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"Rows: {df.shape[0]}")
        with col2:
            st.info(f"Columns: {df.shape[1]}")
        with col3:
            st.info(f"Missing Values: {df.isna().sum().sum()}")
        
        # Show data sample
        with st.expander("View Data Sample"):
            st.dataframe(df.head(10))
        
        # Show column information
        with st.expander("Column Information"):
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values,
                'Non-Null Count': df.count().values,
                'Null Count': df.isna().sum().values
            })
            st.dataframe(col_info)
        
        # Visualizations
        st.subheader("Data Visualization")
        
        # Identify numeric and categorical columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        
        # Select visualization type
        viz_type = st.selectbox(
            "Select visualization type",
            ["Histogram", "Scatter Plot", "Bar Chart", "Box Plot", "Correlation Heatmap"],
            index=0
        )
        
        if viz_type == "Histogram" and numeric_cols:
            col = st.selectbox("Select column for histogram", numeric_cols)
            fig = px.histogram(df, x=col, title=f"Histogram of {col}")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Select X-axis", numeric_cols, key="x_col")
            with col2:
                y_col = st.selectbox("Select Y-axis", numeric_cols, key="y_col")
            
            color_col = None
            if categorical_cols:
                use_color = st.checkbox("Color by category")
                if use_color:
                    color_col = st.selectbox("Select color column", categorical_cols)
            
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, 
                           title=f"{y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Bar Chart":
            if categorical_cols:
                x_col = st.selectbox("Select category column", categorical_cols)
                if numeric_cols:
                    y_col = st.selectbox("Select value column", numeric_cols)
                    agg_func = st.selectbox("Select aggregation", ["sum", "mean", "count", "min", "max"])
                    
                    # Aggregate data
                    agg_df = df.groupby(x_col)[y_col].agg(agg_func).reset_index()
                    fig = px.bar(agg_df, x=x_col, y=y_col, 
                               title=f"{agg_func.capitalize()} of {y_col} by {x_col}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Just count values if no numeric columns
                    counts = df[x_col].value_counts().reset_index()
                    counts.columns = [x_col, 'count']
                    fig = px.bar(counts, x=x_col, y='count', title=f"Count of {x_col}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Bar chart requires categorical columns. None found in your data.")
                
        elif viz_type == "Box Plot" and numeric_cols:
            y_col = st.selectbox("Select numeric column", numeric_cols)
            
            group_by = None
            if categorical_cols:
                use_groups = st.checkbox("Group by category")
                if use_groups:
                    group_by = st.selectbox("Select grouping column", categorical_cols)
            
            fig = px.box(df, y=y_col, x=group_by, title=f"Distribution of {y_col}")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Correlation Heatmap" and len(numeric_cols) > 1:
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            # Create heatmap
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale="RdBu_r",
                title="Correlation Matrix"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # Data filtering
        st.subheader("Data Filtering")
        
        # Select columns to display
        selected_cols = st.multiselect(
            "Select columns to display",
            df.columns.tolist(),
            default=df.columns.tolist()[:5]  # Default to first 5 columns
        )
        
        # Filter data
        filtered_df = df[selected_cols] if selected_cols else df
        
        # Add numeric filter
        if numeric_cols:
            add_numeric_filter = st.checkbox("Add numeric filter")
            if add_numeric_filter:
                filter_col = st.selectbox("Select column to filter", numeric_cols)
                
                min_val = float(df[filter_col].min())
                max_val = float(df[filter_col].max())
                
                filter_range = st.slider(
                    f"Filter range for {filter_col}",
                    min_val, max_val, (min_val, max_val)
                )
                
                filtered_df = filtered_df[
                    (df[filter_col] >= filter_range[0]) & 
                    (df[filter_col] <= filter_range[1])
                ]
        
        # Add categorical filter
        if categorical_cols:
            add_cat_filter = st.checkbox("Add categorical filter")
            if add_cat_filter:
                cat_filter_col = st.selectbox("Select category to filter", categorical_cols)
                
                categories = df[cat_filter_col].unique().tolist()
                selected_cats = st.multiselect(
                    f"Select values for {cat_filter_col}",
                    categories,
                    default=categories
                )
                
                if selected_cats:
                    filtered_df = filtered_df[df[cat_filter_col].isin(selected_cats)]
        
        # Display filtered data
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)
        
        # Download filtered data
        buffer = io.StringIO()
        filtered_df.to_csv(buffer, index=False)
        
        st.download_button(
            label="Download filtered data as CSV",
            data=buffer.getvalue(),
            file_name="filtered_data.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Error analyzing the CSV file: {e}")
