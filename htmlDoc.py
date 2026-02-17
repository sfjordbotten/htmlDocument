""" This is the main class for html document generation """
import yattag
from html.parser import HTMLParser

selfClosingTags = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link",
                   "meta", "param", "source", "track", "wbr"]

class HtmlDoc:
    """Main class to allow document generation.
       This uses a class so that information can be
       stored and converted to text when desired.
       This is helpful if wanting to generate a 
       contents or menue

       Properties:
        - bodyItems: list of body items added to the document. This also stores locations of sections
        - headItems: list of html text for adding css, js, etc to the document head
        - indentText: yattag indent option, for text inside tags. Default is False
        - sections: list of htmlDoc.sections in the document
        - title: document title
    """

    def __init__(self, title="htmlDoc", indentText=False):
        """ initiates a document 

        Parameters:
            - title (optional): document title, if not provided "htmlDoc" will be used
            - indentText (optional): yattag indent option, for text inside tags. Default is False
        """

        # for storing items to add to head.
        # this can include css, javascript, etc
        self.headItems = []
        # for storing sections, can be used to generate menues
        # or table of contents
        self.sections = []
        # list of body items added to the document. This also stores locations of sections
        self.bodyItems = []
        
        # store parameters in object
        self.title = title
        self.indentText = indentText
        

    def addSection(self, title, level=1, id=None, atr=[]):
        """ adds a section to the document

        Parameters:
            - title: title for the section, this will be displayed in a heading tag in the HTML
            - level (optional): heading level to use. Default is 1, which uses h1 heading.
            - id (optional): id value to used in html tag. If not provided or None, title will be used
            - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
                to the heading. For example ["style", "text-align:center"] would add a style attribute
        Returns:
            - the htmlDoc.section object created
        """

        if id is None:
            id = title

        sec = Section(title, level=level, id=id, atr=atr, indentText=self.indentText)
        
        self.sections.append(sec)
        self.bodyItems.append(sec)

        return sec

    def generateHtml(self):
        """ Converts the document into html code

        Returns: html code equivalent of the document
        """

        doc, tag, text = yattag.Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text(self.title)
                for item in self.headItems:
                    doc.asis(item)
            with tag('body'):
                # Add document title as h1 heading
                doc.asis(heading(self.title, level=1, indentText=self.indentText))
                # add body items, which include sections and other html code
                for item in self.bodyItems:
                    if isinstance(item, str):
                        # treat as html generated text already
                        doc.asis(item)
                    else:
                        # assume this is a class from this module, use generateHtml method
                        doc.asis(item.generateHtml())

        result = yattag.indent(
        doc.getvalue(),
        indent_text = self.indentText
        )

        return result
    
    def saveFile(self, filename=None):
        """ saves the document as an html file

        Parameters:
            - filename (optional): name of the file to save. If not provided, title will be used with .html extension
        """

        if filename is None:
            filename = self.title + ".html"

        htmlCode = self.generateHtml()

        with open(filename, 'w') as f:
            f.write(htmlCode)
    
