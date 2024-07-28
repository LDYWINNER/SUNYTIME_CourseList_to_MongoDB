# You need to install pymongo, tabula, and pandas libraries
import pymongo
import tabula
import pandas as pd

import course2db

# 1. Input your MongdoDB's USERNAME and PASSWORD
converter = course2db.Converter(
    username='ldywinner',
    password='utWlobRJxeZEWlnV'
)

# 2. Set the client and make a db and a collection
converter.set_collection(db_name='SSU-GANG-PYEONG', collection_name='course')

# 3. convert the pdf file to make a table - Please write the path of the course list pdf file
converter.pdf2csv(file_url='./2024_spring.pdf')

# 4. Add course info to your database
converter.courses2db(reset_db=False)
