#! /usr/bin/env python

# Copyright (c) 2007-2009 PediaPress GmbH
# See README.txt for additional licensing information.

import os
from mwlib import parser, rendermath, timeline

import urllib
import cgi

from PIL import Image

from mwlib.log import Log

log = Log("htmlwriter")

class HTMLWriter(object):
    imglevel = 0
    namedLinkCount = 1
    def __init__(self, out, no_table=None, images=None, math_renderer=None):
        self.out = out
	self.no_table  = no_table
        self.level = 0
        self.images = images
        # self.images = imgdb.ImageDB(os.path.expanduser("~/images"))
        self.references = []
        if math_renderer is None:
            self.math_renderer = rendermath.Renderer()
        else:
            self.math_renderer = math_renderer
    
    def _write(self, s):
        self.out.write(cgi.escape(s.encode("utf8")))

    def getCategoryList(self, obj):
        categories = list(set(c.target for c in obj.find(parser.CategoryLink)))
        categories.sort()
        return categories
                    
    def write(self, obj):
        m = "write" + obj.__class__.__name__
        m=getattr(self, m, None)
        if not m:
            log.warn("No method to write object:", obj.__class__.__name__)
            return
        m(obj)

    def ignore(self, obj):
        pass

    def serializeVList(self,vlist):
        #FIXED
        return 
        args = []
        styleArgs = []
        gotClass = 0
        gotExtraClass = 0
        for (key,value) in vlist.items():
            if isinstance(value, (basestring, int)):
                if key=="class":
                    args.append('%s="%s"' % (key, value))
                    gotClass = 1
                else:
                    args.append('%s="%s"' % (key, value))
            if isinstance(value, dict) and key=="style":
                for (_key,_value) in value.items():
                    styleArgs.append("%s:%s" % (_key, _value))
                args.append(' style="%s"' % ';'.join(styleArgs))
                gotExtraClass = 1
        return ' '.join(args)


    def writeMagic(self, m):
        if m.values.get('html'):
            for x in m.children:
                self.write(x)

    def writeSection(self, obj):
        header = "%s" % (obj.level)
        self.out.write("")
        self.write(obj.children[0])
        self.out.write("")
                
        self.level += 1
        for x in obj.children[1:]:
            self.write(x)
        self.level -= 1

    def writePreFormatted(self, n):
        self.out.write("")
        for x in n:
            self.write(x)
        self.out.write("")
        
    def writeNode(self, n):
        for x in n:
            self.write(x)

    def writeCell(self, cell):
        svl = ""
        if cell.vlist:
            svl = self.serializeVList(cell.vlist)
            
        self.out.write('%s' % svl)
        for x in cell:
            self.write(x)
        self.out.write("")

    def writeCaption(self, t):
	self.out.write("")

    def writeTagNode(self, t):
	self.out.write("")
	return
        if t.caption == 'ref':
            self.references.append(t)
            self.out.write("%s" % len(self.references))
            return
        elif t.caption == 'references':
            if not self.references:
                return

            self.out.write("")
            for r in self.references:
                self.out.write("")
                for x in r:                    
                    self.write(x)
                self.out.write("")
            self.out.write("")
                           
            self.references = []            
            return
        elif t.caption=='imagemap':
            # FIXME. this is not complete. t.imagemap.entries should also be handled.
            print "WRITEIMAGEMAP:", t.imagemap
            if t.imagemap.imagelink:
                self.write(t.imagemap.imagelink)
            return

        
        self.out.write(t.starttext)
        for x in t:
            self.write(x)
        self.out.write(t.endtext)
            
    def writeRow(self, row):
        self.out.write('')
        for x in row:
            self.write(x)
            
        self.out.write('')

    def writeTable(self, t):          
        if self.no_table:
            return	 
        svl = ""
        if t.vlist:
            svl = self.serializeVList(t.vlist)

        
            
        self.out.write("%s " % svl)
        if t.caption:
            self.out.write("")
            self.write(t.caption)
            self.out.write("")
        for x in t:
            self.write(x)
        self.out.write("")

    def writeMath(self, obj):
        latex = obj.caption
        p = self.math_renderer.render(latex)
        self.out.write('%s' % os.path.basename(p))

    def writeURL(self, obj):
        self.out.write('%s ' % obj.caption)
        if obj.children:
            for x in obj.children:
                self.write(x)
        else:
            self.out.write(obj.caption)
            
        self.out.write('')

    def writeNamedURL(self, obj):
	#FIXED
        self.out.write('%s ' % obj.caption.encode("utf-8"))
        if obj.children:
            for x in obj.children:
                self.write(x)
        else:
            name = "%s" % self.namedLinkCount
            self.namedLinkCount += 1
            self.out.write(name)
                        
        self.out.write('')

        
    def writeParagraph(self, obj):
        self.out.write("\n")
        for x in obj:
            self.write(x)
        self.out.write("\n")

    def getHREF(self, obj):
	return ""
        parts = obj.target.encode('utf-8').split('#')
        parts[0] = parts[0].replace(" ", "_")
        
	return ""
        return ' %s ' % ("#".join([urllib.quote(x) for x in parts]))

    writeLangLink = ignore

    def writeLink(self, obj):
        if obj.target is None:
            return

        href = self.getHREF(obj)
        if href is not None:
