from analyze import *

comments = create_comments()
create_dic(comments)
tendency = create_tendency(comments)
items = sort_data(tendency)
print_result(items)