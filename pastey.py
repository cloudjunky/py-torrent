'''
dstar101@gmail.com
thepiratebay.org API
some shtty python script to get some info from tpb
'''

#thepiratebay CLi Client
'''
    Convert it into Module
'''
#TODO: Add Specific Page function
import BeautifulSoup as bs
import pickle
import urllib2
base_url = 'http://thepiratebay.org'
import sys
def parseNav(html):
    navLinks = [base_url+link['href'] for link in html.findAll("a")]

    return navLinks
def getDetails(html):
    html = str(html)
    soup = bs.BeautifulSoup(html)
    links = [str(tag['href']) for tag in soup.findAll("a")] #Get all links in a list
    for i in soup.findAll('font',{'class':"detDesc"}):
        det = str(i.contents[0])
        det = det.replace('&nbsp', '')
        det = det.replace('Uploaded', '')
        det = det.replace(';', ' ')
        det = det.split(',')
        #print det[0] #Uploaded at
        #print det[1] #Size
    ######################
    #print links[2] #Detail Page
    #print links[3] #Download Link
    #print links[6] #User Page
    ####################
    t = links[2].split('/')
    torrentName = t[-1] #or t = links[2].split('/') => t=t[-1]
    torrenrId = t[2]
    details = {}
    if len(links) == 7: #       if links have length of 7
        details["name"] = torrentName
        details["detaiLink"] = links[2]
        details['downloadLink'] = links[3]
        details['uploaderName'] = links[6].split('/')[-2] #!!
        details['uploaderPage'] = links[6]
        #details['date'] = det[0]
        #details['size'] = det[1]
        details['id'] = torrenrId
    else:
        details["name"] = torrentName
        details["detaillLink"] = links[2]
        details['downloadLink'] = links[3]
        details['uploaderName'] = links[5].split('/')[-2] #!1 ^^
        details['uploaderPage'] = links[5]
        #details['date'] = det[0]
        #details['size'] = det[1]
        details['id'] = torrenrId
    return details
 ########################################################
def start(soup,userPage=False):
    global nav
    menu = []           #Execution starts here
    for tag in soup.findAll("table",{'id':'searchResult'}):
        #I could have used
        #for s in tag.findAll("tr"): but it would have include first tr which
        #caused error so i am using for loop
        tr =  tag.findAll("tr")
        if userPage:
            nav = tr.pop()
            nav = parseNav(nav)
        menu = [getDetails(tr[i])for i in range(1,len(tr))]
        for i in range(1,len(tr)):
            menu.append(getDetails(tr[i]))
            x = getDetails(tr[i])
            #print x['id']
    #for i in menu:print i  #For Debugging
    return menu
def saveNav(nav,fileName="nav.bin"):
    pickle.dump(nav, open(fileName,"wb"))
def main():
    try:
        mode = int(sys.argv[1])
        url = sys.argv[2]
        output = sys.argv[3]
        output = output.lower()
    except Exception,e:
        print "Usage %s mode url \nMode is 1 for top100\t0 for userpage" % sys.argv[0]
        print "eg:\n%s 0 http://thepiratebay.org/user/YIFY/ true" % sys.argv[0]
        print "eg:\n%s 1 http://thepiratebay.org/top/all/ true" % sys.argv[0]
        print "\n\n\n"
        print e
        raw_input(">")
        sys.exit(0)

    print "************************************"
    print "[*]Started"
    print "************************************"
    print "[*]Sending Request"
    req = urllib2.Request(url)
    req.add_header('User-Agent',"Firefox 3")
    #fh = open(url)
    #html = str(fh.readlines())
    print "[*]Reading Response"
    html = str(urllib2.urlopen(req).read())
    soup = bs.BeautifulSoup(html)
    if mode == 1:
        print "[*}Mode is False\n[*]Parsing Top 100 From url: %s" % url
        x = start(soup)
        if output == "true":
            print "\n[*}Printing top 100"
            for i in x:
                print i
        print "\n\n\n"
        print "[*]Saving Top 100 as top100.bin"
        saveNav(x, "top100.bin")
    elif mode == 0: #and 'user' in url:
        print "[*]Mode is True"
        print "[*}Parsing page for user url %s" % url
        x = start(soup,True)
        print "[*]Done Parsing"
        print "[*]Saving Nav Panel"
        if output == "true" and mode == 0:
            print "[*]Printing Response"
            print "====================="
            print x
            print "\n\n============================"
            print "[*]NavPanel"
            print "\n\n================================="
            print nav
        saveNav(nav)
        print "\n\n[*]Done"
    else:print"Sleep with fishes"
if __name__ == '__main__':
    main()