#            self.out.write('%s ' % (href,))
            self.out.write("")
        else:
            self.out.write('')
        if obj.children:
            for x in obj.children:
                self.write(x)
        else:
            self._write(obj.target)
            
        self.out.write("")

    writeArticleLink = writeLink

    def writeSpecialLink(self, obj):
        if obj.children:
            for x in obj.children:
                self.write(x)
        else:
            self._write(obj.target)

    def writeCategoryLink(self, obj):
        if obj.colon:
            if obj.children:
                for x in obj.children:
                    self.write(x)
            else:
                self._write(obj.target)

    def writeTimeline(self, obj):
        #FIXED
        return
        img = timeline.drawTimeline(obj.caption)
        if img is None:
            return
        
        target = "/timeline/"+os.path.basename(img)
        width, height = Image.open(img).size
        
        self.out.write('%s ' % (target, ))
        
    def writeImageLink(self, obj):
	#FIXED
        return 	

        """
        <span class='image'>
          <span class='left'>
            <img src='bla' />
            <span class='imagecaption'>bla bla</span>
          <span/>
        <span/>
        """
        
        if self.images is None:
            return

        width = obj.width
        height = obj.height

        #if not width:
        #    width = 400  # what could be a sensible default if no width is given? maybe better 0?

        if width:
            path = self.images.getPath(obj.target, size=max(width, height))
        else:
            path = self.images.getPath(obj.target)

        if path is None:
            return

        if isinstance(path, str):
            path = unicode(path, 'utf8')
        targetsrc = '/images/%s' % path
        
        
        if self.imglevel==0:
            self.imglevel += 1

            try:
                def getimg():
                    return Image.open(self.images.getDiskPath(obj.target, size=max(width, height)))
                img = None
                
                if not width:
                    if not img:
                        img = getimg()
                    size = img.size
                    width = min(400, size[0])

                if not height:
                    if not img:
                        img = getimg()
                    size = img.size
                    height = size[1]*width/size[0]
            except IOError, err:
                self.imglevel -= 1
                log.warn("Image.open failed:", err, "path=", repr(path))
                return

            if obj.isInline():
                self.out.write('%s ' % (targetsrc, ))
            else:
                align = obj.align
                if obj.thumb == True and not obj.align:
                    obj.align= "clear right"
#                self.out.write('''<div  class="bbotstyle image %s" style="width:%spx">'''% (obj.align, width))
                self.out.write('<img src="%s" width="%s" height="%s" />' % (targetsrc, width, height))
                
 #               self.out.write('<span class="imagecaption">')
                for x in obj.children:
                    self.write(x)
  #              self.out.write('</span></div>')
            self.imglevel -= 1
        else:
#            self.out.write('<a href="%s">' % targetsrc)
            for x in obj.children:
                self.write(x)
            self.out.write('</a>')

    def writeText(self, t):
        #self.out.write(cgi.escape(t.caption).encode('ascii', 'xmlcharrefreplace'))
        self._write(t.caption)
        
    writeControl = writeText

    def writeArticle(self, a):
        if a.caption:
            self.out.write("")
            self._write(a.caption)
            self.out.write("")
            
        for x in a:
            self.write(x)

        self.out.write("\n")
        
    def writeStyle(self, s):
        if s.caption == "''": 
            tag = ''
        elif s.caption=="'''''":
            self.out.write("")
            for x in s:
                self.write(x)
            self.out.write("")
            return
        elif s.caption == "'''":
            tag = ''
        elif s.caption == ";":
            self.out.write("")
            for x in s:
                self.write(x)
            self.out.write("")
            return
        
        elif s.caption.startswith(":"):
            self.out.write(""*len(s.caption))
            for x in s:
                self.write(x)
            self.out.write(""*len(s.caption))
            return
        elif s.caption == "overline":
            self.out.write('')
            for x in s:
                self.write(x)
            self.out.write('')
            return
        else:
            tag = s.caption
    

        self.out.write("%s" % tag)
        for x in s:
            self.write(x)
        self.out.write("%s" % tag)

    def writeItem(self, item):
        self.out.write("")
        for x in item:
            self.write(x)
        self.out.write("\n")

    def writeItemList(self, lst):
        if lst.numbered:
            tag = ""
        else:
            tag = ""
            
        self.out.write("%s" % tag)
            
        for x in lst:
            self.write(x)
            self.out.write("\n")

        self.out.write("%s" % tag)


class NoLinksWriter(HTMLWriter):
    """Subclass that ignores (non-outgoing) links"""
    
    def writeLink(self, obj):
        if obj.target is None:
            return

        if obj.children:
            for x in obj.children:
                self.write(x)
        else:
            self._write(obj.target)

