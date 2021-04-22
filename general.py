"""
Created on Mon Jan 25 09:47:18 2021

@author: jiverson

These are simple functions that I like to use across different projects
These allow me to reuse my code and be more effective.
They aren't anything too special, but they are useful
"""
import pickle

def chunks(l,n=5):
    '''
    params: 
        l: taks in a list (or list like object)
        n: takes an int: default = 5 this is how big the smaller
            chunks will be
    returns:
        a list of lists with the smaller lists being size n
    '''
    return [l[i:i + n] for i in range(0, len(l), n)]

def pickle_write(file_name,data):
    '''
    takes a filename and data and writes it to pickle
    '''
    with open(file_name, 'wb') as fid:
        pickle.dump(data, fid, pickle.HIGHEST_PROTOCOL)
      
def pickle_read(file_name):
    '''
    takes a filename and reads from pickle
    '''
    with open(file_name,'rb') as f:
        data=pickle.load(f)
    return data


def replace_text(text,
                delimiter,
                location,
                new_text):
    '''
    delimit_change_join
    
    takes in a string, a delimiter, location (to change the string), and 
    new text to replace at the desired location
    
    this funciton splits,changes the desired text (at the proper location) to
    the new_text variable.
    
    it then returns a joined string
    '''
    
    temp = text.split(delimiter)
    temp[location] = new_text
    return delimiter.join(temp)