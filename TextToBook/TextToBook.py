#### Text To Book ####
# Filter for MCEdit by jgierer12, suggested by MasterM64

# Unescape HTML Entities from http://effbot.org/zone/re-sub.htm#unescape-html
import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
 # End Unescape HTML Entities

from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import TAG_Int_Array
from pymclevel import TAG_Float
from pymclevel import TAG_Long
import mceutils

try:
    import win32ui
except:
    pass

from mcplatform import askOpenFile

import zipfile
from functools import partial

displayName = "Text to Book"

inputs = [
    (
        ("Text Options", "title"),
        ("Convert", ("string", "value=n/a")),
        ("to a book (\"n/a\" for GUI File selector)", "label"),
        ("", "label"),
        ("Convert text bigger than", 12),
        ("pt to", "label"),
        (u"\u00b7 fullwidth characters", True),
        (u"\u00b7 uppercase", True),
        ("", "label"),
        ("Append", ("string", "value=PTO")),
        ("to the end of each page", True),
        ("but the last one", True),
        ("", "label"),
        ("Allow splitting a single document page", "label"),
        ("into multiple minecraft pages", True),
        ("", "label"),
        ("Make highlighted text obfuscated", True),
    ),
    (
        ("Book Options", "title"),
        ("Output to", ("Book Item Entity", "Book Item in Chest", "Give Book Command Block")),
        ("", "label"),
        ("Make", ("string", "value=Notch")),
        ("the author of the book", False),
        ("", "label"),
        ("Use the file name", ("without extension", "with extension")),
        ("as the book title (Will be overwritten by a Custom Title)", "label"),
        ("", "label"),
        ("Use", ("string", "value=Custom Book Title")),
        ("as the book title", False),
    ),
]

# Character widths in px for default Minecraft font
characterWidths = {
    " ": 4,
    "!": 2,
    "\"": 5,
    "#": 6,
    "$": 6,
    "%": 6,
    "&": 6,
    "'": 3,
    "": 5,
    "": 5,
    "*": 5,
    "+": 6,
    ",": 2,
    "-": 6,
    ".": 2,
    "/": 6,
    "0": 6,
    "1": 6,
    "2": 6,
    "3": 6,
    "4": 6,
    "5": 6,
    "6": 6,
    "7": 6,
    "8": 6,
    "9": 6,
    ":": 2,
    ";": 2,
    "<": 5,
    "=": 6,
    ">": 5,
    "?": 6,
    "@": 7,
    "A": 6,
    "B": 6,
    "C": 6,
    "D": 6,
    "E": 6,
    "F": 6,
    "G": 6,
    "H": 6,
    "I": 4,
    "J": 6,
    "K": 6,
    "L": 6,
    "M": 6,
    "N": 6,
    "O": 6,
    "P": 6,
    "Q": 6,
    "R": 6,
    "S": 6,
    "T": 6,
    "U": 6,
    "V": 6,
    "W": 6,
    "X": 6,
    "Y": 6,
    "Z": 6,
    "[": 4,
    "\\": 6,
    "]": 4,
    "^": 6,
    "_": 6,
    "`": 0,
    "a": 6,
    "b": 6,
    "c": 6,
    "d": 6,
    "e": 6,
    "f": 5,
    "g": 6,
    "h": 6,
    "i": 2,
    "j": 6,
    "k": 5,
    "l": 3,
    "m": 6,
    "n": 6,
    "o": 6,
    "p": 6,
    "q": 6,
    "r": 6,
    "s": 6,
    "t": 4,
    "u": 6,
    "v": 6,
    "w": 6,
    "x": 6,
    "y": 6,
    "z": 6,
    "{": 5,
    "|": 2,
    "}": 5,
    "~": 7
}

# Minecraft color codes
colorCodes = {
    (0, 0, 0): "0",
    (0, 0, 170): "1",
    (0, 170, 0): "2",
    (0, 170, 170): "3",
    (170, 0, 0): "4",
    (170, 0, 170): "5",
    (255, 170, 0): "6",
    (170, 170, 170): "7",
    (85, 85, 85): "8",
    (85, 85, 255): "9",
    (85, 255, 85): "a",
    (85, 255, 255): "b",
    (255, 85, 85): "c",
    (255, 85, 255): "d",
    (255, 255, 85): "e",
    (255, 255, 255): "f"
}

########## Fast data access by SethBling ##########
from pymclevel import ChunkNotPresent
GlobalChunkCache = {}
GlobalLevel = None


