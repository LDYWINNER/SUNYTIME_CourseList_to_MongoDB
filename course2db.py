import pymongo
import tabula
import pandas as pd


class Converter:
    username = ''
    password = ''
    client = ''
    collection = ''
    db = ''
    df = ''
    category = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = pymongo.MongoClient(
            f'mongodb+srv://{self.username}:{self.password}@ssu-gang-pyeong.6s8in70.mongodb.net/?retryWrites=true&w=majority')

    def set_collection(self, db_name, collection_name):
        # self.collection = self.client.test.courses
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def pdf2csv(self, file_url):
        tabula.convert_into(file_url, "output.csv", output_format="csv", pages='all')
        self.df = pd.read_csv('./output.csv')
        self.category = self.df.columns
        # print(self.category) self.category = pd.DataFrame(['classNbr', 'subj', 'crs', 'courseTitle', 'sbc', 'cmp',
        # 'sctn', 'credits', 'day', 'startTime', 'endTime', 'room', 'instructor'])

    def courses2db(self, reset_db=True):
        result = True
        if reset_db:
            self.collection.delete_many({})
        try:
            for i in range(len(self.df)):
                new_data = {
                    self.category[0]: self.df[self.category[0]].iloc[i],
                    self.category[1]: self.df[self.category[1]].iloc[i],
                    self.category[2]: self.df[self.category[2]].iloc[i],
                    self.category[3]: self.df[self.category[3]].iloc[i],
                    self.category[4]: self.df[self.category[4]].iloc[i],
                    self.category[5]: self.df[self.category[5]].iloc[i],
                    self.category[6]: self.df[self.category[6]].iloc[i],
                    self.category[7]: self.df[self.category[7]].iloc[i],
                    self.category[8]: self.df[self.category[8]].iloc[i],
                    self.category[9]: self.df[self.category[9]].iloc[i],
                    self.category[10]: self.df[self.category[10]].iloc[i],
                    self.category[11]: self.df[self.category[11]].iloc[i],
                    self.category[12]: self.df[self.category[12]].iloc[i],
                    'likes': [],
                    'reviews': []
                }
                
                # Check if a document with the same 'subj' and 'crs' already exists
                existing_doc = self.collection.find_one({'Subj': new_data['Subj'], 'CRS': new_data['CRS']})
                print("hi")
                print(existing_doc)

                if existing_doc:
                    # Update the 'Class Nbr' field by appending the new data
                    updated_class_nbr = existing_doc['Class Nbr'] + ', ' + new_data['Class Nbr']
                    self.collection.update_one({'_id': existing_doc['_id']}, {'$set': {'Class Nbr': updated_class_nbr}})
                else:
                    # Insert a new document
                    self.collection.insert_one(new_data)
        except Exception as e:
            print(e)
            result = False
        if result:
            print('The courses info succesfully added to your DB!')
        else:
            print('Sorry! Fail to add your courses info to your DB...')
