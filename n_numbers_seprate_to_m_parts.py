#!/usr/bin/env python
#encoding: utf-8

import time
from numpy import random
from duplicate_avltree import DuplicateAVLTree

def calc_best_group_for_list(delta, list):
    if delta <= 0 or not len(list):
        return ([], None)
    delta_list = [abs(item - delta) for item in list]
    min_delta = min(delta_list)
    min_delta_index = delta_list.index(min_delta)
    if min_delta <= delta:
        new_list = list.copy()
        new_list.pop(min_delta_index)
        (min_elem_ary, result_delta) = calc_best_group_for_list(min_delta, new_list)
        combined_min_elem_ary = [list[min_delta_index]]
        combined_min_elem_ary.extend(min_elem_ary);
        return (combined_min_elem_ary, result_delta)
    elif list[min_delta_index] > 2 * delta:
        return ([], None)
    else:
        # 如果选择这个大数结束， 最后的delta定格在min_delta
        #if select the bigger number then searh finished, and the last delta is min_delta
        option_end_delta = min_delta
        #如果还要尝试小数字
        #try smaller number
        new_list = [item for item in list if item < delta]
        (second_min_delta_ary, second_delta) = calc_best_group_for_list(delta, new_list)
        if second_min_delta_ary and second_delta < option_end_delta:
            return (second_min_delta_ary, second_delta)
        else:
            return ([list[min_delta_index]], min_delta)


def calc_best_group(delta, dataset):
    if delta <= 0 or not dataset:
        return ([], delta)
    delta_set = set([(abs(item - delta), item) for item in dataset])
    min_item_delta_data = min(delta_set, key=lambda x: x[0])
    min_delta = min_item_delta_data[0]
    min_item = min_item_delta_data[1]
    if min_item <= delta:
        new_data_set = dataset.copy()
        new_data_set.remove(min_item)
        (min_elem_ary, result_delta) = calc_best_group(min_delta, new_data_set)
        combined_min_elem_ary = [min_item,]
        combined_min_elem_ary.extend(min_elem_ary);
        return (combined_min_elem_ary, result_delta)
    elif min_item > 2 * delta:
        return ([], delta)
    else:
        # 如果选择这个大数结束， 最后的delta定格在min_delta
        #if select the bigger number then searh finished, and the last delta is min_delta
        option_end_delta = min_delta
        #如果还要尝试小数字
        #try smaller number
        new_data_set = set([item for item in dataset if item < delta])
        (second_min_delta_ary, second_delta) = calc_best_group(delta, new_data_set)
        if second_min_delta_ary and second_delta < option_end_delta:
            return (second_min_delta_ary, second_delta)
        else:
            return ([min_item], min_delta)

def calc_best_group_for_tree(delta, data_node, tree):
    if delta <= 0 or not data_node:
        return ([], delta)
    (bigger_or_equal_node, smaller_node) = tree.find_closest_node_in_subtree(data_node, delta)
    if smaller_node:
        option_min_delta = delta - smaller_node.key
    if bigger_or_equal_node:
        option_bigger_delta = bigger_or_equal_node.key - delta
    if bigger_or_equal_node is None:
        pre_sub_tree_node = tree.get_pre_sub_tree(smaller_node, option_min_delta)
        combined_min_elem_ary = [smaller_node]
        if pre_sub_tree_node == smaller_node:
            pre_node = tree.get_pre_node(smaller_node)
            while pre_node and pre_node.key < option_min_delta:
                option_min_delta = option_min_delta - pre_node.key
                combined_min_elem_ary.append(pre_node)
                pre_node = tree.get_pre_node(pre_node)
            pre_sub_tree_node = tree.get_pre_sub_tree(pre_node, option_min_delta)

        ret = calc_best_group_for_tree(option_min_delta,
                                       pre_sub_tree_node, tree)
        (result_node_ary, option_min_final_delta) = ret
        combined_min_elem_ary.extend(result_node_ary)
        return (combined_min_elem_ary, option_min_final_delta,)
    elif smaller_node is None:
        if option_bigger_delta < delta:
            return ([bigger_or_equal_node], bigger_or_equal_node.key - delta, )
        else:
            return ([], delta)
    elif bigger_or_equal_node.key == delta:
        return ([bigger_or_equal_node], 0)
    else:
        option_bigger_final_delta =  bigger_or_equal_node.key - delta
        pre_sub_tree_node = tree.get_pre_sub_tree(smaller_node, option_min_delta)
        combined_min_elem_ary = [smaller_node]
        if pre_sub_tree_node and pre_sub_tree_node != smaller_node :
            (result_node_ary, option_min_final_delta) = calc_best_group_for_tree(option_min_delta,
                                                                                 pre_sub_tree_node, tree)

            combined_min_elem_ary.extend(result_node_ary)
        else:
            option_min_final_delta = option_min_delta
        if option_min_final_delta < option_bigger_final_delta:
            return (combined_min_elem_ary, option_min_final_delta)
        else:
            for node in combined_min_elem_ary:
                node.reset_usage()
            return ([bigger_or_equal_node], option_bigger_final_delta)


