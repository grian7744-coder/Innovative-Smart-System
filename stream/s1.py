import streamlit as st
import plotly.express as px 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_option_menu import option_menu

df=pd.read_csv("Innovative Smart System.csv")
df.info()

st.set_page_config(page_title="Innovative Smart System", page_icon="Image.jpg", layout="wide",initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

h1,h2,h3{
    color:white;
}

.stMetric{
    background:#1E293B;
    padding:15px;
    border-radius:10px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.2);
}

</style>
""",unsafe_allow_html=True)

st.title("Innovative Smart System- Electric Vehicles Cars 2011-2024")

with st.sidebar:
    opt = option_menu(
        menu_title="Main Menu",
        options=[
            "Home",
            "Dashboard",
            "Dataset",
            "Processing",
            "Visualization",
            "Insights",
            "About"
        ],
        icons=[
            "house-fill",
            "speedometer2",
            "table",
            "gear-fill",
            "bar-chart-fill",
            "lightbulb-fill",
            "info-circle-fill"
        ],
        menu_icon="menu-button-wide",
        default_index=0,
        orientation="vertical"
    )

if opt == "Home":

    st.title("🚗 Innovative Smart System")
    st.subheader("Electric Vehicles (2011–2024)")
    st.markdown("---")

    st.markdown("""
    ## Welcome

    This project analyzes Electric Vehicle (EV) data collected from **2011–2024**.

    The dashboard helps users understand EV adoption trends, compare regions,
    analyze powertrains, and explore different categories through interactive
    charts and visualizations.
    """)
    
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌍 Total Regions",
            df["region"].nunique()
        )

    with col2:
        st.metric(
            "⚡ Powertrains",
            df["powertrain"].nunique()
        )

    with col3:
        st.metric(
            "📅 Years Covered",
            f"{df['year'].min()} - {df['year'].max()}"
        )

    with col4:
        st.metric(
            "📄 Total Records",
            len(df)
        )

    st.markdown("---")

    st.subheader("📂 Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.info(f"Categories Available : {df['category'].nunique()}")

        st.info(f"Parameters Available : {df['parameter'].nunique()}")

    with c2:
        st.info(f"Modes Available : {df['mode'].nunique()}")

        st.info(f"Units Available : {df['unit'].nunique()}")

    st.markdown("---")

    st.success("✅ Use the left sidebar to navigate through the dashboard.")

elif opt == "Dashboard":

    st.title("📊 Electric Vehicles Dashboard")
    st.markdown("---")

    # ----------------------------
    # Sidebar Filters
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        region = st.selectbox(
            "🌍 Select Region",
            ["All"] + sorted(df["region"].dropna().unique().tolist())
        )

    with col2:
        category = st.selectbox(
            "📂 Select Category",
            ["All"] + sorted(df["category"].dropna().unique().tolist())
        )

    with col3:
        powertrain = st.selectbox(
            "⚡ Select Powertrain",
            ["All"] + sorted(df["powertrain"].dropna().unique().tolist())
        )

    filtered_df = df.copy()

    if region != "All":
        filtered_df = filtered_df[
            filtered_df["region"] == region
        ]

    if category != "All":
        filtered_df = filtered_df[
            filtered_df["category"] == category
        ]

    if powertrain != "All":
        filtered_df = filtered_df[
            filtered_df["powertrain"] == powertrain
        ]

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "📄 Records",
            len(filtered_df)
        )

    with c2:
        st.metric(
            "🌍 Regions",
            filtered_df["region"].nunique()
        )

    with c3:
        st.metric(
            "⚡ Powertrains",
            filtered_df["powertrain"].nunique()
        )

    with c4:
        st.metric(
            "📈 Total Value",
            f"{filtered_df['value'].sum():,.0f}"
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        fig1 = px.line(
            filtered_df,
            x="year",
            y="value",
            color="powertrain",
            title="EV Trend by Year",
            markers=True
        )

        st.plotly_chart(fig1, use_container_width=True)

    with right:

        region_chart = (
            filtered_df
            .groupby("region", as_index=False)["value"]
            .sum()
        )

        fig2 = px.bar(
            region_chart,
            x="region",
            y="value",
            color="region",
            title="Region-wise EV Value"
        )

        st.plotly_chart(fig2, use_container_width=True)


    st.markdown("---")

    left2, right2 = st.columns(2)

    with left2:

        fig3 = px.pie(
            filtered_df,
            names="powertrain",
            values="value",
            title="Powertrain Distribution",
            hole=0.45
        )

        st.plotly_chart(fig3, use_container_width=True)

    with right2:

        fig4 = px.histogram(
            filtered_df,
            x="value",
            nbins=30,
            title="Value Distribution"
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    st.subheader("📋 Filtered Dataset")

    st.dataframe(filtered_df, use_container_width=True)

elif opt == "Dataset":

    st.title("📂 Electric Vehicles Dataset (2011–2024)")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Data", "📋 Columns", "📊 Summary", "❓ Missing Values"]
    )

    with tab1:
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.write("### Dataset Shape")
        st.write(df.shape)

        st.write("### Columns")
        st.write(df.columns.tolist())

        st.write("### Data Types")
        st.dataframe(df.dtypes.astype(str))

    with tab3:
        st.dataframe(df.describe(include="all"))

    with tab4:
        st.dataframe(df.isnull().sum().rename("Missing Values"))

elif opt == "Processing":

    st.title("⚙️ Data Processing")
    st.markdown("---")

    t1, t2, t3 = st.tabs([
        "📌 Before Processing",
        "🧹 After Processing",
        "📊 Processing Summary"
    ])

    with t1:

        st.subheader("Dataset Shape")
        st.write("Rows :", df.shape[0])
        st.write("Columns :", df.shape[1])

        st.markdown("---")

        st.subheader("Missing Values")

        st.dataframe(
            pd.DataFrame({
                "Column": df.columns,
                "Missing Values": df.isnull().sum().values
            }),
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("Duplicate Records")

        st.write("Duplicate Rows :", df.duplicated().sum())

        st.markdown("---")

        st.subheader("Dataset Preview")

        st.dataframe(df.head(), use_container_width=True)

    with t2:

        clean_df = df.copy()

        # Remove duplicate rows
        clean_df.drop_duplicates(inplace=True)

        # Remove missing values
        clean_df.dropna(inplace=True)

        # Reset index
        clean_df.reset_index(drop=True, inplace=True)

        st.success("✅ Data Processing Completed Successfully")

        st.subheader("Clean Dataset Shape")

        st.write("Rows :", clean_df.shape[0])
        st.write("Columns :", clean_df.shape[1])

        st.markdown("---")

        st.subheader("Remaining Missing Values")

        st.dataframe(
            pd.DataFrame({
                "Column": clean_df.columns,
                "Missing Values": clean_df.isnull().sum().values
            }),
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("Clean Dataset Preview")

        st.dataframe(clean_df.head(), use_container_width=True)

    with t3:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Original Rows",
            df.shape[0]
        )

        col2.metric(
            "Clean Rows",
            clean_df.shape[0]
        )

        col3.metric(
            "Duplicates Removed",
            df.duplicated().sum()
        )

        col4.metric(
            "Missing Values",
            df.isnull().sum().sum()
        )

        st.markdown("---")

        st.success("""
        ✔ Duplicate records removed

        ✔ Missing values handled

        ✔ Dataset cleaned successfully

        ✔ Ready for visualization and analysis
        """)

elif opt == "Visualization":

    st.title("📈 Data Visualization")
    st.markdown("---")

    t1, t2, t3 = st.tabs([
        "📊 Streamlit Charts",
        "📈 Plotly Charts",
        "🎨 Seaborn Charts"
    ])

    with t1:

        st.subheader("1️⃣ Year-wise EV Trend")

        year_data = df.groupby("year")["value"].sum()

        st.line_chart(year_data)

        st.markdown("---")

        st.subheader("2️⃣ Region-wise EV Values")

        region_data = df.groupby("region")["value"].sum()

        st.bar_chart(region_data)

        st.markdown("---")

        st.subheader("3️⃣ Powertrain-wise EV Values")

        power_data = df.groupby("powertrain")["value"].sum()

        st.bar_chart(power_data)

        st.markdown("---")

        st.subheader("4️⃣ Category-wise EV Values")

        category_data = df.groupby("category")["value"].sum()

        st.bar_chart(category_data)

        st.markdown("---")

        st.subheader("5️⃣ Parameter-wise EV Values")

        parameter_data = df.groupby("parameter")["value"].sum()

        st.bar_chart(parameter_data)

        st.markdown("---")

        st.subheader("6️⃣ Mode-wise EV Values")

        mode_data = df.groupby("mode")["value"].sum()

        st.bar_chart(mode_data)

        st.markdown("---")

        st.subheader("7️⃣ Value Distribution")

        st.area_chart(year_data)

        st.markdown("---")

        st.subheader("8️⃣ Dataset Preview")

        st.dataframe(df.head(10), use_container_width=True)

        with t2:
            
            st.subheader("📈 Interactive Plotly Charts")

    fig1 = px.line(
        df,
        x="year",
        y="value",
        color="powertrain",
        markers=True,
        title="Electric Vehicle Trend by Year"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    region_chart = df.groupby(
        "region",
        as_index=False
    )["value"].sum()

    fig2 = px.bar(
        region_chart,
        x="region",
        y="value",
        color="region",
        text_auto=True,
        title="Region-wise EV Value"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    category_chart = df.groupby(
        "category",
        as_index=False
    )["value"].sum()

    fig3 = px.bar(
        category_chart,
        x="category",
        y="value",
        color="category",
        title="Category-wise EV Value"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    power_chart = df.groupby(
        "powertrain",
        as_index=False
    )["value"].sum()

    fig4 = px.pie(
        power_chart,
        names="powertrain",
        values="value",
        hole=0.45,
        title="Powertrain Distribution"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    fig5 = px.histogram(
        df,
        x="value",
        nbins=30,
        title="Distribution of EV Values"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    fig6 = px.scatter(
        df,
        x="year",
        y="value",
        color="powertrain",
        size="value",
        hover_name="region",
        title="Year vs EV Value"
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("---")

    fig7 = px.box(
        df,
        x="powertrain",
        y="value",
        color="powertrain",
        title="Powertrain vs EV Value"
    )

    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("---")

    fig8 = px.sunburst(
        df,
        path=["region", "category", "powertrain"],
        values="value",
        title="Region → Category → Powertrain"
    )

    st.plotly_chart(fig8, use_container_width=True)

    st.markdown("---")

    fig9 = px.treemap(
        df,
        path=["region", "category", "powertrain"],
        values="value",
        title="EV Treemap"
    )

    st.plotly_chart(fig9, use_container_width=True)

    with t3:
        
        sns.set_style("whitegrid")


    st.subheader("1️⃣ Region-wise EV Value")

    fig, ax = plt.subplots(figsize=(10,5))

    region = df.groupby("region")["value"].sum().sort_values()

    sns.barplot(
        x=region.values,
        y=region.index,
        ax=ax
    )

    plt.xlabel("Value")
    plt.ylabel("Region")

    st.pyplot(fig)

    st.subheader("2️⃣ Category-wise EV Value")

    fig, ax = plt.subplots(figsize=(8,5))

    category = df.groupby("category")["value"].sum().sort_values()

    sns.barplot(
        x=category.index,
        y=category.values,
        ax=ax
    )

    plt.xticks(rotation=30)

    st.pyplot(fig)

    st.subheader("3️⃣ Powertrain Count")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.countplot(
        data=df,
        x="powertrain",
        ax=ax
    )

    plt.xticks(rotation=30)

    st.pyplot(fig)

    st.subheader("4️⃣ Value Distribution")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.histplot(
        data=df,
        x="value",
        bins=30,
        kde=True,
        ax=ax
    )

    st.pyplot(fig)

    st.subheader("5️⃣ Value by Powertrain")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.boxplot(
        data=df,
        x="powertrain",
        y="value",
        ax=ax
    )

    plt.xticks(rotation=25)

    st.pyplot(fig)

    st.subheader("6️⃣ Year vs Value")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.scatterplot(
        data=df,
        x="year",
        y="value",
        hue="powertrain",
        ax=ax
    )

    st.pyplot(fig)

    st.subheader("7️⃣ EV Growth Trend")

    year_data = (
        df.groupby("year")["value"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,5))

    sns.lineplot(
        data=year_data,
        x="year",
        y="value",
        marker="o",
        ax=ax
    )

    st.pyplot(fig)

    st.subheader("8️⃣ Correlation Heatmap")

    numeric_df = df.select_dtypes(include="number")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="Blues",
        ax=ax
    )

    st.pyplot(fig)

elif opt == "Insights":

    st.title("📑 Project Insights")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌍 Regions", df["region"].nunique())
    c2.metric("⚡ Powertrains", df["powertrain"].nunique())
    c3.metric("📂 Categories", df["category"].nunique())
    c4.metric("📄 Total Records", len(df))

    st.markdown("---")

    st.subheader("🌍 Top Region by EV Value")

    top_region = (
        df.groupby("region")["value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(top_region, use_container_width=True)

    st.subheader("⚡ Powertrain Performance")

    power = (
        df.groupby("powertrain")["value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.dataframe(power, use_container_width=True)

    st.subheader("📂 Category Summary")

    category = (
        df.groupby("category")["value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.dataframe(category, use_container_width=True)

    st.subheader("📈 Year-wise Growth")

    growth = (
        df.groupby("year")["value"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        growth.set_index("year")
    )

    st.markdown("---")

    st.subheader("💡 Key Findings")

    st.success("""
    ✅ Electric Vehicle adoption shows significant growth over the years.

    ✅ Battery Electric Vehicles (BEVs) and Plug-in Hybrid Vehicles (PHEVs)
       dominate in many regions.

    ✅ The dataset covers multiple regions, vehicle categories,
       transport modes and powertrain technologies.

    ✅ Interactive dashboards make trend analysis faster and easier.

    ✅ Data visualization helps identify regional EV adoption patterns.
    """)

    st.markdown("---")

    st.subheader("📌 Conclusion")

    st.info("""
