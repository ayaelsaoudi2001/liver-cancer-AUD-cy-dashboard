import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_AUD_page():

    st.markdown("<h1 style='text-align: center;'>Alcohol Use Disorder Rates in Cyprus</h1><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left;'>Alcohol Use Disorder Rate in the Mediterranean Region</h3>", unsafe_allow_html=True)

    regional_alcohol_data = pd.read_csv('C:/Users/acc/Desktop/HCA project/world-share-with-alcohol-use-disorders.csv')
    regional_alcohol_data["Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized"]=regional_alcohol_data["Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized"]*1000

    # Filter data for specific entities
    entities_of_interest = ['Cyprus', 'Turkey', 'Lebanon', 'Palestine', 'Jordan']
    filtered_data = regional_alcohol_data[regional_alcohol_data['Entity'].isin(entities_of_interest)]

    # Define custom colors for specific countries
    color_map = {
        'Cyprus': 'blue',
        'Lebanon': 'red',
        'Turkey': 'green',
        'Palestine': 'orange',
        'Jordan': 'purple',
    }

    # Radio button for selecting the plot type
    plot_type = st.radio("Select Plot Type", options=["Bar Plot", "Line Plot"])

    if plot_type == "Bar Plot":
        # Slider widget for selecting the year
        selected_year = st.slider('Select a Year', min_value=1990, max_value=2019, value=2019, step=1)

        # Filter data for the selected year
        data_for_year = filtered_data[filtered_data['Year'] == selected_year]

        # Sort data in descending order based on the death rate
        data_for_year_sorted = data_for_year.sort_values(by='Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized', ascending=False)

        # Create bar graph using Plotly Express
        fig = px.bar(data_for_year_sorted,
                    x='Entity',
                    y='Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized',
                    color='Entity',
                    color_discrete_map=color_map,  # Use custom color map
                    labels={'Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized': 'Death Rate per 100,000'},
                    title=f'Alcohol Use Disorder Rate in - {selected_year}')

        # Combine legend entries for "Others"
        fig.update_traces(legendgroup="Others", selector=dict(name="Others"))

        # Update layout
        fig.update_layout(xaxis_title='Country', yaxis_title='Rate per 100,000', title_font_size=20)

        # Render the Plotly figure
        st.plotly_chart(fig)
        st.markdown('---')  # Separator line

    elif plot_type == "Line Plot":
        # Filter data for all years
        # Pivot the DataFrame
        pivot_data = filtered_data.pivot(index='Year', columns='Entity', values='Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized')

        # Reset the index
        pivot_data.reset_index(inplace=True)

        # Create line plot using Plotly Express
        fig = px.line(pivot_data, x='Year', y=pivot_data.columns[1:], 
                    labels={'value': 'Death Rate per 100,000', 'Year': 'Year'},
                    color_discrete_map=color_map,  # Use custom color map
                    title='Alcohol Use Disorder Rate Across the Years',
                    )

        # Update layout
        fig.update_layout(xaxis_title='Year', yaxis_title='Rate per 100,000', title_font_size=20, legend_title_text='Country')

        # Render the Plotly figure
        st.plotly_chart(fig)

        st.markdown('---')  # Separator line

    ################################################################################

    number_alcohol_use_disorder = pd.read_csv('C:/Users/acc/Desktop/HCA project/number-with-alcohol-use-disorders.csv')
    number_alcohol_use_disorder_copy = number_alcohol_use_disorder.copy()
    number_alcohol_use_disorder_copy["Males"] = number_alcohol_use_disorder_copy["Current number of cases of alcohol use disorders, in males aged all ages"]
    number_alcohol_use_disorder_copy["Females"] = number_alcohol_use_disorder_copy["Current number of cases of alcohol use disorders, in females aged all ages"]
    number_alcohol_use_disorder_copy = number_alcohol_use_disorder_copy[number_alcohol_use_disorder_copy['Entity'] == 'Cyprus']
    number_alcohol_use_disorder_copy['Total'] = number_alcohol_use_disorder_copy['Males'] + number_alcohol_use_disorder_copy['Females']
    number_alcohol_use_disorder_copy.reset_index(drop=True, inplace=True)
    number_alcohol_use_disorder_copy['Percentage Males'] = (number_alcohol_use_disorder_copy['Males'] / number_alcohol_use_disorder_copy['Total']) * 100
    number_alcohol_use_disorder_copy['Percentage Females'] = (number_alcohol_use_disorder_copy['Females'] / number_alcohol_use_disorder_copy['Total']) * 100

    population = pd.read_csv('C:/Users/acc/Desktop/HCA project/population-by-age-group.csv')
    population_copy = population.copy()
    population_copy['Total Population'] = population_copy.iloc[:, 3:].sum(axis=1)
    cyprus_pop = population_copy[population_copy['Entity'] == 'Cyprus']
    cyprus_pop = cyprus_pop[(cyprus_pop['Year'] >= 1990) & (cyprus_pop['Year'] <= 2019)]
    cyprus_pop.reset_index(drop=True, inplace=True)

    columns_to_remove = [
        'Population by broad age group - Sex: all - Age: 65+ - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 25-64 - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 15-24 - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 5-14 - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 0-4 - Variant: estimates'
    ]

    cyprus_pop = cyprus_pop.drop(columns=[col for col in columns_to_remove if col in cyprus_pop.columns])
    cyprus_pop["total alcohol use disorders"] = number_alcohol_use_disorder_copy['Total']
    cyprus_pop['Rate per 100,000'] = (cyprus_pop['total alcohol use disorders'] / cyprus_pop['Total Population']) * 100000

    aud_by_age = pd.read_csv('C:/Users/acc/Desktop/HCA project/prevalence-of-alcohol-use-disorders-by-age.csv')
    columns_to_convert = [
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged all ages',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 70+ years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 15-49 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 5-14 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 50-69 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged under 5'
    ]

    # Convert each column to per 100,000
    for column in columns_to_convert:
        aud_by_age[column] *= 1000
    aud_by_age.head(5)

    #################################################################################################################

    st.markdown("<h3 style='text-align: left;'>Alcohol Use Disorder Rate in Cyprus</h3>", unsafe_allow_html=True)

    # Create line plot for rate
    fig_line_rate = px.line(cyprus_pop, x='Year', y='Rate per 100,000', title='Rate of Alcohol Use Disorder Cases per 100,000 People in Cyprus')
    fig_line_rate.update_layout(xaxis_title='Year', title_font_size=20, yaxis_title='AUD Rate per 100,000')

    # Create line plot for total number of cases
    fig_line_cases = px.line(cyprus_pop, x='Year', y='total alcohol use disorders', title='Total Number of Alcohol Use Disorder Cases in Cyprus')
    fig_line_cases.update_layout(xaxis_title='Year', yaxis_title='Total Number of Cases', title_font_size=20)

    # Add a checkbox to toggle between the line plots
    show_cases = st.checkbox("Show Cases", value=False)

    # Display the selected plot
    if show_cases:
        st.plotly_chart(fig_line_cases, use_container_width=True)
    else:
        st.plotly_chart(fig_line_rate, use_container_width=True)

    st.markdown('---')  # Separator line

    st.markdown("<h3 style='text-align: left;'>Alcohol Use Disorder Rate in Cyprus Across Demographics</h3>", unsafe_allow_html=True)

    selected_figure = st.selectbox(
        "Select Graph Demographic Breakdown",
        ["Alcohol Use Disorder Rate in Cyprus By Gender", "Alcohol Use Disorder Rate in Cyprus By Age"]
    )

    if selected_figure == "Alcohol Use Disorder Rate in Cyprus By Gender":
        selected_year_grouped = st.slider('Select Year', min_value=1990, max_value=2019, value=2019, step=1)

        data_for_year_grouped = number_alcohol_use_disorder_copy[number_alcohol_use_disorder_copy['Year'] == selected_year_grouped]

        show_rate_grouped = st.checkbox("Show Rate per 100,000", value=True)

        if show_rate_grouped:
            fig_grouped = px.bar(data_for_year_grouped, x='Year', y=['Percentage Males', 'Percentage Females'],
                                title='Percentage of Males and Females with Alcohol Use Disorders Over Time',
                                labels={'Year': 'Year', 'value': 'Percentage'}, barmode='group')
        else:
            fig_grouped = px.bar(data_for_year_grouped, x='Year', y=['Males', 'Females'],
                                title='Number of Males and Females with Alcohol Use Disorders Over Time',
                                labels={'Year': 'Year', 'value': 'Number of Cases'}, barmode='group')

        # Update legend labels to "Male" and "Female"
        fig_grouped.update_traces(
            name='Male',
            selector=dict(name='Percentage Males')
        )
        fig_grouped.update_traces(
            name='Female',
            selector=dict(name='Percentage Females')
        )

        # Update layout
        fig_grouped.update_layout(xaxis_title='Year',title_font_size=20, yaxis_title='Percentage' if show_rate_grouped else 'Number of Cases', legend_title_text='Gender')

        st.plotly_chart(fig_grouped)

    elif selected_figure == "Alcohol Use Disorder Rate in Cyprus By Age":
        plot = aud_by_age[aud_by_age['Entity'] == 'Cyprus']

        # Extract the year column
        years = plot['Year']

        # Extract all the columns related to alcohol use disorders except the one to be excluded
        alcohol_use_columns = [
            'Current number of cases of alcohol use disorders per 100 people, in both sexes aged under 5',
            'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 5-14 years',
            'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 15-49 years',
            'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 50-69 years',
            'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 70+ years'
        ]

        # Create a line plot for each column
        fig = px.line(plot, x=years, y=alcohol_use_columns,
                    title='Alcohol Use Disorders per 100,000 in Cyprus',
                    labels={'value': 'Cases per 100,000 People', 'variable': 'Age Group'})

        # Customize the layout
        fig.update_layout(xaxis_title='Year',title_font_size=20, yaxis_title='Cases per 100,000')

        # Update legend labels
        legend_labels = {
            alcohol_use_columns[0]: 'Under 5',
            alcohol_use_columns[1]: '5-14',
            alcohol_use_columns[2]: '15-49',
            alcohol_use_columns[3]: '50-69',
            alcohol_use_columns[4]: '70+'
        }

        for trace in fig.data:
            trace.name = legend_labels.get(trace.name, trace.name)

        # Show the plot using Streamlit
        st.plotly_chart(fig)

