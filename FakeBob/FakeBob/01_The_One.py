import random

# def func01():
#     for i in shuffle1:
#         if i



card_list = ["梅花","黑桃","方块","红心"]
card_number = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
all_card_list = [[color,num] for color in card_list for num in card_number]

shuffle = random.shuffle(all_card_list)

shuffle1 = all_card_list[0],all_card_list[1],all_card_list[2]



