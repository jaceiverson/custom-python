"""
These are specific functions/classes pertaining to the pandas library
"""
import pandas as pd
import numpy as np

def ccounts(series):
    '''
    This accepts a PD.Series object and returns a 2 column df showing
    Value_counts and the percent of total
    df['count','percent']
    '''
    df=pd.DataFrame([series.value_counts(),series.value_counts(normalize=True)]).T
    df.columns=['count','percent']
    return df

class CompareDF():
    '''
    This class compares 2 data frames. 
    It will show you what has been added,removed, and altered. 
    This will be output in a dictionary object for use.
    '''
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
        
        Based on
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
    
    def summary(self):
      cols = ['Total Rows in New','Rows Added','Rows Removed','Rows Changed']
      data = [df2.shape[0],compare.added().shape[0],compare.removed().shape[0],compare.results.shape[0]]
      return pd.DataFrame([data],columns=cols)

class IndexCompare():
    '''
    Compares column data across all index values
    This is useful when comparing survey results, quiz scores (for specific questions)
    Best used with small pd.DF indexes
    
    Accepts a pd.DF
    
    Call IndexCompare.run() to gather the data
    
    Call self.out to print the data out to console
    '''
    def __init__(self,df):
        self.df = df
        self.data = {}
        
    def run(self):
        self.get_diff_df()
        self.get_comparisons()
        self._init_comparison_data()
        self.all_categories()
    
    def get_diff_df(self):
        #compare each index item accross all columns in the index
        for x in self.df.index:
            #print('X: {}'.format(x))
            self.data[x] = {}
            self.data[x]['raw'] = self.df.loc[x] - self.df.drop(x,axis=0)
    def get_comparisons(self):             
        #determine which index id is most similar and most different for each index
        for x in self.data:
            temp = self.data[x]['raw'].loc[self.data[x]['raw'].index != x].abs().sum(axis=1)
            self.data[x]['similar'] = {'id':temp.idxmin(),'total diff':temp.min()}
            self.data[x]['different'] = {'id':temp.idxmax(),'total diff':temp.max()}
            self.data[x]['avg total distance'] = (self.df.loc[x] - self.df.drop(x,axis=0)).abs().sum(axis=1).mean()

    def _init_comparison_data(self):    
        #init all categorization dicts
        self.most_diff = {'id':None,'total diff':None}
        self.most_same = {'id':None,'total diff':None}
        self.most_similar_to_all = {'id': None,'avg total distance': None}
        self.most_different_to_all = {'id': None, 'avg total distance': None}

    def all_categories(self):
        #find most_diff, most_same, most_similar_to_all, and most_different_to_all
        for x in self.data:
            if self.most_same['total diff'] == None or self.data[x]['similar']['total diff'] < self.most_same['total diff']:
                self.most_same['id'] = x + ' + ' + self.data[x]['similar']['id']
                self.most_same['total diff'] = self.data[x]['similar']['total diff']
                self.most_same['avg diff'] = self.most_same['total diff'] / len(self.df.columns)
            if self.most_diff['total diff'] == None or self.data[x]['different']['total diff'] > self.most_diff['total diff']:
                self.most_diff['id'] = x + ' + ' + self.data[x]['different']['id']
                self.most_diff['total diff'] = self.data[x]['different']['total diff']
                self.most_diff['avg diff'] = self.most_diff['total diff'] / len(self.df.columns)
                
            if self.most_similar_to_all['id'] == None or self.data[x]['avg total distance'] < self.most_similar_to_all['avg total distance']:
                self.most_similar_to_all['id'] = x
                self.most_similar_to_all['avg total distance'] = self.data[x]['avg total distance']
            if self.most_different_to_all['id'] == None or self.data[x]['avg total distance'] > self.most_different_to_all['avg total distance']:
                self.most_different_to_all['id'] = x
                self.most_different_to_all['avg total distance'] = self.data[x]['avg total distance']
                
            self.stats =   {'Similar':self.most_same,
                            'Different': self.most_diff,
                            'Similar to All (smallest average total distance)':self.most_similar_to_all,
                            'Different to All (largest average total distance)':self.most_different_to_all}
        
    def out(self):
        for x in self.data:
            print('{}:\nS:{},\nD:{}\n'\
                  .format(x,self.data[x]['similar'],self.data[x]['different']))
                
        for y in self.stats:
            if 'avg total distance' in self.stats[y].keys():
                print('Most {}: {}\n'\
                      'Average Total Difference: {:.2f}\n'\
                      .format(y,
                              self.stats[y]['id'],
                              self.stats[y]['avg total distance'],)
                      )
            else:
                print('Most {}: {}\n'\
                      'Total Difference: {:.2f}\n'\
                      'Average Difference: {:.2f}\n'\
                      .format(y,
                              self.stats[y]['id'],
                              self.stats[y]['total diff'],
                              self.stats[y]['avg diff'])
                      )
        
    
    
    
    
