#!/usr/bin/env python

"""
The pipeline of the script:
1/ It loads a JSON with the book project's details.
2/ Reads the manuscript, be it a single document or multiple documents.
3/ Transforms the manuscript's content into an object.
4A/ Analyzes the object for the desired stats or search results.
4B/ Transforms the object into the desired output format.
"""

import json
import sys
import docx2txt

## tato část načte JSON s informacemi o knize

with open(sys.argv[1], "r", encoding="utf-8") as project:
    project = project.read()
    project = json.loads(project)

chapters = project["files"]
first_mentions = project["first_mentions"]

try:
    headerLines = project["header_lines"]
except:
    headerLines = 1
try:
    divider = project["subsection_divider"]
except:
    divider = "***"

bookChapters = []
bookParagraphs = []

## tato část načte jednotlivé kapitoly

for chapter in chapters:
    chapterText = docx2txt.process(chapter)
    chapterParagraphs = chapterText.splitlines()
    while("" in chapterParagraphs):
        chapterParagraphs.remove("")
    bookChapters.append(chapterText)
    bookParagraphs.append(chapterParagraphs)

## tato funkce simuluje listování knihou
    
def glimpse(bookParagraphs):
    for x in bookParagraphs:
        print("\n".join(x[0:headerLines]))
        print("\n")

## tato funkce vypisuje první odstavce kapitol
        
def firstParagraphs(bookParagraphs):
    for x in bookParagraphs:
        print(x[headerLines][:200])
        print("\n")

## tato funkce vypisuje poslední odstavce kapitol
        
def lastParagraphs(bookParagraphs):
    for x in bookParagraphs:
        print(x[-1][-200:])
        print("\n")

## tato funkce vypisuje první zmínky jmen i s okolím
        
def firstMentions(bookParagraphs):
    for x in bookParagraphs:
        namesFound = []
        print(x[0] + "\n")
        for name in first_mentions:
            for paragraph in x[headerLines:]:
                if name in paragraph:
                    if name not in namesFound:
                        print(name + ": " + paragraph + "\n")
                        namesFound.append(name)

## tato funkce fulltextově hledá ve všech kapitolách
                        
def findEverything(bookParagraphs, search):
    count = 0
    for x in bookParagraphs:
        for paragraph in x:
            if search in paragraph:
                print(x[0])
                print(paragraph)
                count = count + 1
    print (search + ": found " + str(count) + " times")

## tato funkce vizualizuje délku kapitol
    
def chapterLenght(bookChapters):
    longestChapter = max(bookChapters, key = len)
    longestChapter = len(longestChapter)
    ratio = 40 / longestChapter
    for x in bookChapters:
        header = x.splitlines()[0]
        chapterLenght = len(x)
        chapterLenght = int(chapterLenght * ratio)
        paragraphsBlocks = ""
        for y in range(0, chapterLenght):
            paragraphsBlocks = paragraphsBlocks + "¶"
        print(header)
        print(paragraphsBlocks, "\n")

## tato funkce vizualizuje délku podkapitol
        
def subChapterLenght(bookParagraphs):
    for x in bookParagraphs:
        print(x[0])
        joinedChapter = "\n".join(x)
        subchapters = joinedChapter.split("***")
        for y in subchapters:
            a = y.splitlines()
            while("" in chapterParagraphs):
                a.remove("")
            paragraphs = len(a)
            paragraphsBlocks = ""
            for z in range(0, paragraphs):
                paragraphsBlocks = paragraphsBlocks + "¶"
            print(paragraphsBlocks)
        print("\n")

## tato funkce počítá celkový rozsah
        
def totalLenght(bookChapters):
    lenght = 0
    for x in bookChapters:
        lenght = lenght + len(x)
    print("Total characters: " + str(lenght))

## zde skript čte pokyn z příkazové řádky a volá příslušnou funkci
    
if sys.argv[2] == "glimpse":
    glimpse(bookParagraphs)

if sys.argv[2] == "chapters":
    chapterLenght(bookChapters)

if sys.argv[2] == "subchapters":
    subChapterLenght(bookParagraphs)

if sys.argv[2] == "search":
    search = sys.argv[3]
    findEverything(bookParagraphs, search)

if sys.argv[2] == "totallenght":
    totalLenght(bookChapters)
