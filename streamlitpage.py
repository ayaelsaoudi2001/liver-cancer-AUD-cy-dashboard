import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_liver_cancer_page():

    # Load liver cancer data
    liver_cancer_across_countries = pd.read_csv('C:/Users/acc/Desktop/HCA project/regional liver cancer death rate per 100,000.csv')

    st.markdown("<h1 style='text-align: center;'>Liver Cancer Rates in Cyprus</h1><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left;'>Liver Cancer Death Rate in the Mediterranean Region</h3>", unsafe_allow_html=True)

    # Define custom colors for specific countries
    color_map = {
        'Cyprus': 'blue',
        'Lebanon': 'red',
        'Turkey': 'green',
        'Palestine': 'orange',
        'Jordan': 'purple',
        # Add more countries and colors as needed
    }

    # Radio button for selecting the plot type
    plot_type = st.radio("Select Plot Type", options=["Bar Plot", "Line Plot"])

    if plot_type == "Bar Plot":
        # Slider widget for selecting the year
        selected_year = st.slider('Select a Year', min_value=1990, max_value=2019, value=2019, step=1)

        # Filter data for the selected year
        data_for_year = liver_cancer_across_countries[liver_cancer_across_countries['Year'] == selected_year]

        # Sort data in descending order based on the death rate
        data_for_year_sorted = data_for_year.sort_values(by='Value', ascending=False)

        # Create bar graph using Plotly Express
        fig = px.bar(data_for_year_sorted,
                    x='Location',
                    y='Value',
                    color='Location',
                    color_discrete_map=color_map,  # Use custom color map
                    labels={'Value': 'Death Rate per 100,000'},
                    title=f'Liver Cancer Death Rate in - {selected_year}')

        # Combine legend entries for "Others"
        fig.update_traces(legendgroup="Others", selector=dict(name="Others"))

        # Update layout
        fig.update_layout(xaxis_title='Country', yaxis_title='Death Rate per 100,000',title_font_size=20)

        # Render the Plotly figure
        st.plotly_chart(fig)
        st.markdown('---')  # Separator line

    elif plot_type == "Line Plot":
        # Create line plot using Plotly Express
        fig = px.line(title='Liver Cancer Death Rate Across the Years')

        # Iterate over each unique location
        for location in liver_cancer_across_countries['Location'].unique():
            # Filter data for the current location
            location_data = liver_cancer_across_countries[liver_cancer_across_countries['Location'] == location]

            # Add a line trace for the current location
            fig.add_trace(go.Scatter(
                x=location_data['Year'],
                y=location_data['Value'],
                mode='lines',
                name=location,  # Set the legend label to the location name
                line=dict(color=color_map.get(location))  # Use custom color from the color map
            ))

        # Update layout
        fig.update_layout(xaxis_title='Year', yaxis_title='Death Rate per 100,000', title_font_size=20, legend_title_text='Country')

        # Render the Plotly figure
        st.plotly_chart(fig)

        st.markdown('---')  # Separator line

    ####################################################################
    # Load liver cancer death rate data
    liver_cancer_death_rate = pd.read_csv('C:/Users/acc/Desktop/HCA project/liver cancer death rate per 100,000.csv')

    # Define a function to create the gender graph
    def create_gender_graph(selected_age):
        # Filter the data for Cyprus and the selected age group
        data_cyprus_selected_age = liver_cancer_death_rate[(liver_cancer_death_rate['Location'] == 'Cyprus') & 
                                                            (liver_cancer_death_rate['Age'] == selected_age)]

        # Filter the data for females
        data_females = data_cyprus_selected_age[data_cyprus_selected_age['Sex'] == 'Female']

        # Filter the data for males
        data_males = data_cyprus_selected_age[data_cyprus_selected_age['Sex'] == 'Male']

        # Filter the data for both genders
        data_both = data_cyprus_selected_age[data_cyprus_selected_age['Sex'] == 'Both']

        # Create line plots for each sex
        fig = go.Figure()

        # Add line for males
        fig.add_trace(go.Scatter(x=data_males['Year'], y=data_males['Value'], mode='lines', 
                                name='Males', line=dict(color='orange')))

        # Add line for females
        fig.add_trace(go.Scatter(x=data_females['Year'], y=data_females['Value'], mode='lines', 
                                name='Females', line=dict(color='green')))

        # Add line for both genders
        fig.add_trace(go.Scatter(x=data_both['Year'], y=data_both['Value'], mode='lines', 
                                name='Both', line=dict(color='blue')))

        # Update layout
        fig.update_layout(title='Liver Cancer Death Rate in Cyprus Across Genders',
                        xaxis_title='Year',
                        yaxis_title='Death Rate per 100,000',title_font_size=20)

        # Render the Plotly figure
        st.plotly_chart(fig)

    # Define a function to create the age graph
    def create_age_graph(selected_gender):
        # Filter the data for Cyprus and all ages
        data_cyprus_all_ages = liver_cancer_death_rate[(liver_cancer_death_rate['Location'] == 'Cyprus') & 
                                                    (liver_cancer_death_rate['Age'] != 'All ages')]

        # Filter the data for the selected gender
        data_selected_gender = data_cyprus_all_ages[data_cyprus_all_ages['Sex'] == selected_gender]

        # Create line plots for each age group
        fig = px.line(title=f'Liver Cancer Death Rate in Cyprus Across Ages for {selected_gender}',
                    labels={'Year': 'Year', 'Value': 'Value'})

        # Add lines for each age group
        for age_group in data_selected_gender['Age'].unique():
            data_age_group = data_selected_gender[data_selected_gender['Age'] == age_group]
            fig.add_scatter(x=data_age_group['Year'], y=data_age_group['Value'], mode='lines', name=age_group)

        # Update legend order
        fig.update_layout(legend=dict(traceorder='reversed'),yaxis_title='Death Rate per 100,000',title_font_size=20)

        # Render the Plotly figure 
        st.plotly_chart(fig)

    # Streamlit app
    st.markdown("<h3 style='text-align: left;'>Trends in Liver Cancer Death Rates Across Demographics</h3>", unsafe_allow_html=True)

    # Radio button for selecting the graph type
    graph_type = st.radio("Select Graph Demographic Breakdown (Death Rate)", options=["Gender", "Age"])

    # Render the selected graph
    if graph_type == "Gender":
        # Drop-down menu for selecting age group
        selected_age = st.selectbox("Select Age Group (Death Rate)", liver_cancer_death_rate['Age'].unique())
        create_gender_graph(selected_age)
        st.markdown('---')  # Separator line
    elif graph_type == "Age":
        # Drop-down menu for selecting gender
        selected_gender = st.selectbox("Select Gender (Death Rate)", liver_cancer_death_rate['Sex'].unique())
        create_age_graph(selected_gender)
        st.markdown('---')  # Separator line

    ###########################################################################3
    # Load liver cancer DALY rate data
    liver_cancer_daly_rate = pd.read_csv('C:/Users/acc/Desktop/HCA project/liver cancer daly rates per 100,000.csv')

    # Define a function to create the gender graph
    def create_gender_graph(selected_age):
        # Filter the data for Cyprus and the selected age group
        data_cyprus_selected_age = liver_cancer_daly_rate[(liver_cancer_daly_rate['Location'] == 'Cyprus') & 
                                                            (liver_cancer_daly_rate['Age'] == selected_age)]

        # Filter the data for females
        data_females = data_cyprus_selected_age[data_cyprus_selected_age['Sex'] == 'Female']

        # Filter the data for males
        data_males = data_cyprus_selected_age[data_cyprus_selected_age['Sex'] == 'Male']

        # Filter the data for both genders
        data_both = data_cyprus_selected_age[data_cyprus_selected_age['Sex'] == 'Both']

        # Create line plots for each sex
        fig = go.Figure()

        # Add line for males
        fig.add_trace(go.Scatter(x=data_males['Year'], y=data_males['Value'], mode='lines', 
                                name='Males', line=dict(color='orange')))

        # Add line for females
        fig.add_trace(go.Scatter(x=data_females['Year'], y=data_females['Value'], mode='lines', 
                                name='Females', line=dict(color='green')))

        # Add line for both genders
        fig.add_trace(go.Scatter(x=data_both['Year'], y=data_both['Value'], mode='lines', 
                                name='Both', line=dict(color='blue')))

        # Update layout
        fig.update_layout(title='Liver Cancer DALY Rate in Cyprus Across Genders',
                        xaxis_title='Year',
                        yaxis_title='DALY Rate per 100,000',title_font_size=20)

        # Render the Plotly figure
        st.plotly_chart(fig)

    # Define a function to create the age graph
    def create_age_graph(selected_gender):
        # Filter the data for Cyprus and all ages
        data_cyprus_all_ages = liver_cancer_daly_rate[(liver_cancer_daly_rate['Location'] == 'Cyprus') & 
                                                    (liver_cancer_daly_rate['Age'] != 'All ages')]

        # Filter the data for the selected gender
        data_selected_gender = data_cyprus_all_ages[data_cyprus_all_ages['Sex'] == selected_gender]

        # Create line plots for each age group
        fig = px.line(title=f'Liver Cancer DALY Rate in Cyprus Across Ages for {selected_gender}',
                    labels={'Year': 'Year', 'Value': 'Value'})

        # Add lines for each age group
        for age_group in data_selected_gender['Age'].unique():
            data_age_group = data_selected_gender[data_selected_gender['Age'] == age_group]
            fig.add_scatter(x=data_age_group['Year'], y=data_age_group['Value'], mode='lines', name=age_group)

        # Update legend order
        fig.update_layout(legend=dict(traceorder='reversed'),yaxis_title='DALY Rate per 100,000',title_font_size=20)

        # Render the Plotly figure 
        st.plotly_chart(fig)

    # Streamlit app
    st.markdown("<h3 style='text-align: left;'>Trends in Liver Cancer DALY Rates Across Demographics</h3>", unsafe_allow_html=True)

    # Radio button for selecting the graph type
    graph_type = st.radio("Select Graph Demographic Breakdown (DALY Rate)", options=["Gender", "Age"])

    # Render the selected graph
    if graph_type == "Gender":
        # Drop-down menu for selecting age group
        selected_age = st.selectbox("Select Age Group (DALY Rate)", liver_cancer_daly_rate['Age'].unique())
        create_gender_graph(selected_age)
        st.markdown('---')  # Separator line
    elif graph_type == "Age":
        # Drop-down menu for selecting gender
        selected_gender = st.selectbox("Select Gender (DALY Rate)", liver_cancer_daly_rate['Sex'].unique())
        create_age_graph(selected_gender)
        st.markdown('---')  # Separator line