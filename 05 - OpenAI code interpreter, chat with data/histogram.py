import pandas as pd
import matplotlib.pyplot as plt
import kagglehub

# Download the dataset and get the path
path = kagglehub.dataset_download("notkrishna/top-1000-kaggle-datasets")

# Load the dataset into a Pandas DataFrame
df = pd.read_csv(f"{path}/kaggle_-1000.csv")

# Sort the dataset by upvotes in descending order and select the top 5
top_5_datasets = df.sort_values(by='upvotes', ascending=False).head(5)

# Extract titles and upvotes for plotting
titles = top_5_datasets['title']
upvotes = top_5_datasets['upvotes']

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(titles, upvotes, color='skyblue')
plt.xlabel('Dataset Title')
plt.ylabel('Upvotes')
plt.title('Top 5 Upvoted Datasets')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Show the plot
plt.show()
