import requests, json
import pandas as pd
from datetime import timedelta, datetime


cube_history_column_list_info = ["id",
                                "character_name",
                                "world_name",
                                "create_date",
                                "cube_type",
                                "item_upgrade_result",
                                "miracle_time_flag",
                                "item_equip_part",
                                "item_level",
                                "target_item",
                                "potential_option_grade",
                                "additional_potential_option_grade",
                                "upgradeguarantee",
                                "upgradeguaranteecount"
]
# 조회하고자 하는 일자 (YYYY-MM-DD) *2022년 11월 25일부터 조회 가능
def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]

    return dates

# 큐브 사용 내역 조회 * date, cursor 중 하나만 입력 가능
def inquery(api_key, count, date, cursor, result_df):

    if cursor == "":
        url = f"https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results?count={count}&date={date}"
    else :
        url = f"https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results?count={count}&cursor={cursor}"
    result = requests.get(url, headers=api_key)
    data_dict = json.loads(result.text)

    cube_histories = data_dict.get("cube_histories")
    next_cursor = data_dict.get("next_cursor")

    for i in range(len(cube_histories)):
        inquery_result = data_dict.get("cube_histories")[i]

        cube_history_val_list_info = []
        for key in cube_history_column_list_info:
            cube_history_val_list_info.append(inquery_result.get(key))
        cube_history_column_list_options, cube_history_val_list_options = parse_history(inquery_result)

        history_column_list_temp = cube_history_column_list_info + cube_history_column_list_options
        history_val_list_temp = cube_history_val_list_info + cube_history_val_list_options
        history_dict = dict(zip(history_column_list_temp, history_val_list_temp))

        history_df = pd.DataFrame([history_dict])

        result_df = pd.concat([result_df, history_df], ignore_index=True)

    if next_cursor == "":
        return result_df

    return inquery(api_key, count, date, next_cursor, result_df)


def parse_history(inquery_result):
    history = inquery_result

    history_column_list = []
    history_val_list = []

    def options(column_name, options, options_len):

        options_val_list = []

        if options_len < 3:
            options_column_list = \
                [column_name + '_value_first',
                 column_name + '_grade_first',
                 column_name + '_value_second',
                 column_name + '_value_second']
            for option in options:
                for val in option.values():
                    options_val_list.append(val)
        else:
            options_column_list = \
                [column_name + '_value_first',
                 column_name + '_grade_first',
                 column_name + '_value_second',
                 column_name + '_grade_second',
                 column_name + '_value_third',
                 column_name + '_grade_third']
            for option in options:
                for val in option.values():
                    options_val_list.append(val)
        return options_column_list, options_val_list

    #큐브 돌리기 전 잠재
    if history.get("before_potential_options"):
        history_column_list += options("before_potential_options", history.get("before_potential_options"), len(history.get("before_potential_options")))[0]
        history_val_list += options("before_potential_options", history.get("before_potential_options"), len(history.get("before_potential_options")))[1]
    #큐브 돌리기 전 에잠
    if history.get("before_additional_potential_options"):
        history_column_list += options("before_additional_potential_options", history.get("before_additional_potential_options"), len(history.get("before_additional_potential_options")))[0]
        history_val_list += options("before_additional_potential_options", history.get("before_additional_potential_options"), len(history.get("before_additional_potential_options")))[1]
    #큐브 돌린 후 잠재
    if history.get("after_potential_options(history"):
        history_column_list += options("after_potential_options(history", history.get("after_potential_options"), len(history.get("after_potential_options")))[0]
        history_val_list += options("after_potential_options(history", history.get("after_potential_options"), len(history.get("after_potential_options")))[1]
    #큐브 돌린 후 에잠
    if history.get("after_additional_potential_options"):
        history_column_list += options("after_additional_potential_options", history.get("after_additional_potential_options"), len(history.get("after_additional_potential_options")))[0]
        history_val_list += options("after_additional_potential_options", history.get("after_additional_potential_options"), len(history.get("after_additional_potential_options")))[1]

    return history_column_list, history_val_list


def main():
    with open("./resource/API_key.json", 'rt') as fp1:
        value_result = fp1.read()
    auth_key = json.loads(value_result).get('Authorization', {})
    api_key = {"Authorization": auth_key}
    count = input("횟수(10 ~ 1000): ") #조회하고자 하는 횟수
    start_date = input("시작 날짜(YYYY-MM-DD): ") #조회하고자 하는 시작일
    end_date = input("종료 날짜(YYYY-MM-DD): ") #조회하고자 하는 종료일

    date = date_range(start_date, end_date)
    cursor = ""
    result_df = pd.DataFrame()
    inquery_df = pd.DataFrame()

    file_path = f"./resource/{start_date}_{end_date}_{count}.csv"

    for cube_date in date:
        inquery_df = pd.concat([inquery_df, inquery(api_key, count, cube_date, cursor, result_df)], ignore_index=True)

    inquery_df.to_csv(file_path, sep='|', na_rep='NaN', index=False)



if __name__ == '__main__':
    main()