def getChunk(x, z):
    global GlobalChunkCache
    global GlobalLevel
    chunkCoords = (x >> 4, z >> 4)
    if chunkCoords not in GlobalChunkCache:
        try:
            GlobalChunkCache[chunkCoords] = GlobalLevel.getChunk(x >> 4, z >> 4)
        except ChunkNotPresent:
            return None

    return GlobalChunkCache[chunkCoords]


def blockAt(x, y, z):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    return chunk.Blocks[x % 16][z % 16][y]


def dataAt(x, y, z):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    return chunk.Data[x % 16][z % 16][y]


def tileEntityAt(x, y, z):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    return chunk.tileEntityAt(x, y, z)


def setBlockAt(x, y, z, block):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    chunk.Blocks[x % 16][z % 16][y] = block


def setDataAt(x, y, z, data):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    chunk.Data[x % 16][z % 16][y] = data
########## End fast data access ##########


def perform(level, box, options):
    global GlobalLevel
    GlobalLevel = level

    filePath = options["Convert"]

    if filePath == "n/a":
        try:
            filePath = askOpenFile("Select *.txt or *.docx file to convert to Book...", defaults=False, suffixes=["txt", "docx"])

        except:
            try:
                openFile = win32ui.CreateFileDialog(1, None, None, 0, "All Files (*.*)|*.*|Text Files (*.txt)|*.txt|Word Files (*.docx)|*.docx|")
                openFile.DoModal()
                filePath = openFile.GetPathName()

            except:
                raise Exception("win32ui could not be imported! Please enter the file path manually.")

    fileName = filePath

    while "/" in fileName:
        fileName = fileName[fileName.find("/")+1:]

    fileExtension = fileName[fileName.find(".")+1:]

    if options["as the book title"]:
        bookTitle = options["Use"]

    else:
        bookTitle = fileName
        if options["Use the file name"] == "with extension":
            bookTitle += "." + fileExtension

    if filePath is None or fileName == "":
        raise Exception("Please select a file!")

    mceutils.showProgress("Generating Book", progressIter())

    totalText = decodeFile(filePath, fileExtension, options)

    makeBook(level, box, options, totalText, bookTitle)


def progressIter():
    yield "Depending on your file size, this process could take a while!"


def decodeFile(textFile, textFileExt, options):
    if textFileExt == "txt":
        return splitText(options, [[[open(textFile).read(), "left"]]])

    elif textFileExt == "docx":
        docxFile = zipfile.ZipFile(textFile)
        rawXML = docxFile.open("word/document.xml").read()

        tagText = ""
        currentType = "unknown"
        styles = False
        fullwidth = False
        uppercase = False

        rawText = [[[u"", "left"]]]

        documentPage = 0
        paragraphNumber = 0

        for letter in rawXML:

            if letter == "<":
                currentType = "tagOpen"
            elif letter == ">":
                currentType = "tagClose"

            if currentType == "tag":
                tagText += letter

            elif currentType == "tagOpen":
                currentType = "tag"

            elif currentType == "tagClose":

                currentType = "unknown"

                if tagText[:3] == "w:t":
                    currentType = "text"
                elif tagText[:3] == "w:i":
                    styles = True
                    rawText[documentPage][paragraphNumber][0] += u"\u00A7o"
                elif tagText[:3] == "w:b" and tagText != "w:body":
                    styles = True
                    rawText[documentPage][paragraphNumber][0] += u"\u00A7l"
                elif tagText[:3] == "w:u":
                    styles = True
                    rawText[documentPage][paragraphNumber][0] += u"\u00A7n"
                elif tagText[:8] == "w:strike":
                    styles = True
                    rawText[documentPage][paragraphNumber][0] += u"\u00A7m"
                elif tagText[:11] == "w:highlight" and options["Make highlighted text obfuscated"]:
                    styles = True
                    rawText[documentPage][paragraphNumber][0] += u"\u00A7k"
                elif tagText[:7] == "w:color":
                    styles = True
                    rawText[documentPage][paragraphNumber][0] += u"\u00A7"+getColor(tagText[tagText.find("w:val")+7:tagText.find("w:val")+13])
                elif tagText[:4] == "w:sz":
                    if int(tagText[tagText.find("w:val")+7:tagText.find("\"", tagText.find("w:val")+7)]) > options["Convert text bigger than"]*2:
                        if options[u"\u00b7 fullwidth characters"]:
                            fullwidth = True
                        if options[u"\u00b7 uppercase"]:
                            uppercase = True
                elif tagText[:4] == "w:jc":
                    rawText[documentPage][paragraphNumber][1] = tagText[tagText.find("w:val")+7:tagText.find("\"", tagText.find("w:val")+7)]
                elif tagText[:4] == "/w:r" and len(tagText) == 4:
                    fullwidth = False
                    uppercase = False
                    if styles:
                        styles = False
                        rawText[documentPage][paragraphNumber][0] += u"\u00A7r"
                elif tagText[:4] == "/w:p" and len(tagText) == 4:
                    rawText[documentPage].append([u"", "left"])
                    paragraphNumber += 1
                elif tagText[:23] == "w:lastRenderedPageBreak":
                    rawText.append([[u"", "left"]])
                    documentPage += 1
                    paragraphNumber = 0

                tagText = ""

            elif currentType == "text":
                if uppercase:
                    letter = letter.upper()

                if fullwidth:
                    try:
                        letter = unichr(0xFEE0 + ord(letter))
                    except:
                        pass

                rawText[documentPage][paragraphNumber][0] += letter

        pageNumber = 0
        for page in rawText:
            paragraphNumber = 0
            for paragraph in page:
                rawText[pageNumber][paragraphNumber][0] = unescape(paragraph[0])
                paragraphNumber += 1
            pageNumber += 1

        return splitText(options, rawText)

    else:
        raise Exception("Only *.txt and *.docx files are supported!")


