import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SequentialFeatureSelector as SequentialFeatureSelector
import statsmodels.api as sm
import matplotlib.colors as mcolors
import geopandas as gpd

pd.options.display.max_columns = 100

df_unemployment = pd.read_csv("")
df_leases = pd.read_csv("")
#Only taking the availability to use in Graph, for practice purposes
df_percentAvailable = df_leases[['availability_proportion','state']]

#This is to look at the normal distribution of the percent available
df_percentAvailable = df_percentAvailable[df_percentAvailable.state.str.len()==2]

#linear regression for price sensitivity by state affected by unemployment
df_state_price = df_leases.groupby(['state', 'year', 'quarter']).agg(
    price=('overall_rent', 'mean')
).reset_index()
df_unemployment2=df_unemployment[['state','year','quarter','unemployment_rate']]
df_state = df_state_price.merge(df_unemployment2,on=['state','year','quarter']).dropna()

x = df_state[['unemployment_rate']]
y = df_state['price']
y_log = np.log(y)

# Add state dummy variables
state_dummies = pd.get_dummies(df_state['state'], drop_first=True)
state_dummies = state_dummies.astype(int)

# Concatenate unemployment rate and state dummies
x = pd.concat([x, state_dummies], axis=1).dropna()

# Step 2: Create interaction terms between 'unemployment_rate' and each state dummy variable
for state in x.columns[1:]:  # Exclude 'unemployment_rate' and 'Price' from the loop
    x[f'Unemployment_{state}'] = x[state] * x['unemployment_rate']

interaction_terms = x.filter(like='Unemployment')  # This will get all columns with 'Unemployment' in their name
interaction_terms['unemployment_rate'] = x['unemployment_rate']

x_cleaned = interaction_terms.copy()

# Step 2: Define the dependent variable (Price) and the independent variables (including interaction terms)
# Add constant term (intercept)
x_cleaned = sm.add_constant(x_cleaned)  
# Fit the OLS model
ols_model = sm.OLS(y_log, x_cleaned)
results = ols_model.fit()

# Extract coefficients and their standard errors
coefficients = results.params

# # Create a DataFrame for the coefficients
coeff_df = coefficients.reset_index()
coeff_df.columns = ['Variable', 'Coefficient']
# Exclude the intercept
state_coeffs_df = coeff_df[coeff_df['Variable'] != 'const']  

#===================================== DO NOT TOUCH ================================================

#1. get rid of Unemployment_ and only keep state as name in 'Variable' column. Done
#2 . change "unemployement_rate" to "AZ"
#Add the intercept affect 
number_to_add = -0.031705
state_coeffs_df.iloc[:-1, state_coeffs_df.columns.get_loc('Coefficient')] += number_to_add
#changing the intercept affect to AZ since this is the varibable removed
state_coeffs_df.loc[state_coeffs_df['Variable'] == 'unemployment_rate', 'Variable'] = 'AZ'
#Removing the Unemployment_ so it is easier to merge and connect to heat map
state_coeffs_df['Variable'] = state_coeffs_df['Variable'].str.replace('Unemployment_', '', regex=False)
#Code for heat map merging heat map and price sensitivity
gdf = gpd.read_file('/Users/jonangui23/Documents/cb_2018_us_state_5m/cb_2018_us_state_5m.shp')
gdf = gdf.merge(state_coeffs_df,left_on='STUSPS',right_on='Variable', how = 'left')
#plotting heat map
# Plot
fig, ax = plt.subplots(figsize=(15, 10))
#Only plot valid geometries
gdf.dropna(subset=['geometry']).plot(
    column='Coefficient',
    cmap='plasma',
    edgecolor='black',
    legend=True,
    ax=ax
)
plt.title('States with Diverse Economies are less \n Price Sensitive to Unemployment', fontsize=20)
plt.axis('off')
plt.show()
