import pandas as pd
import plotly.express as px


def chart_processing(data_modeled):

    df = data_modeled.groupby(by=['Cluster']).mean()

    # I select a subset of relevant variables for which I want to compute the averages

    subset = ["Financial institution account (% age 15+)",
    "Store money using a financial institution (% age 15+)",
    "Saved at a financial institution (% age 15+)",
    "Saved at a financial institution or using a mobile money account (% age 15+)",
    "Borrowed any money from a formal financial institution or using a mobile money account (% age 15+)",
    "Made a digital payment (% age 15+)",
    "Made a utility payment: using a mobile phone (% who paid utility bills, age 15+)",
    "Account, female (% age 15+)",
    "Financial institution account, female (% age 15+)",
    "Used a mobile phone or the internet to buy something online, female (% age 15+)",
    "Used a mobile phone or the internet to buy something online, male (% age 15+)"]

    # I filter the df for the columns I am interested in
    df = df[[x for x in list(df.columns) if x in subset]]

    # I can now reset the index (creating the column 'Cluster')
    df.reset_index(inplace=True)

    # And I transform it into a string
    df['Cluster'] = df['Cluster'].astype(str)

    # I drop a cluster if it has null values
    null_indices = df[df.isnull().any(axis=1)].index
    if len(null_indices) > 0:
        index_to_drop = null_indices[0]
        df = df.drop(index_to_drop)

    # And round its values
    df = df.round(1)


    return df


def chart(chart_data, column: int):

    fig = px.bar(chart_data, x='Cluster', y= chart_data.columns[column], title= f'Share of population with {chart_data.columns[column]}')
    fig.update_layout(template='plotly_white',
                    xaxis_title='Cluster',
                    yaxis_title='%')
    fig.update_traces(marker=dict(color='#FFDE59',
                                line=dict(width=1, color='#1C3F60')),
                                    width=0.9,
                                    text=chart_data[chart_data.columns[column]],  # Display values as text
                                    textposition='auto',
                                    textfont=dict(color='#1C3F60')# Position the text automatically
    )

    fig.update_layout(
        paper_bgcolor='#FFFFFE',
        plot_bgcolor='#FFFFFE',
        xaxis_title="Cluster",
        yaxis_title="Share of population (%)",
        font=dict(
            family="Sans",
            size=28,
            color="#1C3F60"
        ),
        xaxis=dict(
            gridcolor='#DFDFAC',  # Change x-axis grid line colo
            title_font=dict(  # Custom font for the x-axis title
                family="Sans",
                size=28,
                color="#1C3F60"
            )
        ),
        yaxis=dict(
            gridcolor='#F1F1CD',  # Change y-axis grid line color
            title_font=dict(  # Custom font for the y-axis title
                family="Sans",
                size=28,
                color="#1C3F60"),
            range=[0, 100]),

        width=800,  # Width of the figure
        height=600,
        title={
            'text': f'Share of population with {chart_data.columns[column]}',
            'font': {
                'size': 28,  # Reduce the font size
            },
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    fig.show()
