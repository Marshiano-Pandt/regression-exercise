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





def get_zillow_data():    
    url = env.get_db_url(db='zillow')
    query = '''
        select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
            from properties_2017
                where propertylandusetypeid = '261' 
                            
    '''

    df = pd.read_sql(query, url)

    
    return df


def wrangle_zillow():
    '''
    Aqcuiring the data and droppinfg rows that have nan.
    '''
    
    zillow = get_zillow_data()
    
    df = zillow.dropna()
    
    
    return df



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


