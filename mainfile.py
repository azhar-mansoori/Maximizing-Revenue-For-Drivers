import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import scipy.stats as st
import warnings
warnings.filterwarnings('ignore')
print("strt")
#reading data
df = pd.read_csv('Data/TaxiTripData.csv')
print("data load")

#converting into datetime format                                            
df['tpep_pickup_datetime']=pd.to_datetime(df['tpep_pickup_datetime']) 
print(df['tpep_pickup_datetime'])               
df['tpep_dropoff_datetime']=pd.to_datetime(df['tpep_dropoff_datetime'])
print('change')

#finding the trip duration              
df['duration']=df['tpep_dropoff_datetime']-df['tpep_pickup_datetime']                
df['duration']=df['duration'].dt.total_seconds()/60                   #converting into minutes
print('time')
#Extracting columns need for testing
df=df[['passenger_count','payment_type','fare_amount','trip_distance','duration']]
print("eda")
#droping null values as it is 1% only 
df=df.dropna(inplace=True)

#converting into integer values as it is in float
df['passenger_count']=df['passenger_count'].astype('int64')
df['payment_type']=df['payment_type'].astype('int64')
print('int')

#Removing the duplictes values 
df=df.drop_duplicates(inplace=True)

#Removing OUTLIERS from Payment Type and Passenger Count 
df=df[df['payment_type']<3]  #taking Card and Cash

df=df[(df['passenger_count']>0) & (df['passenger_count']<6)]  #taking passenger count 1 to 5 only

#changing payment type as cash and card
df['payment_type']=df['payment_type'].replace([1,2],['card','cash'],inplace=True)

#remove negative values from numerical vales 
df=df[df['fare_amount']>0]
df=df[df['trip_distance']>0]
df=df[df['duration']>0]
print("-tive ")

#remove outliers using InterQuantile Range
for col in ['fare_amount','trip_distance','duration']:
    q1=df[col].quantile(0.25)
    q3=df[col].quantile(0.75)
    IQR=q3-q1

    lower_bound=q1-1.5*IQR
    upper_bound=q3+1.5*IQR

    df=df[(df[col]>=lower_bound) & (df[col]<= upper_bound)]
print("outlires")
#doiing hypothesis testing using T-test 
card_sample=df[df['payment_type']=='card']['fare_amount']
cash_sample=df[df['payment_type']=='cash']['fare_amount']

t_stats,p_value=st.ttest_ind(a=card_sample,b=cash_sample,equal_var=False)
print("end")

print("T Statistics",t_stats,"p_values",p_value)

