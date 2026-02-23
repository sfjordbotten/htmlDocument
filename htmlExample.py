import htmlDoc

# create the document object
doc = htmlDoc.HtmlDoc(title="Example HTML Document", indentText=False)

# add text at the document level
doc.addText('This is an example HTML document created using the htmlDoc library. ' +
            'The htmlExampl.py file plus the example html file show how to use the ' +
            'library to create an html document with various features.')

# Add section showing basice html functionality
section = doc.addSection('Basic HTML', level=2, id='basicHtml')
section.addText('This section shows basic html functionality.')

###########################
# ADD GENERTIC TEXT EXAMPLE
###########################
sub = section.addSubsection('Paragraph Text', id='paragraphText')

sub.addText('Text can be added using the addText method, which will be wrapped ' +
'in a paragraph (<p>) tag. You can also include html tags in the text, such as ' +
'<b>&lt;b&gt;bold&lt;/b&gt;</b> or <i>&lt;i&gt;italics&lt;/i&gt;</i>.',
                )
sub.addText('By default, special characters in the text will be escaped, except ' +
'for html tags allowed inside a paragraph. If you want to limit allowed html tags, ' +
'you can use the "keepTags" parameter to specify which tags to allow. If you want ' +
'to prevent this "smart" behaviour, you can use the allAsText or allAsIs paramters. ' +
'The allAsText method will escape all special characters (including html tags), ' + 
'while the allAsIs method will not escape any special characters.')
sub.addText('For example, this text is added using allAsText=True: <b>Bold Text</b>', allAsText=True)
sub.addText('For example, this text is added using allAsIs=True: <b>Bold Text</b>', allAsIs=True)

###########################
# HYPERLINK EXAMPLE
###########################
sub = section.addSubsection('Hyperlinks', id='hyperlinks')
sub.addText('You can add hyperlinks using the hyperlink function: ' + htmlDoc.hyperlink('https:\\www.google.com', 'Google'))

###########################
# LIST EXAMPLE
###########################
sub = section.addSubsection('Lists', id='HTML Lists')

sub.addText('You can add ordered and unordered lists using the addOrderedList and addUnorderedList methods. ' +
'These methods take a list of items to include in the list. Each item can be a string or a block of html code. ' +
'You can also include nested lists by including a list as an item in the main list.')

sub.addText('The following is an example of an ordered list:')
sub.addOrderedList(['First item', 'Second item', ['2a', '2b'], 'Third item'])
sub.addText('The following is an example of an unordered list:')
sub.addUnorderedList(['First item', 'Second item', 'Third item', ['Subitem 1', 'Subitem 2']])
sub.addText('The following is an example of an ordered list with a nested unordered list. ' +
            'Note that the unordered list is included as part of the second item in the ' + 
            'ordered list (rather than as its own item):')
sub.addOrderedList(['First item', 
                    'Second item' + htmlDoc.unorderedList(['Subitem, unorderd']),
                    'Third item'])

text = doc.generateHtml()
doc.saveFile("testDoc.html")