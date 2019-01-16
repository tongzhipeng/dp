#!/usr/bin/env python
#encoding: utf-8

import time

def calc_best_group(delta, list):
    if delta <= 0 or not list:
        return (None, None)
    delta_list = [abs(item - delta) for item in list]
    min_delta = min(delta_list)
    min_delta_index = delta_list.index(min_delta)
    if list[min_delta_index] <= delta:
        new_list = list.copy()
        new_list.pop(min_delta_index)
        (min_elem_ary, result_delta) = calc_best_group(min_delta, new_list)
        if not min_elem_ary:
            return ([list[min_delta_index], ], min_delta)
        else:
            combined_min_elem_ary = [list[min_delta_index]]
            combined_min_elem_ary.extend(min_elem_ary);
            return (combined_min_elem_ary, result_delta)

    elif list[min_delta_index] > 2 * delta:
        return (None, None)
    else:
        # 如果选择这个大数结束， 最后的delta定格在min_delta
        #if select the bigger number then searh finished, and the last delta is min_delta
        option_end_delta = min_delta
        #如果还要尝试小数字
        #try smaller number
        new_list = [item for item in list if item < delta]
        (second_min_delta_ary, second_delta) = calc_best_group(delta, new_list)
        if second_min_delta_ary and second_delta < option_end_delta:
            return (second_min_delta_ary, second_delta)
        else:
            return ([list[min_delta_index]], min_delta)

start = time.time()
number_list = [28, 25, 19, 18, 10, 9, 6, 4, 3, 1]

group_cnt = 5
average = sum(number_list) / group_cnt
print('average=', average)
group_numbers_list = []
for group_index in range(group_cnt):
    first_number = max(number_list)
    number_list.remove(first_number)
    group_numbers = []
    if first_number < average:
        group_numbers, delta = calc_best_group(average - first_number, number_list)
        for elem in reversed(group_numbers):
            number_list.remove(elem)
    group_numbers.insert(0, first_number)
    group_numbers_list.append(group_numbers)
    print('group_numbers=', group_numbers)
end = time.time()
print('time used:', end - start)