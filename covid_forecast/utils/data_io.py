import shutil
import requests
import pandas as pd
from datetime import date, datetime
import os


def search_for_xlsx(url='https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide'):
    """
    This search for the xlsx file to download
    :param url: where is the file to dowload
    :return: such as 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-20.xlsx'

    """
    response = requests.get(url)
    for i in response.text.split(' '):
        if (i not in ['', ' ']) and (i.__contains__('csv')) and (i.__contains__('https://www.ecdc.europa.eu/sites')):
            x = i
            print(i)
    # TODO: x could generate exception of no assignment
    url_xlsx = x.split('"')[1]
    return url_xlsx


def download_the_data(url='https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide',
    dowload_folder_name='../data/data.xlsx'):
    """
    DEPRECATED AS [European Centre for Disease Prevention and Control](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)
* Script with more cases in `/analysis/playing_with_arima.py`. chage their website.
    Download the data from url and place it in file and folder
    """
    url_xlsx=search_for_xlsx(url=url)
    response = requests.get(url_xlsx, stream=True)
    with open(dowload_folder_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return None

def get_data(dowload_folder_name = '../data/data.csv'):
    data = pd.read_csv(dowload_folder_name, encoding="ISO-8859-1")
    return data


def download_csv_from_link(url='https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',
    dowload_folder_name='../data/data.csv'):
    """
    Download the data from url and place it in file and folder
    """
    response = requests.get(url, stream=True)
    with open(dowload_folder_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return None

def download_csv_from_link_to_folder_date(url='https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',
    dowload_folder='../data/ecdc'):
    """
    download file in a folder with a time stamp so we do not do queries to the website alwasys
    :param url: where to look for
    :param dowload_folder: where to place the csv
    :return:
    """
    """
    Download the data from url and place it in file and folder
    """
    today = date.today()
    dowload_file_name = dowload_folder + '/data_ecdc_{}.csv'.format(today.strftime('%y_%m_%d'))
    response = requests.get(url, stream=True)
    with open(dowload_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return dowload_file_name


def get_data_latest_folder(dowload_folder='../../data/ecdc', keep_only_latest_file=False):
    """
    Upload the latest version of the date and if it is not up today check for a newer one.

    :param dowload_folder: folder where to place the data
    :param keep_only_latest_file: boolean. Remove all previous data files. To save space
    :return:
      data: dataframe with the data for all countries
      file_date: as datetime.date(2020, 4, 13). So it is easy to check if the data need to be refreshed. Only once per
      day
    """
    try:
        # to see if is needed to refresh which data is todaay
        today = date.today()
        # Let explore our data files to see the latest one
        list_csv_files = []
        for root, dirs, files in os.walk(dowload_folder):
            for file in files:
                if file.endswith('.csv'):
                    list_csv_files.append(file)
        if list_csv_files != []:
            # try to get the latest file
            latest_file = sorted(list_csv_files)[-1]
            dowload_file_name = dowload_folder + '/'+latest_file
        else:
            # Could happen there is not files, so let get one
            dowload_file_name = download_csv_from_link_to_folder_date(
                url='https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',
                dowload_folder=dowload_folder)
            data = pd.read_csv(dowload_file_name, encoding="ISO-8859-1")
            file_date = today
            return data, file_date
        # If there is files let get the date from the name of the file
        file_date = latest_file.split('.')[0].split('_')[-3:]
        file_date = datetime.strptime('-'.join(file_date), '%y-%m-%d').date()
        # if today we got the latest version fine if not we get it
        if file_date != today:
            dowload_file_name = download_csv_from_link_to_folder_date(
                url='https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',
                dowload_folder=dowload_folder)
            # After updating remove all previous files
            if keep_only_latest_file:
                for file in list_csv_files:
                    os.remove(dowload_folder + '/' + file)
            # update current date
            file_date = today
        data = pd.read_csv(dowload_file_name, encoding="ISO-8859-1")
        return data, file_date
    except Exception as e:
        print(e)
        print(dowload_folder)

if __name__ == '__main__':

    import doctest
    # :TODO implementation of tests
    doctest.testmod(verbose=True)

    # download the data if needed

    dowload_folder = '../../data/ecdc'
    resources_folder = 'resources'
#    """ Upload the data"""
    data, file_date = get_data_latest_folder(dowload_folder=dowload_folder, keep_only_latest_file=True)

