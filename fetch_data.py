import os
import requests
import pandas as pd
# import flatten_json
from sqlalchemy import create_engine

def fetch_ticketmaster_data(state_code: list, country_code: str) -> pd.DataFrame:
    """Fetches data from the Ticketmaster """
    
    event_list = []
    page_number = 0

    while True:

        ticketmaster_api_key = 'Yn7rF52hOv8TYqTtjrLnrt9ycOJFD87F'
        base_url = 'https://app.ticketmaster.com/discovery/v2/events.json'
        params = {
            'apikey': ticketmaster_api_key,
            # 'city': city_name,
            'stateCode': state_code,
            'countryCode': country_code,
            'size': 100,
            'page' : page_number
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'page' in data:
            total_pages = data['page']['totalPages']

            if data['page']['number'] < total_pages:
                events = data['_embedded']['events']
                event_list.extend(events)
                print(f'Getting {page_number + 1} out of {total_pages} pages')

                page_number += 1

            else:
                break
        else:
            break

    df = pd.DataFrame(event_list)
    df.rename(columns={'':'blank'}, inplace=True)
    duplicate_cols = df.columns[df.columns.duplicated()]
    df.drop(columns=duplicate_cols, inplace=True)
    df.drop(columns=['locale','images','promoter','pleaseNote','products','seatmap','test',
                     'accessibility','ticketLimit','ticketing','_links', 'doorsTimes', 'outlets', 'ageRestrictions'], inplace=True)
    print(df)
    return df

def transform(df, cols_to_flatten):
    """Flatten columns with nested list/dict values"""

    def flatten_data(y):
        out = {}
        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x
        flatten(y)
        return out
    
    df_root = df.drop(columns=cols_to_flatten, inplace=False)
    
    flattened_dfs = []

    for col in cols_to_flatten:
        flattened_col = df[col].apply(flatten_data)
        flattened_df = pd.DataFrame.from_records(flattened_col)
        
        if '' in flattened_df.columns:
            flattened_df.rename(columns={'':'blank'}, inplace=True)
            # duplicate_cols = flattened_df.columns[flattened_df.columns.duplicated()]
            flattened_df.drop(columns='blank', inplace=True)

        flattened_dfs.append(flattened_df)

    concat_df = pd.concat(flattened_dfs, axis=1)
    merged_df = pd.concat([df_root, concat_df], axis=1)
    
    print(merged_df)
    return merged_df

def finalize(df):
    """Drop unecessary columns and rename column labels"""

    condition = '^[1-9]_|_[2-9]_|_[1-9][0-9]_|.*image|.*inks|.*upcoming|attractions.*classifications|.*arking|box.?ffice|.*arket|.*dma|.*ada|.*lias|test|.*TB[A-D]|.*ocale|.*eneral.?nfo|.*ocial|.*ccessible.*eating'
    col_ind = df.filter(regex=condition).columns
    df.drop(columns=col_ind, inplace=True)

    new_cols = df.columns.str.replace('0_', 'temp_').to_list()
    new_df = df.set_axis(new_cols, axis=1)

    new_df.rename(columns={'':'blank'}, inplace=True)
    duplicate_cols = new_df.columns[new_df.columns.duplicated()]
    new_df.drop(columns=duplicate_cols, inplace=True)
    
    print(new_df)

    return new_df

def ingest_data(df):
    """Load data to Postgres"""

    user="awahfgjj"
    password="wnvI7QEwTduxzf89CKeh1JGDPG8668Ns"
    host="satao.db.elephantsql.com"
    port="5432"
    db="awahfgjj"
    table_name="ticketmaster_data"

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')


df = fetch_ticketmaster_data(['CA','GA','IL','NC','NY','TX'], 'US')
flatten_df = transform(df, ['sales','dates','classifications','promoters','priceRanges','_embedded'])
df_final = finalize(flatten_df)
ingest_data(df_final)