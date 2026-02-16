""" This is the main class for html document generation """
import yattag

class HtmlDoc:
    """Main class to allow document generation.
       This uses a class so that information can be
       stored and converted to text when desired.
       This is helpful if wanting to generate a 
       contents or menue

       Properties:
        - bodyItems: list of body items added to the document. This also stores locations of sections
        - headItems: list of html text for adding css, js, etc to the document head
        - sections: list of htmlDoc.sections in the document
        - title: document title
    """

    def __init__(self, title="htmlDoc"):
        """ initiates a document 

        Parameters:
            - title (optional): document title, if not provided "htmlDoc" will be used
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

    def addSection(title, level=1, id=None, atr=[]):
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

        raise NotImplementedError()

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

    def addText(self, text, atr=[]):
        """ Adds text to the section, this will be inside a html paragraph tag
    
        Parameters:
            - text: paragraph text
            - atr (optional): list of tuples. Each item is a name-value pair which is added as an atribute
                to the heading. For example ["style", "text-align:center"] would add a style attribute
        """

        code = paragraph(text, atr, self.indentText)
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

    atr = [('src', link)] + atr
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
        
def paragraph(textStr, atr=[], indentText=False):
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

    with tag('p', *atr):
        text(textStr)
    
    result = yattag.indent(
        doc.getvalue(),
        indent_text = indentText
        )

    return result

# FOR TESTING
if __name__ == "__main__":
    section = Section('This is a Heading', level=2, id='sec1', atr=[("class",'testClass')])
    section.addText('This is section 1 paragraph text')
    sub = section.addSubsection('this is a subsection', id='sec1.1')
    sub.addText('This is section 1.1 paragraph text')
    text = section.generateHtml()
    print(text)

    print(hyperlink('www.google.com'))
    
