import jieba

positive_seeds = ()
negative_seeds = ()
exclude = "，。！？：”@#￥%……&*（）{}【】；’‘~,\"～"

def sep_data():
    #将正向负向评论分离
    file = open("外卖评论.csv", "r", encoding="utf-8").readlines()
    positive = ""
    negative = ""

    for line in file:
        if line[0] == '1':
            positive += line[2:].replace("\n", "")
        else:
            negative += line[2:].replace("\n", "")

    return positive, negative

def sort_data(comments):
#返回排好从大到小序的统计数据
    lis_comments = jieba.lcut(comments)
    counts = {}
    for word in lis_comments:
        if (word in positive_seeds) or (word in negative_seeds) or (word in exclude):
            continue
        counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(reverse=True, key=lambda x: x[1])
    return items

def main():
    all_comments = sep_data()
    positive_comments = all_comments[0]
    negative_comments = all_comments[1]
    sorted_positive_comments = sort_data(positive_comments)
    sorted_negative_comments = sort_data(negative_comments)

    print("{:=^20}".format("positive"))
    for i in range(0, 50):
        print("{: ^10}{: ^10}".format(sorted_positive_comments[i][0], sorted_positive_comments[i][1]))

    print("{:=^20}".format("negative"))
    for i in range(0, 50):
        print("{: ^10}{: ^10}".format(sorted_negative_comments[i][0], sorted_negative_comments[i][1]))

main()