class Section:
    """ Class for a section of the html document 

    Properties:
        - htmlCode: list of html code items added to the section, also tracks location of subsections
        - id: id value to used in html tag. If not provided or None, title will be used
        - level: heading level to use. Default is 1, which uses h1 heading.
        - subsections: list of subsections in this section
        - title: title for the section, this will be displayed in a heading tag in the HTML
    """

    def __init__(self, title, level=1, id=None, atr=[], indentText=False):
        """ Creates a section object

        Parameters:
            - title: title for the section, this will be displayed in a heading tag in the HTML
            - level (optional): heading level to use. Default is 1, which uses h1 heading.
            - id (optional): id value to used in html tag. If not provided or None, title will be used
            - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
                to the heading. For example ["style", "text-align:center"] would add a style attribute
            - indentText (optional): yattag indent option, for text inside tags. Default is False
        """

        # store parameters in object
        self.title = title
        self.level = level
        if id is None:
            self.id = title
        else:
            self.id = str(id)
        self.atr = atr
        self.indentText = indentText
        
        # list of subsections added to section
        self.subsections = []
        # list of html code added to the section. This also includes location of subsections
        self.htmlCode = []

    # TODO add docs for allAsText and allAsIs parameters
    def addText(self, text, atr=[], allAsText=False, allAsIs=False):
        """ Adds text to the section, this will be inside a html paragraph tag
    
        Parameters:
            - text: paragraph text
            - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
                to the heading. For example ["style", "text-align:center"] would add a style attribute
        """

        code = paragraph(text, atr, self.indentText, allAsText=allAsText, allAsIs=allAsIs)
        self.htmlCode.append(code)
        
    def addSubsection(self, title, id=None, atr=[]):
        """adds a subsection one level lower than this section

        Parameters
            - title: title for the section, this will be displayed in a heading tag in the HTML
            - id (optional): id value to used in html tag. If not provided or None, title will be used
            - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
                to the heading. For example ["style", "text-align:center"] would add a style attribute
        """

        sub = Section(title, level=self.level + 1, id = id, atr=atr, indentText=self.indentText)
        self.subsections.append(sub)
        self.htmlCode.append(sub)
    
        return sub
        
    def generateHtml(self):
        """ Converts the section into a block of html text

        Returns: html code equivalent of the section
        """

        doc, tag, text = yattag.Doc().tagtext()

        with tag("section"):
            # if id is not provided in atr, add it
            if 'id' not in [x[0] for x in self.atr]:
                self.atr.append(('id', self.id))
            doc.asis(heading(self.title, self.level, atr=self.atr, indentText=self.indentText))
                                 
            for item in self.htmlCode:
                if isinstance(item, str):
                    # treat as html generated text already
                    doc.asis(item)
                else:
                    # assume this is a class from this module, use generateHtml method
                    doc.asis(item.generateHtml())

        result = yattag.indent(
        doc.getvalue(),
        indent_text = self.indentText
        )

        return result

def heading(title, level=1, atr=[], indentText=False):
    """Creates an html heading tag
    
    Parameters:
        - title: title for the section, this will be displayed in a heading tag in the HTML
        - level (optional): heading level to use. Default is 1, which uses h1 heading.
        - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
            to the heading. For example ["style", "text-align:center"] would add a style attribute
        - indentText (optional): yattag indent option, for text inside tags. Default is False
        """

    doc, tag, text = yattag.Doc().tagtext()

    tagType = 'h' + str(level)

    with tag(tagType, *atr):
        text(title)
    
    result = yattag.indent(
        doc.getvalue(),
        indent_text = indentText
        )

    return result

def hyperlink(link, textStr=None, newTab=True, atr=[], indentText=False):
    """ generates an html hyperlink

    Parameters:
        - link: the target for the hyperlink
        - textStr (optional): if provided, the text to show as the hyperlink.
            Default is None, in which case link is displayed
        - newTab (optional): whether or not the link should be opened in a new tab
            Default is True
        - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
            to the heading. For example ["style", "text-align:center"] would add a style attribute
        - indentText (optional): yattag indent option, for text inside tags. Default is False

    Returns:
        - html code for the hyperlink
    """

    atr = [('href', link)] + atr
    if newTab:
        if "target" not in [x[0] for x in atr]:
            atr.append(('target', '_blank'))
    if textStr is None:
        textStr = link
        
    doc, tag, text = yattag.Doc().tagtext()

    with tag('a', *atr):
        text(textStr)
    
    result = yattag.indent(
        doc.getvalue(),
        indent_text = indentText
        )

    return result

# TODO add docs for allAsText and allAsIs parameters and keepTags parameter        
def paragraph(textStr, atr=[], indentText=False, allAsText=False, allAsIs=False,
              keepTags=['a', 'abbr', 'area', 'audio', 'b', 'bdi', 'bdo', 'br',
                        'button', 'canvas', 'cite', 'code', 'data', 'datalist', 
                        'del', 'dfn', 'em', 'embed', 'i', 'iframe', 'img', 'input',
                        'ins', 'kbd', 'label', 'link', 'map', 'mark', 'math', 'meta',
                        'meter', 'noscript', 'object', 'output', 'picture', 'progress', 
                        'q', 'ruby', 's', 'samp', 'script', 'select', 'slot', 'small', 
                        'span', 'strong', 'sub', 'sup', 'SVG svg', 'template', 'text',
                        'textarea', 'time', 'u', 'var', 'video', 'wbr'],
            ):
    """ Generates an html paragraph
    
    Parameters:
        - textStr: paragraph text
        - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
            to the heading. For example ["style", "text-align:center"] would add a style attribute
        - indentText (optional): yattag indent option, for text inside tags. Default is False

    Returns:
        html code for the paragraph
    """
    
    doc, tag, text = yattag.Doc().tagtext()

    if allAsText and allAsIs:
        raise ValueError("allAsText and allAsIs cannot both be True")
    if allAsText:
        subTexts = [textStr]
        subTypes = ['text']
    elif allAsIs:
        subTexts = [textStr]
        subTypes = ['tag']
    else:
        subTexts, subTypes = spitTags(textStr, keepTags)

    with tag('p', *atr):
        for iii in range(0, len(subTexts)):
            if subTypes[iii] == 'text':
                text(subTexts[iii])
            else:
                doc.asis(subTexts[iii])
    
    result = yattag.indent(
        doc.getvalue(),
        indent_text = indentText
        )

    return result