def makeBook(level, box, options, totalText, bookTitle):
    x = box.minx
    y = box.miny
    z = box.minz

    bookItem = TAG_Compound()
    bookItem["id"] = TAG_Short(387)
    bookItem["Damage"] = TAG_Short(0)
    bookItem["Count"] = TAG_Byte(1)
    bookItem["tag"] = TAG_Compound()
    bookItem["tag"]["title"] = TAG_String(bookTitle)
    bookItem["tag"]["pages"] = TAG_List()

    if options["the author of the book"] and options["Make"]:
        bookItem["tag"]["author"] = TAG_String(options["Make"])

    for page in totalText:
        bookItem["tag"]["pages"].append(TAG_String(page))

    if options["Output to"] == "Book Item Entity":
        book = TAG_Compound()
        book["Pos"] = TAG_List()
        book["Pos"].append(TAG_Double(x))
        book["Pos"].append(TAG_Double(y))
        book["Pos"].append(TAG_Double(z))
        book["id"] = TAG_String("Item")
        book["Item"] = bookItem

        chunk = getChunk(x, z)
        chunk.Entities.append(book)
        chunk.dirty = True

    elif options["Output to"] == "Book Item in Chest":

        chest = TAG_Compound()
        chest["id"] = TAG_String("Chest")
        chest["x"] = TAG_Int(x)
        chest["y"] = TAG_Int(y)
        chest["z"] = TAG_Int(z)
        chest["Items"] = TAG_List()
        chest["Items"].append(bookItem)

        chunk = getChunk(x, z)
        te = tileEntityAt(x, y, z)
        if te is not None:
            chunk.TileEntities.remove(te)
        chunk.TileEntities.append(chest)
        chunk.dirty = True

        setBlockAt(x, y, z, 54)
        setDataAt(x, y, z, 0)

    elif options["Output to"] == "Give Book Command Block":
        command = "/give @p minecraft:written_book 1 0 {title:\"" + bookTitle + "\",pages:["

        for page in totalText:
            command += "\"" + page + "\","

        if len(totalText) > 0:
            command = command[:len(command)-1]

        command += "]"

        if options["the author of the book"] and options["Make"]:
            command += ",author:\"" + options["Make"]

        command += "}"

        control = TAG_Compound()
        control["Command"] = TAG_String(command)
        control["id"] = TAG_String(u'Control')
        control["CustomName"] = TAG_String(u'@')
        control["SuccessCount"] = TAG_Int(0)
        control["x"] = TAG_Int(x)
        control["y"] = TAG_Int(y)
        control["z"] = TAG_Int(z)

        chunk = getChunk(x, z)
        te = tileEntityAt(x, y, z)
        if te is not None:
            chunk.TileEntities.remove(te)
        chunk.TileEntities.append(control)
        chunk.dirty = True

        setBlockAt(x, y, z, 137)
        setDataAt(x, y, z, 0)


def getColor(strColor):
    color = (int(strColor[0:2], 16), int(strColor[2:4], 16), int(strColor[4:6], 16))

    closestColor = min(colorCodes, key=partial(colorDifference, color))

    return colorCodes[closestColor]


def colorDifference(testColor, color):
    difference = 0
    for i in [0, 1, 2]:
        difference += abs(testColor[i]-color[i])

    return difference


