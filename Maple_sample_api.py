import requests, json
from datetime import timedelta, datetime

def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates

def api_test():
    with open("./resource/API_key.json", 'rt') as fp1:
        value_result = fp1.read()
    auth_key = json.loads(value_result).get('Authorization', {})
    header = {"Authorization": auth_key}
    count = 1000
    date = "2022-12-01"
    cursor = 100
    url = f"https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results?count={count}&date={date}"
    result = requests.get(url, headers=header)
    print(result.text)



def main():
    with open("./resource/API_key.json", 'rt') as fp1:
        value_result = fp1.read()
    auth_key = json.loads(value_result).get('Authorization', {})
    header = {"Authorization": auth_key}
    count = 1000
    date = "2022-12-02"
    date = date_range(date, datetime.strftime(datetime.now(), "%Y-%m-%d"))
    print(date)
    for cube_date in date:
        url = f"https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results?count={count}&date={cube_date}"#&cursor={cursor}"
        result = requests.get(url, headers=header)
        print(result.text)
        data_dict = json.loads(result.text)
        print(data_dict)
        # black_count = 0
        # black_count_sucess = 0
        # add_cube_count_sucess = 0
        # add_cube_count = 0
        # black_sucess = 0
        # black_fail = 0
        # add_cube_sucess = 0
        # add_cube_fail = 0
        # for i in reversed(data_dict.get('cube_histories', {})):
        #     if i.get('character_name') == '오라웨푼':
        #         if i.get('cube_type') == '블랙 큐브':
        #             black_count += 1
        #             if i.get('item_upgrade_result') == '성공':
        #                 black_sucess += 1
        #                 black_count_sucess = black_count
        #             else:
        #                 black_fail += 1
        #         elif i.get('cube_type') == '에디셔널 큐브':
        #             add_cube_count += 1
        #             if i.get('item_upgrade_result') == '성공':
        #                 add_cube_sucess += 1
        #                 add_cube_count_sucess = add_cube_count
        #             else:
        #                 add_cube_fail += 1

        print(black_count_sucess, black_sucess, black_fail, add_cube_count_sucess, add_cube_sucess, add_cube_fail)

if __name__ == '__main__':
    api_test()
    #main()