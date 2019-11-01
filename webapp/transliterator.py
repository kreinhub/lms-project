import os

def latinizator(letter, dic):
    for i, j in dic.items():
        letter = letter.replace(i, j)
    return letter

def get_slug(words):
    legend = {
    'а':'a',
    'б':'b',
    'в':'v',
    'г':'g',
    'д':'d',
    'е':'e',
    'ё':'yo',
    'ж':'zh',
    'з':'z',
    'и':'i',
    'й':'y',
    'к':'k',
    'л':'l',
    'м':'m',
    'н':'n',
    'о':'o',
    'п':'p',
    'р':'r',
    'с':'s',
    'т':'t',
    'у':'u',
    'ф':'f',
    'х':'h',
    'ц':'ts',
    'ч':'ch',
    'ш':'sh',
    'щ':'shch',
    'ъ':'y',
    'ы':'y',
    'ь':"'",
    'э':'e',
    'ю':'yu',
    'я':'ya',

    'А':'A',
    'Б':'B',
    'В':'V',
    'Г':'G',
    'Д':'D',
    'Е':'E',
    'Ё':'Yo',
    'Ж':'Zh',
    'З':'Z',
    'И':'I',
    'Й':'Y',
    'К':'K',
    'Л':'L',
    'М':'M',
    'Н':'N',
    'О':'O',
    'П':'P',
    'Р':'R',
    'С':'S',
    'Т':'T',
    'У':'U',
    'Ф':'F',
    'Х':'H',
    'Ц':'Ts',
    'Ч':'Ch',
    'Ш':'Sh',
    'Щ':'Shch',
    'Ъ':'Y',
    'Ы':'Y',
    'Ь':"'",
    'Э':'E',
    'Ю':'Yu',
    'Я':'Ya',
    }

    words = words.replace("ь", "").replace(",", "").replace("*", "").replace("@","").replace("?", "").replace('"', '').replace("_", "-")

    translit = ""
    for line in words:
        translit += latinizator(line, legend)
        # print(latinizator(line, legend), end='')

    slug = sluger(translit)
    return slug

def sluger(words):
    match_symb_list = ["(", ":", "-", "."]
    result = []
    empty_result = True
    for symb in match_symb_list:
        if symb in words:
            if symb == "-" or symb == ".":
                idx = words.index(symb)
                result.append(words[:idx])
                empty_result = False
            elif symb == ":":
                idx = words.index(symb)
                result.append(words[:idx])
                empty_result = False                
            elif symb == "(":
                idx = words.index(symb)
                result.append(words[:idx-1])
                empty_result = False                

    if empty_result:
        result = words.replace(" ", "-")
        return result

    result_words = result[-1].replace(" ", "-")
    return result_words

    

    # try:
    #     return result[-1]
    # except IndexError:
    #     return result

    # for symb in match_symb_list:
    #     try:
    #         if symb == "-" or symb == ".":
    #             idx = words.index(symb)
    #             cutted_words = words[:idx]
    #             words = cutted_words.replace(" ", "-")
    #             return words

    #         idx = words.rindex(symb)
    #         words = words.replace(" ", "-")
    #         if symb == "(" or symb == "-":
    #             return words[:idx-1]
    #         return words[:idx]
    #     except ValueError:
    #         continue

    # words = words.replace(" ", "-")
    # return words



if __name__ == "__main__":
    words = input("Введи русское предложение: ")
    print(get_slug(words))