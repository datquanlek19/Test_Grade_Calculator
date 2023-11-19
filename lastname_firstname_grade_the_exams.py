import os
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd


# Task 1: kiểm tra file có tồn tại không và thông báo cho người dùng
def open_file(file_path):
    # Kiểm tra xem file có tồn tại hay không và mở file
    try:
        with open(file_path, 'r') as file:
            read_file = file.read()
            print(f'Successfully opened {filename}.txt')

    # Nếu file không tồn tại thì thông báo và thoát hẳn chương trình   
    except FileNotFoundError:
        print(f'File {filename} canot be found.')
        sys.exit()

# Task 2: kiểm tra các giá trị hợp lệ và thông báo
def validate_data(file_path):
    with open(file_path, 'r') as rf:
        # Đọc file truyền vào dataframe
        readfile = rf.readlines()

        print('**** ANALYZING ****')

        # Biến đếm dòng không hợp lệ
        invalid_line = 0

        # Tạo vòng lặp qua tất cả các row
        for line in readfile:  
            # Đếm số phần tử trong 1 dòng ngăn cách bởi dấu ','
            counts = len(line.split(','))

            #Kiểm tra đủ số phần tử, nếu không đủ thì báo ra màn hình và chuyển tới dòng tiếp theo
            if counts != 26:
                print(f'Invalid line of data: does not contain exactly 26 values:\n{line.strip()}')
                invalid_line += 1
                continue
            
            # Kiểm tra định dạng ID học sinh nếu không đúng thì chuyển sang dòng tiếp theo
            match = re.match(r'^N\d{8},', line)
            if not match:
                print(f'Invalid line of data: N# is invalid\n{line.strip()}')
                invalid_line += 1
                continue

        #Nếu không có lỗi gì thì báo ra màn hình                
        if invalid_line == 0:
            print('No errors found!')

        # In các báo cáo ra màn hình
        print('**** REPORT ****')
        valid_line = len(readfile) - invalid_line
        print(f'Total valid lines of data: {valid_line}')
        print(f'Total invalid lines of data: {invalid_line}')

# Task 3: tính điểm
def grade_exam(file_path):
    # Key đáp án:
    answer_key = 'B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D'

    # Thông số quan tâm
    count_line = 0          # Số dòng hợp lệ trong class
    scores_array = []       # Mảng lưu tất cả điểm của class
    high_scores = 0         # Số lượng hs đạt điểm cao (>80)
    question_skip = 0       # Câu bị bỏ qua nhiều nhất
    question_incorrect = 0  # Câu sai nhiều nhất
    skip_arr = []           # Lưu vị trí những câu bỏ qua
    incorr_arr = []         # Lưu vị trí những câu sai
    grades = []             # Lưu lại kết quả điểm của hs

    # Mở file
    with open(file_path, 'r') as rf:
        readfile = rf.read()

    # Tách thành từng các dòng
    lines = readfile.split('\n')

    # So sánh từng row với answer_key
    for line in lines:
        correct = 0         # Số câu đúng
        incorrect = 0       # Số câu sai
        not_found = 0       # Số câu bỏ qua
        scores = 0          # Điểm của hs

        # Tạo 2 array để chấm điểm
        stu = (line.split(',')[1:])     # Bài làm của hs
        ans = (answer_key.split(','))   # Đáp án
        
        # Kiểm tra điều kiện số câu tl (Task 2)
        if len(stu) != 25:
            continue
        
        # Kiểm tra điều kiện mã học sinh (Task 2)
        if not re.match(r'^N\d{8},', line):
            continue
        
        # Tính điểm cho học sinh
        for i in range(len(stu)):
            # Đếm câu đúng
            if stu[i] == ans[i]:
                correct += 1
                continue
            
            # Đếm câu không làm
            if stu[i] == '':
                not_found += 1
                skip_arr.append(i+1)
                continue

            # Đếm câu sai
            incorrect += 1
            incorr_arr.append(i+1)

        # Tính điểm
        count_line += 1
        scores = correct*4 - incorrect
        scores_array.append(scores)

        grades.extend([line.split(',')[0], scores])

        if scores > 80:
            high_scores += 1

    mean_scores = np.mean(scores_array)         # Điểm trung bình của class
    highest_score = max(scores_array)           # Điểm cao nhất
    lowest_score = min(scores_array)            # Điểm thấp nhất
    range_score = highest_score - lowest_score  # Miền giá trị điểm
    median_score = int(np.median(scores_array)) # Giá trị trung vị

    # Đếm số lần xuất hiện của mỗi câu bị bỏ qua
    skip_counter = Counter(sorted(skip_arr))
    max_skip_count = max(skip_counter.values())                                 # Tìm số lần lặp nhiều nhất
    skip_rate = max_skip_count/count_line                                       # Tính tỉ lệ bỏ qua
    skip_result = [k for k, v in skip_counter.items() if v == max_skip_count]   # Tìm tất cả các phần tử có số lần lặp nhiều nhất

    # Đếm số lần xuất hiện của mỗi câu sai
    incorr_counter = Counter(sorted(incorr_arr))
    max_incorr_count = max(incorr_counter.values())                                 # Tìm số lần lặp nhiều nhất
    incorr_rate = max_incorr_count/count_line                                       # Tính tỉ lệ câu sai
    incorr_result = [k for k, v in incorr_counter.items() if v == max_incorr_count] # Tìm tất cả các phần tử có số lần lặp nhiều nhất

    # In kết quả ra màn hình
    print('Total student of high scores:', high_scores)
    print(f'Mean (average) score: {mean_scores:.2f}')
    print('Highest score:', highest_score)
    print('Lowest score:', lowest_score)
    print('Range of scores:', range_score)
    print('Median score:', median_score)
    print(f'Question that most people skip: ' + ', '.join(f'{el} - {max_skip_count} - {skip_rate:.2f}' for el in skip_result))
    print(f'Question that most people answer incorrectly: ' + ', '.join(f'{el} - {max_incorr_count} - {incorr_rate:.2f}' for el in incorr_result))

    return grades

# Task 4: lưu kết quả
def result_save(grades):
    # Chuyển đổi mảng thành DataFrame
    df = pd.DataFrame({'key': grades[::2], 'value': grades[1::2]})

    # Ghi DataFrame vào tệp txt
    df.to_csv(f'{filename}_grades.txt', index=False, header=False)

# Chương trình chính
# Nhập tên file cần tìm
filename = input('Enter a class to grade (i.e. class1 for class1.txt): ')

# Đường dẫn tới thư mục chứa file .py
folder_path = os.path.dirname(os.path.realpath(__file__))

# Tạo đường dẫn tới file muốn mở
file_path = folder_path + '/Data Files/' + filename + '.txt'

open_file(file_path)
validate_data(file_path)
a = grade_exam(file_path)
result_save(a)
