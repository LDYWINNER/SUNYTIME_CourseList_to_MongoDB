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
        tabula.convert_into(file_url, "output.csv",
                            output_format="csv", pages='all')
        self.df = pd.read_csv('./output.csv')
        self.category = self.df.columns
        # print(self.category) self.category = pd.DataFrame(['classNbr', 'subj', 'crs', 'courseTitle', 'sbc', 'cmp',
        # 'sctn', 'credits', 'day', 'startTime', 'endTime', 'room', 'instructor'])

    def courses2db(self, reset_db=True):
        result = True
        already_inserted_courses = []
        # TODO: should change for different files
        current_semester = '2024_spring'

        if reset_db:
            self.collection.delete_many({})

        for i in range(len(self.df)):
            try:
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
                    self.category[13]: self.df[self.category[13]].iloc[i],
                    'likes': [],
                    'reviews': []
                }

                # Check if a document with the same 'subj' and 'crs' already exists
                existing_doc = self.collection.find_one(
                    {'subj': new_data['Subj'], 'crs': new_data['CRS']})
                print("hi")
                print(existing_doc)
                print(new_data)

                if new_data['Subj'] == "AMS" or new_data['Subj'] == "ACC" or new_data['Subj'] == "BUS":
                    continue

                if existing_doc:
                    if new_data['Course Title'] not in already_inserted_courses:
                        # class nbr, cmp, sctn, day, start time, end time, room, instructor, instructor_names, semesters, unique_instructor
                        updated_class_nbr = existing_doc['classNbr'] + ', ' + str(
                            new_data['Class Nbr'])
                        updated_cmp = existing_doc['cmp'] + \
                            ', ' + str(new_data['Cmp'])
                        updated_sctn = existing_doc['sctn'] + \
                            ', ' + str(new_data['Sctn'])
                        updated_day = existing_doc['day'] + \
                            ', ' + str(new_data['Days'])
                        updated_start_time = existing_doc['startTime'] + \
                            ', ' + str(new_data['Start Time'])
                        updated_end_time = existing_doc['endTime'] + \
                            ', ' + str(new_data['End Time'])
                        updated_room = existing_doc['room'] + \
                            ', ' + str(new_data['Room'])
                        existing_doc['instructor'].append(
                            new_data['Instructor'])
                        existing_doc['semesters'].append(
                            current_semester)

                        if new_data['Instructor'] not in existing_doc['instructor_names']:
                            updated_instructor_names = existing_doc['instructor_names'] + \
                                ', ' + str(new_data['Instructor'])
                            self.collection.update_one({'_id': existing_doc['_id']}, {'$set': {
                                'instructor_names': updated_instructor_names, }})
                        if new_data['Instructor'] not in existing_doc['unique_instructor']:
                            temp_unique_instructor = existing_doc['unique_instructor'].split(
                                ", ")
                            del temp_unique_instructor[0]
                            temp_unique_instructor.append(
                                new_data['Instructor'])
                            updated_unique_instructor = ', '.join(
                                temp_unique_instructor)
                            self.collection.update_one({'_id': existing_doc['_id']}, {'$set': {
                                'unique_instructor': updated_unique_instructor
                            }})

                        self.collection.update_one({'_id': existing_doc['_id']}, {'$set': {
                                                   'classNbr': updated_class_nbr, 'cmp': updated_cmp, 'sctn': updated_sctn, 'day': updated_day, 'startTime': updated_start_time, 'endTime': updated_end_time, 'room': updated_room, }})

                    # If the course is already inserted => use / if LEC and () if REC or LAB
                    else:
                        if new_data['Cmp'] == 'LEC':
                            slash_updated_class_nbr = existing_doc['classNbr'] + \
                                '/' + str(new_data['Class Nbr'])
                            slash_updated_cmp = existing_doc['cmp'] + \
                                '/' + str(new_data['Cmp'])
                            slash_updated_sctn = existing_doc['sctn'] + \
                                '/' + str(new_data['Sctn'])
                            slash_updated_day = existing_doc['day'] + \
                                '/' + str(new_data['Days'])
                            slash_updated_start_time = existing_doc['startTime'] + \
                                '/' + str(new_data['Start Time'])
                            slash_updated_end_time = existing_doc['endTime'] + \
                                '/' + str(new_data['End Time'])
                            slash_updated_room = existing_doc['room'] + \
                                '/' + str(new_data['Room'])

                            self.collection.update_one({'_id': existing_doc['_id']}, {
                                '$set': {'classNbr': slash_updated_class_nbr, 'cmp': slash_updated_cmp, 'sctn': slash_updated_sctn, 'day': slash_updated_day, 'startTime': slash_updated_start_time, 'endTime': slash_updated_end_time, 'room': slash_updated_room}})
                        else:
                            paren_updated_class_nbr = existing_doc['classNbr'] + \
                                '(' + str(new_data['Class Nbr']) + ')'
                            paren_updated_cmp = existing_doc['cmp'] + \
                                '(' + str(new_data['Cmp']) + ')'
                            paren_updated_sctn = existing_doc['sctn'] + \
                                '(' + str(new_data['Sctn']) + ')'
                            paren_updated_day = existing_doc['day'] + \
                                '(' + str(new_data['Days']) + ')'
                            paren_updated_start_time = existing_doc['startTime'] + \
                                '(' + str(new_data['Start Time']) + ')'
                            paren_updated_end_time = existing_doc['endTime'] + \
                                '(' + str(new_data['End Time']) + ')'
                            paren_updated_room = existing_doc['room'] + \
                                '(' + str(new_data['Room']) + ')'

                            self.collection.update_one({'_id': existing_doc['_id']}, {
                                '$set': {'classNbr': paren_updated_class_nbr, 'cmp': paren_updated_cmp, 'sctn': paren_updated_sctn, 'day': paren_updated_day, 'startTime': paren_updated_start_time, 'endTime': paren_updated_end_time, 'room': paren_updated_room}})

                    already_inserted_courses.append(new_data['Course Title'])
                else:
                    if new_data['Cmp'] == 'LEC':
                        self.collection.insert_one(new_data)

                        already_inserted_courses.append(
                            new_data['Course Title'])

            except Exception as e:
                print(e)
                continue
