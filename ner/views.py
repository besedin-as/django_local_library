# coding=utf-8
from django.shortcuts import render_to_response, render, redirect
from django.views.decorators.csrf import csrf_exempt
from nermaster.nera import *
import random
import glob


@csrf_exempt
def index(request):
    texts = get_texts()
    return render_to_response('index.html', {'texts': texts})


@csrf_exempt
def add_text(request):
    if request.method == 'POST':
        text = request.POST['text']
        install()
        dicti = print_predict(text)
        print(dicti)
        for dict in dicti:
            if dict['tag'][0:2] == 'B-':
                dict['tag'] = dict['tag'][2:len(dict['tag'])]
            elif dict['tag'][0:2] == 'I-':
                dict['tag'] = dict['tag'][2:len(dict['tag'])]

        tags = []
        unic_tag = []
        i = 0
        for dict in dicti:
            if dict['tag'] not in unic_tag and dict['tag'] != '':
                unic_tag.append(dict['tag'])
                if i > 9:
                    color = '#%02X%02X%02X' % (r(), r(), r())
                else:
                    color = get_color_list()[i]
                tags.append(Tag(dict['tag'], color))
                i += 1

        return render(request, 'result.html', {'dicti': dicti, 'text': text, 'tags': tags})
    else:
        return redirect('/')


def r():
    return random.randint(0, 255)


def get_color_list():
    return ['#00BFFF', '#7CFC00', '#EE82EE', '#6A5ACD', '#F4A460',
            '#FF6347', '#FFA500', '#FFFF00', '#F08080', '#A9A9A9']


def get_texts():
    texts = []
    for i in range(0, len(glob.glob('texts/*.txt'))):
        file_name = glob.glob('texts/*.txt')[i]
        f = open(file_name)
        title = f.readline()
        text = ''
        line = f.readline()
        while line:
            text += line+"\n"
            line = f.readline()
        f.close()
        texts.append(Text(title, text))
    return texts


class Tag:
    def __init__(self, tag, color):
        self.tag = tag
        self.color = color


class Text:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text