The dashboard provides an interactive platform to explore
Electric Vehicle data from 2011–2024.

Using Python, Pandas, Plotly and Streamlit,
users can monitor EV trends, compare regions,
analyze powertrain technologies and support
data-driven decision making.
""")

elif opt == "About":

    st.title("ℹ️ About Project")
    st.markdown("---")

    st.header("🚗 Innovative Smart System")
    st.subheader("Electric Vehicles Cars (2011–2024)")

    st.write("""
This project is an interactive data analytics dashboard developed using
Python and Streamlit to analyze Electric Vehicle (EV) data from 2011 to 2024.

The dashboard enables users to explore EV adoption trends, compare regions,
analyze different powertrains, and generate meaningful insights through
interactive charts and visualizations.
""")

    st.markdown("---")

    st.subheader("🎯 Project Objectives")

    st.markdown("""
- Analyze Electric Vehicle data
- Perform Data Cleaning & Preprocessing
- Build Interactive Dashboard
- Generate Business Insights
- Compare EV Growth Across Regions
- Analyze Powertrain Technologies
- Support Data-driven Decision Making
""")

    st.markdown("---")

    st.subheader("💻 Technologies Used")

    tech = {
        "Technology":[
            "Python",
            "Streamlit",
            "Pandas",
            "NumPy",
            "Plotly",
            "Matplotlib",
            "Seaborn"
        ],

        "Purpose":[
            "Programming Language",
            "Dashboard Development",
            "Data Manipulation",
            "Numerical Computing",
            "Interactive Charts",
            "Static Charts",
            "Statistical Visualization"
        ]
    }

    st.table(pd.DataFrame(tech))

    st.markdown("---")

    st.subheader("📂 Dataset Information")

    st.write("Rows :", df.shape[0])
    st.write("Columns :", df.shape[1])

    st.write("Dataset Columns")

    st.code(", ".join(df.columns))

    st.markdown("---")

    st.subheader("✨ Dashboard Features")

    st.markdown("""
✔ Interactive Dashboard

✔ Dataset Explorer

✔ Data Cleaning

✔ KPI Cards

✔ Streamlit Charts

✔ Plotly Charts

✔ Seaborn Charts

✔ Insights & Reports

✔ Interactive Filters

✔ Download Dataset
""")

    st.markdown("---")

    st.subheader("🚀 Future Scope")

    st.info("""
• Real-time Electric Vehicle data

• Machine Learning Prediction

• EV Sales Forecasting

• Charging Station Analysis

• AI-based Recommendation System

• Live API Integration

• Power BI Integration

• Cloud Deployment
""")

    st.markdown("---")

    st.subheader("👨‍💻 Developer")

    st.success("""
Project Name:
Innovative Smart System

Domain:
Data Science & Analytics

Technology:
Python | Streamlit | Plotly | Pandas

Academic Project:
MCA Major Project
""")

    st.markdown("---")

    st.caption("© 2026 Innovative Smart System | Electric Vehicles (2011–2024)")