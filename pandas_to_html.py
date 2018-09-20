#!/usr/bin/env python

"""
Export Pandas dataframes to HTML 
Uses two means of creating the HTML
(1) The automatic df.style.render() method which incorporates styling applied
to the dataframe
(2) Direct writing to the HTML (e.g. using HTML_Helper class)
This may cause a certain amount of duplication/messiness but using
df.style.render() is very convenient, although direct update also needed
for extra flexibility, e.g. add headings and nav)

General approach -
 Create dataframe(s)
 Style them using standard Pandas styler
 Convert them to HTML using styler render() method (which retains pandas styling)
 Write these to HTML file but also with directly added elements which may have
 their own manual styling
"""

import pandas as pd

class HTML_Helper(object):
    """Helps construct HTML File
    Args:
        filename - filename of destination HTML file
    """ 
    def __init__(self, filename):
        self.filename = filename
        # Holds the html text
        self.content = ""
    
    def add(self, text):
        """Append text to content
        args:
            text - text to be added"""
        self.content = self.content + text
    
    def save(self, mode="w"):
        """Save content to file
        args:
            mode - file open mode"""
        with open(self.filename, mode) as f:
            f.write(self.content)

    def heading(self, text, h_id="", size='3'):
        """Add heading with id for hyperlinking"""
        size = str(size) #size needs to be a string, not a number
        text = '\n<h{} id="{}" >{}</h{}>\n'.format(size, h_id, text, size)
        self.add(text)
        
    def link(self, text, l_id):
        """Add hyperlink"""
        ##text = '<a href="#'+l_id+'">'+str(text)+'</a><br>\r\n'
        text = '<a href="#{}">{}</a><br>\n'.format(l_id, text)
        self.add(text)
        
    def cssline(self, lable, values):
        """Create  CSS style line"""
        return lable+"{"+"".join([v+";" for v in values])+"}"

    def image(self, filename, border="", scale="", hyper=True):
        """Add image to file
        Args:
            filename - image filename
            border - optional border width
            scale - optional width & height scale as % e.g. "50%"
            hyper (bool) - when true make image a hyperlink to the image file
        """
        if hyper:
            text = '<a href="'+filename+'">\n'
        else:
            text = ''

        text = text + '<img src="' + filename + '" alt="' + filename + '"'

        if border:
            text = text + ' border="' + border + '"'
        if scale:
            text = text + ' width="' + scale + '"'
            text = text + ' height="'+ scale + '"'
        #end of image
        text = text + '>\n'
        #end of hyperlink
        if hyper:
            text = text + "</a>\n"
        self.add(text)

    def nav(self, title="Links", items=[("1","Item 1"),("2","Item 2")]):
        """Adds a nav containing in-page links
        Args:
            title (heading text for nav)
            items - items for nav as list of pairs (list or tuple)
            left of each pair is the link name (without #), right of each pair
            is link text to display, eg [("1","Item 1"),("2","Item 2")]
        """
        text = "\n\n<nav>\n<b>" + title + "</b>\n<br>\n"
        for item in items:
            text = text + '<a class="nav" href="#' + item[0] + '">' + item[1] + '</a><br>\n'
        text = text + "</nav>\n"
        self.add(text)

# Pandas dataframe styling/formatting functions

def highlight_conditions(val):
    """Cell formating function for Pandas dataframe .styl.applymap()
    method
    """
    mapping = {
        0:("red", "pink"),
        1:("yellow", "orange"),
        4:("purple", "blue")
    }
    colours = mapping.get(val, ("black", "white") )
    return 'color: {}; background-color: {}'.format(*colours)


def row_style(row_data):
    """Row-by-row styler for pandas
    Use with df.style.apply(row_data, axis=1)
    """
    highlighted = "color: blue; background-color: orange"
    # Define style for each column within the row
    # List comprehension might be possible but trouble too
    row_styles = []
    for i, value in enumerate(row_data):
        #Default plain style
        style = ""
        #Special styling
        if i==2:
            if row_data[0] < row_data[2]:
                style = highlighted
        row_styles.append(style)
    return row_styles

#Style for df.style.set_table_styles()
styles = [
    {"selector":"th", "props":[("font-size","110%"),("color","cyan"),("background-color","grey")]}
]



# General Style for the HTML file (not used by Pandas styler)
style="""
<style>
h1 {font-size:200%;background-color:#111131;margin-bottom:3;margin-top:0;color:#EEEE22;clear:both;}
h2 {font-size:140%;background-color:#111151;margin-bottom:8;margin-top:8;color:#FEFEFE;clear:both;}
h3 {font-size:120%;background-color:#CDCDDD;margin-bottom:8;margin-top:8;color:#111151;clear:both;}

table {border-collapse:collapse;cellspacing:1; cellpadding:1;}
table, th, td {border:1px solid #555555;}
th {font-size:90%;font-family:verdana,arial,'sans serif';background-color:#C0C0D0}
tr {font-size:90%;font-family:verdana,arial,'sans serif';background-color:#FFFFFF;vertical-align:top;}

#bad {background-color:#FFF366;}
#skip {background-color:#DDFFDD;}

body{
font-size:75%;
font-family:verdana,arial,'sans serif';
background-color:#EFEFFF;
color:#000040;
margin:10px
}

nav{
background-color:#EEEEAA;
position: fixed;
right: 2%;
top: 5%;
padding:8px;
border:1px black solid;
opacity: 0.9;
}

img{
width: 60%;
height: auto;
}

.left_block{
float:left;
width: 48%;
overflow:hidden;
}

.right_block{
		float:left;
		overflow:hidden;
		width: 48%;
		##padding-right:30px
}

</style>
"""

# Create a dataframe
df1 = pd.DataFrame()
df1["x 1"] = range(0, 10)
df1["y 2"] = df1["x 1"]**2
df1["z 3"] = 5*df1["x 1"] - df1["y 2"]

#Create another dataframe
data = [[x*y for x in range(1, 4)] for y in range(0, 11)]
df2 = pd.DataFrame(data, columns = ["Cakes", "Hats", "Moose"])

#Create another dataframe
data = [[x*x-y for x in range(1, 4)] for y in range(0, 21)]
df3 = pd.DataFrame(data, columns = ["Mangrove", "Marzipan", "Sheds"])


#dfh = df1.style.set_table_styles(styles)\
#.applymap(highlight_conditions)\
#.apply(row_style, axis=1)\
#.set_properties(**{'border-color': 'black', 'border-style':'solid', 'border-width':'thin'})\
#.render()


#dfh = df1.style.set_table_styles(styles)\
#.applymap(highlight_conditions)\
#.set_properties(**{'border-color': 'black', 'border-style':'solid', 'border-width':'thin'})\
#.render()


# hide_index needs Pandas 0.23
##dfh = df1.style.applymap(highlight_conditions).hide_index().render()
dfh = df1.style.applymap(highlight_conditions).render()

#Setup HTML File
filename = "eg.html"
go = HTML_Helper(filename)
go.add(style)
go.heading("Pandas Dataframes Exported to HTML", size=1)


#Add the dataframes
dataframes = [df1, df2, df3]
headings = ["First", "Second", "Third"]
nav_items = []
for i, (df, heading) in enumerate(zip(dataframes, headings)):
    # Add heading to HTML
    go.heading(heading, str(i), size=2)
    # Apply style, convert to html source, add to the html
    df_html = df.style.applymap(highlight_conditions).render()   
    go.add(df_html)
    nav_items.append((str(i), heading))

#Save at end
go.nav(items = nav_items)
go.save()