# TODO: add docs
def spitTags(text, tags):

    # create parser to find tags and their locations in the text
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.foundItem = []
            self.startInds = []
            self.foundType = []
        def handle_starttag(self, tag, attrs):
            self.foundItem.append(tag)
            self.startInds.append(self.getpos())
            self.foundType.append("start")
        def handle_endtag(self, tag):
            self.foundItem.append(tag)
            self.startInds.append(self.getpos())
            self.foundType.append("end")
        def handle_data(self, data):
            self.foundItem.append(data)
            self.startInds.append(self.getpos())
            self.foundType.append("data")


    parser = MyHTMLParser()
    parser.feed(text)
    # parser shows line and index of the tag, but we want index in the whole string, 
    # so we need to convert
    lines = text.split('\n')
    startInds = parser.startInds
    startInds = [sum([len(x) - 1 for x in lines[0 : start[0] - 1]]) + # passed lines
                 2 * (start[0]-1) + # newlines in passed lines
                 start[1] for start in startInds] # index in line
    # extract information about tags found by parser
    foundItem = parser.foundItem
    foundType = parser.foundType
    # check if tags found are in search list
    subTexts = []
    subTypes = []
    subStartInds = []
    subEndInds = []
    iii = 0
    while iii < len(foundItem):
        if foundType[iii] == 'start' and foundItem[iii] in tags:
            if len(subEndInds) == 0 and startInds[iii] > 0:
                # if this is the first tag found and there is text before it, add that text to subTexts and subTypes
                subTexts.append(text[0 : startInds[iii]])
                subTypes.append('text')
                subStartInds.append(0)
                subEndInds.append(startInds[iii] - 1)
            elif not subEndInds[-1] == startInds[iii] - 1:
                # if there is text between the end of the last tag and the start of this tag, add that text to subTexts and subTypes
                subTexts.append(text[subEndInds[-1] + 1 : startInds[iii]])
                subTypes.append('text')
                subStartInds.append(subEndInds[-1] + 1)
                subEndInds.append(startInds[iii] - 1)

            if foundItem[iii] in selfClosingTags:
                # no end tag, just add to subTexts and subTypes
                startInd = startInds[iii]
                if iii + 1 < len(startInds):
                    endInd = startInds[iii + 1]
                else:
                    endInd = len(text)
                subTexts.append(text[startInd : endInd])
                subTypes.append('tag')
                subStartInds.append(startInd)
                subEndInds.append(endInd - 1)
            else:
                # find corresponding end tag
                tag = foundItem[iii]
                startInd = startInds[iii]
                iii += 1
                while not (foundItem[iii] == tag and foundType[iii] == 'end'):
                    iii += 1
                if iii + 1 < len(startInds):
                    endInd = startInds[iii + 1]
                else:
                    endInd = len(text)
                subTexts.append(text[startInd : endInd])
                subTypes.append('tag')
                subStartInds.append(startInd)
                subEndInds.append(endInd - 1)
        iii += 1
    # check for text after the last tag
    if len(subEndInds) > 0 and subEndInds[-1] < len(text) - 1:
        subTexts.append(text[subEndInds[-1] + 1 :])
        subTypes.append('text')
        subStartInds.append(subEndInds[-1] + 1)
        subEndInds.append(len(text) - 1)

    return subTexts, subTypes
    

# FOR TESTING
if __name__ == "__main__":
    

    html_string = '<h1>Hi<br></h1><p>test \n<span class="time">test</span></p>'
    print(paragraph(html_string))#, keepTags=[]))
    
    

    
        
