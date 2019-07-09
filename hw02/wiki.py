from requests import get
import re
def get_link(topic):
    link = "https://ru.wikipedia.org/wiki/" + topic.capitalize()
    return link

def get_topic_page(topic):
    link = get_link(topic)
    html = get(link).text
    return html

def get_topic_text(topic):
    html_content = get_topic_page(topic)
    words = re.findall("[а-яА-Я]{3,}",html_content)
    return words

def get_common_words(topic):
    words_list = get_topic_text(topic)
    rate={}
    for word in words_list:
        if word in rate:
            rate[word]+=1
        else:
            rate[word]=1
    rate_list = list(rate.items())
    rate_list.sort(key = lambda x :-x[1])

    return rate_list

def visualize_common_words(topic):
    words = get_common_words(topic)
    for w in words[0:10]:
        print(f'{w[0]} встречается {w[1]} раз')



list1 = visualize_common_words(topic)
print(list1)
#print(len(list1))
