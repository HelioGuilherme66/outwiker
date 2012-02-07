#!/usr/bin/python
# -*- coding: UTF-8 -*-

def parseTagsList (tagsString):
    """
    Преобразовать строку тегов, разделенных запятой, в список
    """
    tags = [tag.strip() for tag in tagsString.split (",") 
            if len (tag.strip()) > 0]

    return tags


def getTagsString (tags):
    """
    Получить строку тегов
    """
    result = u""
    count = len (tags)

    for n in range (count):
        result += tags[n]
        if n != count - 1:
            result += ", "

    return result


def removeTag (page, tag):
    """
    Удалить тег из страницы
    """
    pageTags = [pagetag.lower() for pagetag in page.tags]

    taglower = tag.lower()
    while taglower in pageTags:
        pageTags.remove (taglower)

    page.tags = pageTags


def appendTag (page, tag):
    pageTags = page.tags[:]
    pageTags.append (tag)
    page.tags = pageTags


def appendTagsList (page, tagslist):
    pageTags = page.tags[:]
    pageTags.extend (tagslist)
    page.tags = pageTags


def tagBranch (parentPage, tags):
    """
    Добавить теги к ветке, начиная с родительской страницы
    """
    # map (lambda tag: appendTag (parentPage, tag), tags)
    appendTagsList (parentPage, tags)
    map (lambda child: tagBranch (child, tags), parentPage.children)

