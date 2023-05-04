import requests, json
header = {"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjEzOTI1ODI5ODEiLCJhdXRoX2lkIjoiMiIsImV4cCI6MTY4OTg5MzQ2MSwiaWF0IjoxNjc0MzQxNDYxLCJuYmYiOjE2NzQzNDE0NjEsInNlcnZpY2VfaWQiOiI0MzAwMTEzOTciLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.7h1xoegE8xHK7TJjcgXRxs9ZS08Vtr6EBDXBuxJ-7tY"}
count = 1000
date = "2023-05-02"

url = f"https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results?count={count}&date={date}"#&cursor={cursor}"

result = requests.get(url, headers=header)
print(result.text)
data_dict = json.loads(result.text)
print(data_dict)
black_count = 0
add_cube_count = 0
black_sucess = 0
black_fail = 0
add_cube_sucess = 0
add_cube_fail = 0
for i in reversed(data_dict.get('cube_histories', {})):
    if i.get('character_name') == '오라웨푼':
        if i.get('cube_type') == '블랙 큐브':
            black_count += 1
            if i.get('item_upgrade_result') == '성공':
                black_sucess += 1
                black_count_sucess = black_count
            else:
                black_fail += 1
        elif i.get('cube_type') == '에디셔널 큐브':
            add_cube_count += 1
            if i.get('item_upgrade_result') == '성공':
                add_cube_sucess += 1
                add_cube_count_sucess = add_cube_count
            else:
                add_cube_fail += 1

print(black_count_sucess, black_sucess, black_fail, add_cube_count_sucess, add_cube_sucess, add_cube_fail)