def splitText(options, rawText):

    totalText = [[""]]
    pagedText = []

    allowedLineWidth = 120
    actualAllowedLineWidth = allowedLineWidth
    allowedLinesOnPage = 14

    lineWidth = 0

    pageNumber = 0
    lineNumber = 0

    extraWidth = getWidth(options, options["Append"])

    for documentPage in rawText:
        for documentParagraph in documentPage:
            letterIndex = 0

            align = documentParagraph[1]
            documentParagraphText = documentParagraph[0]

            for letter in documentParagraphText:
                letterWidth = 0
                wordWidth = getWidth(options, documentParagraphText[letterIndex:documentParagraphText.find(" ", letterIndex)])

                if totalText[pageNumber][lineNumber] != "":
                    if totalText[pageNumber][lineNumber][len(totalText[pageNumber][lineNumber])-1] != u"\u00A7":
                        letterWidth = getWidth(options, letter)
                    else:
                        wordWidth -= getWidth(options, letter)

                if options["to the end of each page"] and lineNumber == allowedLinesOnPage:
                    actualAllowedLineWidth = allowedLineWidth - extraWidth

                if lineWidth + wordWidth <= actualAllowedLineWidth and lineNumber != 0 and lineNumber <= allowedLinesOnPage:
                    totalText[pageNumber][lineNumber] += letter
                    lineWidth += letterWidth

                else:
                    actualAllowedLineWidth = allowedLineWidth

                    #if align == "center" or align == "right":
                    #    totalText[pageNumber][lineNumber] = alignText(options, align, totalText[pageNumber][lineNumber])

                    if lineNumber + 1 <= allowedLinesOnPage:
                        lineNumber += 1
                        totalText[pageNumber].append(letter)
                        lineWidth = letterWidth

                    elif options["into multiple minecraft pages"]:
                        pageNumber += 1
                        lineNumber = 0
                        totalText.append([letter])
                        lineWidth = letterWidth

                    else:
                        break

                letterIndex += 1

            totalText[pageNumber][lineNumber] += u"\012"

            actualAllowedLineWidth = allowedLineWidth

            if align == "center" or align == "right":
                totalText[pageNumber][lineNumber] = alignText(options, align, totalText[pageNumber][lineNumber])

            if lineNumber + 1 <= allowedLinesOnPage:
                lineNumber += 1
                totalText[pageNumber].append("")
                lineWidth = 0

            elif options["into multiple minecraft pages"]:
                pageNumber += 1
                lineNumber = 0
                totalText.append([""])
                lineWidth = 0

            else:
                break

        pageNumber += 1
        lineNumber = 0
        totalText.append([""])
        lineWidth = 0

    for page in totalText:
        lastLineNumber = len(page)-1
        while page[lastLineNumber] == "" or page[lastLineNumber] == u"\u00A7r" or u"\012" in page[lastLineNumber]:
            if u"\012" in page[lastLineNumber]:
                page[lastLineNumber] = page[lastLineNumber][:len(page[lastLineNumber])-1]

            else:
                page.pop(lastLineNumber)
                lastLineNumber -= 1
                if lastLineNumber < 0:
                    break

        if page != []:
            pagedText.append("")
            for line in page:
                pagedText[len(pagedText)-1] += line

            if options["to the end of each page"]:
                pagedText[len(pagedText)-1] += u"\u00A7r"+options["Append"]

    if options["to the end of each page"] and options["but the last one"]:
        lastPageNumber = len(pagedText)-1
        pagedText[lastPageNumber] = pagedText[lastPageNumber][:len(pagedText[lastPageNumber])-len(options["Append"])-2]

    return pagedText


def getWidth(options, text):
    totalWidth = 0
    letterIndex = 0
    for letter in text:
        if text[letterIndex-1] != u"\u00A7":
            try:
                totalWidth += characterWidths[letter]
            except:
                for character in characterWidths:
                    try:
                        # is it a fullwidth character?
                        if letter == unichr(0xFEE0 + ord(character)):
                            totalWidth += characterWidths[character]
                            break
                    except:
                        pass

    return totalWidth


def alignText(options, align, text):
    allowedLineWidth = 120
    textWidth = getWidth(options, text)

    factor = 1
    correction = 0

    if align == "center":
        factor = 2
    elif align == "right":
        correction = -1

    spaceCount = min(range(30), key=lambda trySpaceCount: abs(allowedLineWidth-abs(trySpaceCount*factor*4+textWidth)))

    line = " " * (spaceCount + correction) + text

    return line
