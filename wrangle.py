import os 
import env
import pandas as pd
from sklearn.model_selection import train_test_split





def check_file_exists(filename, query, url):
    if os.path.exists(filename):
        print('this file exists, reading csv')
        df = pd.read_csv(filename, index_col=0)
    else:
        print('this file doesnt exist, read from sql, and export to csv')
        df = pd.read_sql(query, url)
        df.to_csv(filename)
        
    return df



###################################

def get_zillow_data(): 
    '''
    got the data from the Mysql database,
    ran a query to get specific columns that are 'Single Family Residential'(261) properties
    '''
    filename = "zillow.csv"

    if os.path.isfile(filename):

        return pd.read_csv(filename, index_col=0)
    
    
    url = env.get_db_url(db='zillow')
    query = '''
        select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
            from properties_2017
                where propertylandusetypeid = '261' 
                            
    '''

    # Read the SQL query into a dataframe
    df = pd.read_sql(query, url)

        # Write that dataframe to disk for later. Called "caching" the data for later.
    df.to_csv(filename)

        # Return the dataframe to the calling code
    
    

    return df
################################


def prep_zillow(df):
    '''
    This function takes in a dataframe
    renames the columns and drops nulls values
    Additionally it changes datatypes for appropriate columns
    and renames fips to actual county names.
    Then returns a cleaned dataframe
    '''
    df = df.rename(columns = {'bedroomcnt':'bedrooms',
                     'bathroomcnt':'bathrooms',
                     'calculatedfinishedsquarefeet':'area',
                     'taxvaluedollarcnt':'taxvalue',
                     'fips':'county'})
    
    df = df.dropna()
    
    make_ints = ['bedrooms','area','taxvalue','yearbuilt']

    for col in make_ints:
        df[col] = df[col].astype(int)
        
    df.county = df.county.map({6037:'LA',6059:'Orange',6111:'Ventura'})
    
    return df

##################################
def wrangle_zillow():
    '''
    Aqcuiring the data and droppinfg rows that have nan.
    '''
    
    zillow = get_zillow_data()
    
    df = prep_zillow(zillow)
    
    
    return df

##########################################

def splitting_data(df, col):
    '''
    splitting the data into models of train, validate, and test.
    '''
    #first split
    train, validate_test = train_test_split(df, 
                                            train_size=0.6,
                                            random_state=123,
                                            stratify=df[col]
                                           )
    
    validate, test = train_test_split(validate_test,
                                      train_size=0.5,
                                      random_state=123,
                                      stratify=validate_test[col]
                                      
                                     )
    return train, validate, test


