import htmlDoc

# create the document object
doc = htmlDoc.HtmlDoc(title="Example HTML Document", indentText=False)
# Add section showing basice html functionality
section = doc.addSection('Basic HTML', level=2, id='basicHtml')
section.addText('This section shows basic html functionality.')
# TODO show allAsText and allAsIs examples
section.addText('Text can be added using the addText method, which will be wrapped in a paragraph (<p>) tag. You can also include html tags in the text, such as <b>&lt;b&gt;bold&lt;/b&gt;</b> or <i>&lt;i&gt;italics&lt;/i&gt;</i>.',
                )
section.addText('You can also add hyperlinks using the hyperlink function: ' + htmlDoc.hyperlink('https:\\www.google.com', 'Google'))

sub = section.addSubsection('Lists', id='HTML Lists')
sub.addText('Not implemented')

text = doc.generateHtml()
doc.saveFile("testDoc.html")