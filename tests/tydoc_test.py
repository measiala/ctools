# Some tests for tytable

import sys
import os
import os.path

sys.path.append( os.path.join( os.path.dirname(__file__), "../.."))

from ctools.tydoc import *
from ctools.latex_tools import run_latex

def test_tytag_option():
    t = TyTag('demo')
    t.set_option("FOO")
    assert t.option("FOO")==True
    assert t.option("BAR")==False
    t.set_option("BAR")
    assert t.option("FOO")==True
    assert t.option("BAR")==True
    t.clear_option("FOO")
    assert t.option("FOO")==False
    assert t.option("BAR")==True

    
def test_tytable_access():
    """Make sure construction and access methods work properly"""
    t = tytable()
    t.add_head(['x','x-squared','x-cubed'])
    t.add_data([1,1,1])
    t.add_data([2,4,8])
    t.add_data([3,9,27])
    for row in t.rows():
        s = ET.tostring(row,encoding='unicode')
        print(s)
    assert t.get_cell(0,1).text == 'x-squared'
    assert float(t.get_cell(1,1).text) == 1
    assert float(t.get_cell(2,1).text) == 4
    assert float(t.get_cell(3,1).text) == 9

def test_tytable_attribs():
    d2 = tytable()
    d2.set_option(OPTION_LONGTABLE)
    d2.add_head(['State','Abbreviation','Population'],cell_attribs={ATTRIB_ALIGN:ALIGN_CENTER})
    d2.add_data(['Virginia','VA',8001045],
                cell_attribs=[{},{ATTRIB_ALIGN:ALIGN_CENTER},{ATTRIB_ALIGN:ALIGN_RIGHT}])
    d2.add_data(['California','CA',37252895],
                cell_attribs=[{},{ATTRIB_ALIGN:ALIGN_CENTER},{ATTRIB_ALIGN:ALIGN_RIGHT}])
    s = ET.tostring(d2,encoding='unicode')
    assert 'CENTER' in s
    assert d2.get_cell(0,0).attrib[ATTRIB_ALIGN]==ALIGN_CENTER
    assert d2.get_cell(0,1).attrib[ATTRIB_ALIGN]==ALIGN_CENTER
    assert d2.get_cell(0,2).attrib[ATTRIB_ALIGN]==ALIGN_CENTER
    assert ATTRIB_ALIGN not in d2.get_cell(1,0).attrib
    assert d2.get_cell(1,1).attrib[ATTRIB_ALIGN]==ALIGN_CENTER
    assert d2.get_cell(1,2).attrib[ATTRIB_ALIGN]==ALIGN_RIGHT

    

def test_tydoc_latex():
    """Create a document that tries lots of features and then make a LaTeX document and run LaTeX"""

    doc = tydoc()
    doc.h1("Table demo")

    d2 = doc.table()
    d2.set_option(OPTION_TABLE)
    d2.add_head(['State','Abbreviation','Population'])
    d2.add_data(['Virginia','VA',8001045])
    d2.add_data(['California','CA',37252895])


    d2 = doc.table()
    d2.set_option(OPTION_LONGTABLE)
    d2.add_head(['State','Abbreviation','Population'])
    d2.add_data(['Virginia','VA',8001045])
    d2.add_data(['California','CA',37252895])

    doc.save("tydoc.tex", format="latex")
    run_latex("tydoc.tex")

def test_tydoc_toc():
    """Test the Tydoc table of contents feature."""
    doc = tydoc()
    doc.h1("First Head1")
    doc.p("blah blah blah")
    doc.h1("Second Head1 2")
    doc.p("blah blah blah")
    doc.h2("Head 2.1")
    doc.p("blah blah blah")
    doc.h2("Head 2.2")
    doc.p("blah blah blah")
    doc.h3("Head 2.2.1")
    doc.p("blah blah blah")
    doc.h1("Third Head1 3")
    doc.p("blah blah blah")

    # Add a toc
    doc.insert_toc()

    # Make sure that the TOC has a pointer to the first H1
    print(doc.prettyprint())
    key = f".//{TAG_X_TOC}"
    tocs = doc.findall(key)
    assert len(tocs)==1
    toc = tocs[0]

    h1s = doc.findall(".//{}/{}".format(TAG_BODY,TAG_H1))
    assert len(h1s)==3
    h1 = h1s[0]

    # Make sure that they both have the same ID
    id1 = toc.find('.//{}'.format(TAG_A)).attrib['HREF']
    id2 = h1.find('.//{}'.format(TAG_A)).attrib['NAME']
    
    assert id1==id2
