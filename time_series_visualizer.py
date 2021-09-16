import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df.set_index('date')


# Clean data
df = df[((df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975)))]

    
def draw_line_plot():
    # Draw line plot
   
    fig=df.plot(x='date',y='value',kind='line',figsize=(10,4),linewidth=1,color='red')
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    #[PS] I did refer some code from net to tidy up my bar plot as I was finding it difficult to get the right parameters
    df_groupby=df.copy()

    # Copy and modify data for monthly bar plot
    df_groupby["year"] = pd.DatetimeIndex(df['date']).year
    df_groupby["month"] = pd.DatetimeIndex(df['date']).month
    df_groupby=df_groupby.groupby(['year','month'])['value'].mean()
    df_groupby=df_groupby.unstack()
   
    
    # Draw bar plot
    fig = df_groupby.plot(kind ="bar", legend = True, figsize = (10,5))
    plt.xlabel("Years", fontsize= 10)
    plt.ylabel("Average Page Views", fontsize= 10)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.legend(fontsize = 10, title="Months", labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    # Save image and return fig (don't change this part)
    fig.figure.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    #[PS] I did add some extra code to get the month name as the original code was giving me month as numbers.
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'])
   
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.month for d in df_box.date]
    df_box['month_name'] = [d.strftime('%b') for d in df_box.date]
    df_box = df_box.sort_values("month")
   

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.set_figwidth(20)
    fig.set_figheight(10)

    ax1 = sns.boxplot(x=df_box["year"], y=df_box["value"], ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)") 
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    ax2 = sns.boxplot(x=df_box["month_name"], y=df_box["value"], ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
