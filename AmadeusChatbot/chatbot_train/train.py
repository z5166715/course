# script to clean the data from ed_forum
import pandas
def my_readcsv(filename):
    data=pandas.read_csv(filename,usecols=[1,2])
    return data


if __name__ == '__main__':
    data=my_readcsv('ed_information_for_9021.csv')
    data.dropna(inplace=True)
    data.to_csv('after_clean.csv',index=False)
    pass