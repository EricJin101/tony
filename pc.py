import re,urllib,threading
from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = 0 # lable flag
        self.content_flag= 0 #content flag
        self.links = []
        self.title=""
        self.img=[]
        self.content=[]
        self.linkcontent=[]
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0: pass
            else:
                for (variable, value)  in attrs:
                    if variable == "href":
                        self.links.append(value)
                        self.flag=4
        if tag == "ul":
            if len(attrs)==0:pass
            else:
                for(varviable,value) in attrs:
                    if varviable=="class" and (value=="info" or value=="description"):
                        self.flag=3
                        self.content_flag=1
        if tag == "div":
            if len(attrs)==0:pass
            else:
                for(varviable,value) in attrs:
                    if varviable=="class":
                        if value=="content" or value=="author" or value=="conleft":
                            self.flag=3
                            self.content_flag=1
        if tag=="meta":
            if len(attrs)==0:pass
            else:
                for (variable,value) in attrs:
                    if variable=="content":
                        pass#self.title=value
        if tag=="title":
            self.flag=1
        if tag=="img":
            if len(attrs)==0:pass
            else:
                # img_host=u'http://pic.58.com/'
                for(variable,value) in attrs:
                    if variable=="src":
                        self.img.append(value)
        if tag=="p":
            if self.flag==3:
                self.flag=2
        if tag=="br":
            if self.content_flag==1:
                self.flag=2
    def handle_endtag(self, tag):
        if tag=="p":
            if self.content_flag==1:
                self.content_flag=0
    def handle_data(self,data):
        if self.flag==1:
            self.title=data
            self.flag=0
        if self.flag==3:
            self.content.append(data)
            self.flag=0
        if self.flag==4:
            self.linkcontent.append(data)
            self.flag=0
def getimageurl(img):
    reg='^http:\/\/\w{3}\.\w{9}\.com\/\w{6}\/\w{8}.*?'
    imageurl = []
    for i in range(len(img)):
        list = re.compile(reg).findall(img[i])
        # print len(list)
        if len(list) == 0:
            continue
        imageurl.append(img[i])
    return imageurl
url = ['http://www.qiushibaike.com/imgrank',]
def getlist(url):
    lParser = MyHTMLParser()
    lParser.feed(urllib.urlopen(url).read().decode('utf-8'))
    lParser.close()
    # print lParser.linkcontent[10]
    # print lParser.img
    imageurllist = getimageurl(lParser.img)
    num = range(len(imageurllist))
    for a in num:
        urllib.urlretrieve(imageurllist[a],'E://images/b%d.jpg' % (a))
    # for list in lParser.img:
    #     print list
def main():
    threads=[]
    nloops=range(len(url))
    for i in nloops:
        t = threading.Thread(target=getlist,args=[url[i],])
        threads.append(t)
    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()
if __name__ == '__main__':
    main()