for i in range(100):
    #number_list = [28, 25, 19, 18, 10, 9, 6, 4, 3, 1]
    number_list = list(random .randint(low=1, high=1000, size=1000))
    #number_list = list(set(random .randint(low = 1, high=100000, size=10000)))
    #number_list = list(set(random .randint(low = 1, high=100, size=30)))
    number_list.extend([1,1,1])
    number_list.sort()

    #group_cnt = 3
    group_cnt = 100
    average = sum(number_list) / group_cnt
    failed = False

    try:
        print('average=', average)
        start = time.time()
        numbers_tree = DuplicateAVLTree(number_list)

        mn = numbers_tree.max_node()
        tree_grouped_number_ary_list = []
        for group_index in range(group_cnt):
            cur_group = []
            max_node = numbers_tree.max_node()
            group_first_node = max_node
            cur_group.append(group_first_node)
            numbers_tree.remove_node(max_node)
            if group_index == group_cnt - 1:
                print('last index..., sum=',sum(numbers_tree.inorder(numbers_tree.rootNode)))

            (left_group_nodes, delta) = calc_best_group_for_tree(average - group_first_node.key, numbers_tree.rootNode, numbers_tree)
            cur_group.extend(left_group_nodes)
            group_numbers = [item.key for item in cur_group]
            tree_grouped_number_ary_list.append(group_numbers)
            print('group_index=', group_index,',group_numbers=', group_numbers, ',sum=', sum(group_numbers))
            for node in left_group_nodes:
                numbers_tree.remove_node(node)

        end = time.time()
        print('tree arange time used:', end - start)
        continue
        num_list = list(number_list)
        average1 = sum(number_list) / group_cnt
        assert average == average1
        group_numbers_list = []

        start_set = time.time()
        for group_index in range(group_cnt):
            if not len(num_list):
                print('group failed...')
                break
            first_number = max(num_list)
            num_list.remove(first_number)
            group_numbers = [first_number]
            if first_number < average:
                left_group_numbers, delta = calc_best_group_for_list(average - first_number, num_list)
                #group_numbers, delta = calc_best_group(average - first_number, number_dataset)
                if left_group_numbers:
                    for elem in reversed(left_group_numbers):
                        num_list.remove(elem)
                group_numbers.extend(left_group_numbers)
            group_numbers_list.append(group_numbers)
            print('group index:%d, group_numbers=%s, sum=%d, percent=%.2lf%%'% (group_index, str(group_numbers), sum(group_numbers), (group_index + 1.0)*100 / group_cnt))
            if sum(group_numbers) != sum(tree_grouped_number_ary_list[group_index]):
                failed = True
                break
                # raise Exception('exception ocured...')
            #assert group_numbers == tree_grouped_number_ary_list[group_index]
        if failed:
            continue
        end_set = time.time()
        print('list arage time used:', end_set - start_set)

        number_dataset = set(number_list)
        average1 = sum(number_list) / group_cnt
        assert average == average1
        group_numbers_set = []

        start_set = time.time()
        for group_index in range(group_cnt):
            if not len(number_dataset):
                print('group failed...')
                break
            first_number = max(number_dataset)
            number_dataset.remove(first_number)
            group_numbers = [first_number]
            if first_number < average:
                left_group_numbers, delta = calc_best_group(average - first_number, number_dataset)
                if left_group_numbers:
                    for elem in reversed(left_group_numbers):
                        number_dataset.remove(elem)
                group_numbers.extend(left_group_numbers)
            group_numbers_set.append(group_numbers)
            print('group index:%d, group_numbers=%s, sum=%d, percent=%.2lf%%'% (group_index, str(group_numbers), sum(group_numbers), (group_index + 1.0)*100 / group_cnt))
            assert group_numbers == tree_grouped_number_ary_list[group_index]
        end_set = time.time()
        print('list arage time used:', end_set - start_set)
    except Exception as e:
       print('e = ', e)

#print('ret=', ret)