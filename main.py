import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv("D:/Downloads/archive/Customer_Behaviour_Survey_responses.csv")
# print(data.columns)
data = data.drop_duplicates()
cols = ['Age', 'Gender', 'Current State or Union Territory', 'City', 'City Tier', 'Marital Status', 'Occupation',
        'branded', 'Frequently Purchased', 'Browsing time', 'Monthly Rate', 'Avg spent', 'Electronic Preference',
        'Fashion Preference', 'Clothing Preference', 'Preferred OTT', 'Book Preference', 'Date', 'Time']
data.City = data['City'].astype(str)
# Convert timestamp to date time and separate date from time
data.Timestamp = pd.to_datetime(data['Timestamp'], format="%m/%d/%Y %H:%M", errors='coerce')
data['Date'] = data.Timestamp.dt.date
data['Time'] = data.Timestamp.dt.time
data = data.drop('Timestamp', axis=1)
# Clean the 'Age' column

data = data.rename(columns={'Age ': 'age', 'Which Tier does your city belong to?': 'city_tier',
                            'What is your financial status?': 'occupation',
                            'will you purchase other brands if available': 'branded',
                            'What is the Product Category that you shop very frequently?': 'frequently_purchased',
                            'On a scale of 1 to 5 , how often do you shop in the selected product category monthly? ':
                                'monthly_rate',
                            'What is the average money that you spend while shopping the above items in one time?':
                                'avg_spent',
                            'Which product among Electronics do you shop very often?': 'electronic_preference',
                            'Which product among Fashion do you shop very often?': 'fashion_preference',
                            'Which product among Clothing do you shop very often?': 'clothing_preference',
                            'Which OTT subscriptions do you use the most?': 'OTT',
                            'Which type of Books do you buy the most?': 'book_preference',
                            'How much time do you spend while picking the right product to buy?': 'browsing_time'})
data['age'] = data['age'].str.split().str[0]
data['age'] = pd.to_numeric(data['age'], errors='coerce')
data['age'] = data['age'].fillna(0).astype(int)
# Define the age ranges and labels
age_ranges = [0, 20, 45, float('inf')]  # Specify the age limits
labels = ['0-20', '20-45', '>45']  # Specify the labels for each range

# Speed up the ages into ranges
speed_ranges = pd.cut(data['age'], bins=age_ranges, labels=labels)
data['age_range'] = speed_ranges
data['frequently_purchased'] = data['frequently_purchased'].str.split().str[0]
mask = data.frequently_purchased.str.startswith('H')
data.loc[mask, 'frequently_purchased'] = 'Home'

# # Check for errors in marital status
for i in range(len(data['Marital Status'])):
    if data['Marital Status'][i] == 'Married' or data['Marital Status'][i] == 'Not Married':
        pass
    else:
        print(i)
# Merge product cells together
data['product_preference'] = pd.Series()
data.loc[(pd.isnull(data['fashion_preference'])) & (pd.isnull(data['book_preference'])) &
         (pd.isnull(data['electronic_preference'])), 'product_preference'] = data['clothing_preference']
data.loc[(pd.isnull(data['book_preference'])) & (pd.isnull(data['clothing_preference'])) &
         (pd.isnull(data['electronic_preference'])), 'product_preference'] = data['fashion_preference']
data.loc[(pd.isnull(data['clothing_preference'])) & (pd.isnull(data['fashion_preference'])) &
         (pd.isnull(data['electronic_preference'])), 'product_preference'] = data['book_preference']
data.loc[(pd.isnull(data['clothing_preference'])) & (pd.isnull(data['fashion_preference'])) &
         (pd.isnull(data['book_preference'])), 'product_preference'] = data['electronic_preference']
data.loc[(~pd.isnull(data['clothing_preference'])) & (~pd.isnull(data['fashion_preference'])) &
         (~pd.isnull(data['book_preference'])), 'product_preference'] = 'litigate'
data = data.drop(['fashion_preference', 'book_preference', 'clothing_preference', 'electronic_preference'], axis=1)
# del data['fashion_preference'], data['clothing_preference'], data['book_preference']
for i in range(len(data['avg_spent'])):
    if 'Between' in data['avg_spent'][i]:
        data['avg_spent'].replace(data['avg_spent'][i], '1000-5000', inplace=True)
    elif 'Greater' in data['avg_spent'][i]:
        data['avg_spent'].replace(data['avg_spent'][i], '>5000', inplace=True)
    elif 'Less' in data['avg_spent'][i]:
        data['avg_spent'].replace(data['avg_spent'][i], '<1000', inplace=True)

count_male = 0
count_female = 0
for i in data['Gender']:
    if i == 'Male':
        count_male += 1
    else:
        count_female += 1
print(f'Male: {count_male}, Female: {count_female}')


clean_data = data
clean_data.to_csv('e_commerce_clean.csv', index=False)
clean_data.to_excel('excel.xlsx', index=False)

# customers from each city tier
sns.countplot(x='city_tier', data=clean_data)
plt.title('This plot shows what  tier of cities our customers come from')
plt.show()


#
sns.countplot(data=clean_data, x='branded')
plt.title("Branded or Don't care")
plt.show()

# Relationship between customer age and genders
sns.boxplot(x='age', y='Gender', data=clean_data)
plt.title('This plot shows the age and gender relationship')
plt.show()

# Relationship between age and frequently purchased
sns.barplot(data=clean_data, x='frequently_purchased', y='age')
plt.title('This plot shows the relationship between age and frequently purchased')
plt.show()

# Scatter plot to show the relationships between frequently purchased items, gender and age
sns.scatterplot(data=clean_data, x='frequently_purchased', y='age', hue='Gender')
plt.title('Shows the relationship between age, gender and frequently purchased')
plt.show()


# Relationship between occupation and avg_spent
sns.countplot(data=clean_data, x='avg_spent', hue='occupation')
plt.title('This plot shows the relationship between occupation and avg_spent')
plt.show()

# Relationship between browsing time and occupation
sns.countplot(data=clean_data, x='browsing_time', hue='occupation')
plt.title('This plot shows the relationship between occupation and avg_spent')
plt.show()

# Relationship between browsing time and gender
sns.countplot(data=clean_data, x='browsing_time', hue='Gender')
plt.title('This plot shows the relationship between b-time and gender')
plt.show()

# Relationship between purchase time and product
sns.countplot(data=clean_data, x='product_preference')
plt.title('This plot shows the relationship between occupation and avg_spent')
plt.show()


sns.countplot(data=clean_data, x=speed_ranges)
plt.title = ('This plot shows the population in each age range setting')
plt.show()
