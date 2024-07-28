# import csv
#
# input_file = './course3.csv'
# output_file = 'output3.csv'
#
# # 원하는 열 순서 정의
# new_fieldnames = {
#     'classNbr', 'subj', 'crs', 'courseTitle', 'sbc', 'cmp', 'sctn', 'credits', 'day',
#     'startTime', 'endTime', 'past_instructors', 'recent_two_instructors', 'most_recent_instructor',
#     'avgGrade', 'likes', 'location', 'id', 'semesters'
# }
#
# # 기본값 정의
# default_values = {
#     'likes': 0,
#     'avgGrade': 0,
#     'semesters': '?',
#     'past_instructors': {},
#     'recent_two_instructors': {},
#     'most_recent_instructor': '?'
# }
#
# with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
#     reader = csv.DictReader(infile)
#     fieldnames = reader.fieldnames
#
#     # DictWriter를 새 fieldnames와 함께 설정
#     writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
#     writer.writeheader()
#
#     for row in reader:
#         # location 필드 값을 수정
#         if 'location' in row:
#             row['location'] = f'{{{row["location"]}}}'
#
#         # 새로운 열에 기본값 설정
#         for col in new_fieldnames:
#
#             if col not in row:
#
#                 row[col] = default_values.get(col, '')
#
#         # 새로운 열에 기본값을 적용한 행을 작성
#         new_row = {field: row.get(field, '') for field in new_fieldnames}
#         writer.writerow(new_row)
import csv

input_file = './course3.csv'
output_file = 'output5.csv'

# 원하는 열 순서 정의 (리스트로 변경)
new_fieldnames = [
    'classNbr', 'subj', 'crs', 'courseTitle', 'sbc', 'cmp', 'sctn', 'credits',
    'day', 'startTime', 'endTime', 'past_instructors', 'recent_two_instructors',
    'most_recent_instructor', 'avgGrade', 'likes', 'location', 'id', 'semesters'
]

# 기본값 정의
default_values = {
    'likes': 0,
    'avgGrade': 0,
    'semesters': '?',
    'past_instructors': '{}',
    'recent_two_instructors': '{}',
    'most_recent_instructor': '?'
}

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
    writer.writeheader()

    for row in reader:
        # location 필드 값을 수정
        if 'location' in row:
            row['location'] = f'{{{row["location"]}}}'

        for field in row:
            if row[field] == '':
                row[field] = '?'
        # 새로운 열에 기본값 설정 및 기존 값 유지
        new_row = {}
        for field in new_fieldnames:

            if field in row:
                new_row[field] = row[field]
            else:
                new_row[field] = default_values.get(field, '')

        writer.writerow(new_row)

print("CSV 파일 변환이 완료되었습니다.")
