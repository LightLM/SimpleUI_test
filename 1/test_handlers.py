import json
import os
from ru.travelfood.simple_ui import NoSQL as noClass
from PIL import Image
import datetime

queue_birds = []


def init(hashMap, _files=None, _data=None):
    SW_Birds = noClass("birds_nosql")
    finish_log = noClass("birds_log")
    return hashMap


def birds_on_start(hashMap, _files=None, _data=None):
    SW_Birds = noClass("birds_nosql")
    hashMap.put("mm_local", "")
    hashMap.put("mm_compression", "70")
    hashMap.put("mm_size", "65")

    list = {"customcards": {

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    'key': '@id_number',
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {

                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@pic",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
                            "TextColor": "#DB7093",
                            "TextBold": True,
                            "TextItalic": False,
                            "BackgroundColor": "",
                            "width": "75",
                            "height": "75",
                            "weight": 0
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@id_number",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@color",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    }
    }

    query = SW_Birds.getallkeys()
    jkeys = json.loads(query)
    list["customcards"]["cardsdata"] = []
    # Чек списка
    # list["customcards"]["cardsdata"].append({"id_number": query})
    for i in jkeys:
        a = json.loads(SW_Birds.get(i))

        pic = ""
        if 'photo' in a:
            p = a['photo']
            if len(p) > 0:
                for jf in _files:
                    if jf['id'] == p[0]:
                        if os.path.exists(jf['path']):
                            pic = "~" + jf['path']
                        break
        list["customcards"]["cardsdata"].append(
            {"key": a["id"], "id_number": a['id'], 'color': a['color'], 'name': a['name'], 'pic': pic})
    # Тесты птиц
    # for n in range(10):
    #    list["customcards"]["cardsdata"].append(
    #        {"name": "Тестовая птица " + str(n), "key": n, "id_number_number": str(n), "color": str(n), "pictures": [],
    #         "pic": ""})

    hashMap.put("list", json.dumps(list))

    return hashMap


def birds_input(hashMap, _files=None, _data=None):
    global nom_id

    if hashMap.get("listener") == "btn_add":
        hashMap.put("name", "")
        hashMap.put("color", "")

        hashMap.put("photoGallery", json.dumps([]))

        nom_id = -1
        hashMap.put("ShowScreen", "Добавление")
    elif hashMap.get('listener') == 'CardsClick':
        hashMap = open_nom(hashMap, hashMap.get("selected_card_key"))

    return hashMap


def birds_record_input(hashMap, _files=None, _data=None):
    global nom_id
    if hashMap.get("listener") == "btn_save":

        hashMap, success = save_nom(hashMap)
        if success:
            hashMap.put("ShowScreen", "Птицы")

    elif hashMap.get("listener") == "photo":

        image_file = str(
            hashMap.get("photo_path"))

        image = Image.open(image_file)
        im = image.resize((500, 500))
        im.save(image_file)

        jphotoarr = json.loads(hashMap.get("photoGallery"))
        hashMap.put("photoGallery", json.dumps(jphotoarr))
        nom_id = 1


    elif hashMap.get(
            "listener") == "gallery_change":
        if hashMap.containsKey("photoGallery"):
            jphotoarr = json.loads(hashMap.get("photoGallery"))
            hashMap.put("photoGallery", json.dumps(jphotoarr))

    return hashMap


def birds_record_on_start(hashMap, _files=None, _data=None):
    hashMap.put("mm_local", "")
    hashMap.put("mm_compression", "70")
    hashMap.put("mm_size", "65")

    hashMap.put("fill_name", json.dumps({"hint": "Название птицы", "default_text": hashMap.get("name")}))
    hashMap.put("fill_color", json.dumps({"hint": "Цвет птицы", "default_text": hashMap.get("color")}))

    return hashMap


def card_input(hashMap, _files=None, _data=None):
    global info
    global queue_birds
    SW_Birds = noClass("birds_nosql")
    if hashMap.get('listener') == 'btn_add_score':
        info['counter'] = str(int(info['counter']) + 1)
        SW_Birds.put('Object' + info['id'], json.dumps(info, ensure_ascii=False), True)

    hashMap.put('toast', json.dumps(queue_birds))
    if not 'Object' + info['id'] in queue_birds:
        queue_birds.append('Object' + info['id'])

    return hashMap


def card_on_start(hashMap, _files=None, _data=None):
    global info
    hashMap.put("mm_local", "")
    hashMap.put("mm_compression", "70")
    hashMap.put("mm_size", "65")
    list2 = {"customcards": {

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    'key': '@id_number',
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {

                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@pic",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "25",
                            "TextColor": "#DB7093",
                            "TextBold": True,
                            "TextItalic": False,
                            "BackgroundColor": "",
                            "width": "150",
                            "height": "150",
                            "weight": 0
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": '@id_number',
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@color",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    }
    }
    list2["customcards"]["cardsdata"] = []
    pic = ""
    if 'photo' in info:
        p = info['photo']
        if len(p) > 0:
            for jf in _files:
                if jf['id'] == p[0]:
                    if os.path.exists(jf['path']):
                        pic = "~" + jf['path']
                    break
    list2["customcards"]["cardsdata"].append(
        {"key": info["id"], "id_number": info['id'], 'color': info['color'], 'name': info['name'], 'pic': pic})
    hashMap.put("list2", json.dumps(list2))

    return hashMap


def open_nom(hashMap, key):
    global info
    SW_Birds = noClass("birds_nosql")
    jsinfo = json.loads(SW_Birds.get('Object' + key))
    info = jsinfo
    hashMap.put("ShowScreen", "Карточка птицы")
    hashMap.put('toast', json.dumps(info))
    return hashMap


def get_if_exist(hashMap, field):
    if hashMap.containsKey(field):
        res = hashMap.get(field)
    else:
        res = ""
    return res


def save_nom(hashMap):
    SW_Birds = noClass("birds_nosql")
    global nom_id
    if not hashMap.containsKey("name"):
        hashMap.put("toast", "Не указано наименование")
        return hashMap, False
    else:
        if len(hashMap.get("name")) == 0:
            hashMap.put("toast", "Не указано наименование")
            return hashMap, False
    if not hashMap.containsKey("color"):
        hashMap.put("toast", "Не указан цвет")
        return hashMap, False
    else:
        if len(hashMap.get("color")) == 0:
            hashMap.put("toast", "Не указан цвет")
            return hashMap, False
    jkeys = json.loads(SW_Birds.getallkeys())
    if len(jkeys) == 0:
        id = '0'
    else:
        id_mn = json.loads(SW_Birds.get(jkeys[-1]))['id']
        id = str(int(id_mn) + 1)
    if nom_id < 0:
        d = {'id': id, 'name': get_if_exist(hashMap, "name"), 'color': get_if_exist(hashMap, "color"), 'counter': '0'}
        SW_Birds.put('Object' + id, json.dumps(d, ensure_ascii=False), True)
    else:
        d = {'id': id, 'name': get_if_exist(hashMap, "name"), 'color': get_if_exist(hashMap, "color"),
             'photo': json.loads(hashMap.get("photoGallery")), 'counter': '0'}
        SW_Birds.put('Object' + id, json.dumps(d, ensure_ascii=False), True)

    return hashMap, True


def finish_on_start(hashMap, _files=None, _data=None):
    finish_log = noClass("birds_log")
    hashMap.put("mm_local", "")
    hashMap.put("mm_compression", "70")
    hashMap.put("mm_size", "65")

    list3 = {"customcards": {

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    'key': '@id_number',
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {

                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@pic",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
                            "TextColor": "#DB7093",
                            "TextBold": True,
                            "TextItalic": False,
                            "BackgroundColor": "",
                            "width": "125",
                            "height": "125",
                            "weight": 0
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@id_number",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@date",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@counter",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@color",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    }
    }
    query = finish_log.getallkeys()
    jkeys = json.loads(query)
    list3["customcards"]["cardsdata"] = []
    for i in jkeys[::-1]:
        a = json.loads(finish_log.get(i))
        hashMap.put('toast', finish_log.get(i))
        pic = ""
        if 'photo' in a:
            p = a['photo']
            if len(p) > 0:
                for jf in _files:
                    if jf['id'] == p[0]:
                        if os.path.exists(jf['path']):
                            pic = "~" + jf['path']
                        break
        list3["customcards"]["cardsdata"].append(
            {"date": i, "id_number": a['id'], 'color': a['color'], 'name': a['name'], 'pic': pic,
             'counter': a['counter']})

    hashMap.put("list3", json.dumps(list3))

    return hashMap


def finish_input(hashMap, _files=None, _data=None):
    global queue_birds
    SW_Birds = noClass("birds_nosql")
    finish_log = noClass("birds_log")
    if hashMap.get("listener") == "btn_plus":
        for i in queue_birds:
            inf = json.loads(SW_Birds.get(i))
            if 'photo' in inf:
                d = {'id': inf['id'], 'name': inf['name'], 'color': inf['color'],
                     'counter': inf['counter'],
                     'photo': inf['photo']}
                finish_log.put(str(datetime.datetime.now()), json.dumps(d, ensure_ascii=False), True)
            else:
                d = {'id': inf['id'], 'name': inf['name'], 'color': inf['color'], 'counter': inf['counter']}
                finish_log.put(str(datetime.datetime.now()), json.dumps(d, ensure_ascii=False), True)
        else:
            queue_birds = []
    hashMap.put('toast', finish_log.getallkeys())
    return hashMap
