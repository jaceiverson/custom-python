"""
These are specific functions/classes pertaining to pandas
"""

import pandas as pd
import numpy as np

def ccounts(series):
    '''
    This accepts a PD.Series object and returns a 2 column table showing
    Value_counts and the percent of total
    
    df['count','percent']
    
    '''
    df=pd.DataFrame([series.value_counts(),series.value_counts(normalize=True)]).T
    df.columns=['count','percent']
    return df

class CompareDF():

    def __init__(self,old_df,new_df):
        '''
        old_df: what the df looked like
        new_df: what the df changed too
        '''
        self.df1 = old_df
        self.df2 = new_df
        
        self.remove = self.removed()
        self.add = self.added()
        
        self.clean_df1 = self.df1.loc[~self.df1.index.isin(self.remove)].copy()
        self.clean_df2 = self.df2.loc[~self.df2.index.isin(self.add)].copy()
        
        self.compare()
        
    def compare(self):
        '''
        COMPARE 2 pd.dfs and returns the index & columns as well as what changed.
        
        Indexes must be matching same length/type
        
        Comes from
        https://stackoverflow.com/questions/17095101/compare-two-dataframes-and-output-their-differences-side-by-side
        '''
        
        ne_stacked = (self.clean_df1 != self.clean_df2).stack()
    
        changed = ne_stacked[ne_stacked]
    
        changed.index.names = ['ID', 'Column']
    
        difference_locations = np.where(self.clean_df1 != self.clean_df2)
        
        changed_from = self.clean_df1.values[difference_locations]
        changed_to = self.clean_df2.values[difference_locations]
        
        final = pd.DataFrame({'from': changed_from, 'to': changed_to},index=changed.index)
    
        self.results = final.dropna(how='all')
    
    def removed(self,full=False):
        '''
        full: bool: if True will return the entire row, if False just the index
        '''
        if full:
            return self.df1.loc[~self.df1.index.isin(self.df2.index)]
        else:
            return self.df1.loc[~self.df1.index.isin(self.df2.index)].index.values
    
    def added(self,full=False):
        '''
        full: bool: if True will return the entire row, if False just the index
        '''
        if full:
            return self.df2.loc[~self.df2.index.isin(self.df1.index)]
        else:
            return self.df2.loc[~self.df2.index.isin(self.df1.index)].index.values
    
    def output(self):
        return {'ADDED': self.add,'REMOVED': self.remove,'CHANGED':self.results}