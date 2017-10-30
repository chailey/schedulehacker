from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.log = ""
        self.file = open("classes.csv", "w+")
        self.file.write("courseName,className,units,description,section," +
                       "session,type,time,days,registered,instructor,location")

        self.count = 0

    def __del__(self):
        self.file.close()

    def getClasses(self, url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None

        try:
            bsObj = BeautifulSoup(html,"html.parser")
            for link in bsObj.findAll("a"):
                if 'href' in link.attrs:
                    if ('https://classes.usc.edu/term-20181/classes/' in link.attrs['href']):
                        print(link.attrs['href'])
                        self.addClasses(link.attrs['href'])

        except AttributeError as e:
            return None

    def addClasses(self, url): # Must be a url for a class
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None

        try:
            bsObj = BeautifulSoup(html,"html.parser")
            for link in bsObj.findAll("a"):
                if 'href' in link.attrs:
                    if ('https://classes.usc.edu/term-20181/course/' in link.attrs['href']):
                        #print("\t-" + link.attrs['href'])
                        self.addCourseToCsv(link.attrs['href'])
        except AttributeError as e:
            return None

    def addCourseToCsv(self, url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None

        url = url[:-1]

        try:
            bsObj = BeautifulSoup(html,"html.parser")

            courseName = url.rsplit('/', 1)[-1].upper()

            className = bsObj.find("h2", {"class": "single"}).get_text()

            units = bsObj.find("span", {"class": "units"}).get_text()

            description = bsObj.findAll("div", {"class": "catalogue"})
            section = bsObj.findAll("td", {"class": "section"})
            session = bsObj.findAll("td", {"class" : "session"})
            type = bsObj.findAll("td", {"class": "type"})
            time = bsObj.findAll("td", {"class": "time"})
            days = bsObj.findAll("td", {"class": "days"})
            registered = bsObj.findAll("td", {"class": "registered"})
            instructor = bsObj.findAll("td", {"class": "instructor"})
            location = bsObj.findAll("td", {"class": "location"})

            i = 0
            while (i < len(section)-1):
                self.addClassToFile(courseName, className, units, description[0], section[i],
                       session[i], type[i], time[i], days[i], registered[i], instructor[i], location[i])
                i += 1




        except AttributeError as e:
            return None

    def log(self, className):
        self.log += className + "\n"

    def addClassToFile(self, courseName, className, units, description, section,
                       session, type, time, days, registered, instructor, location):
        self.addToFile(courseName + "," + className.replace(',',"&#44") + "," + units + "," +
                  description.get_text().replace(',',"&#44")  + "," + section.get_text() + "," +
                  session.get_text() + "," + type.get_text() + "," + time.get_text() +
                  "," + days.get_text().replace(',',"&#44") + "," + registered.get_text() + "," +
                  instructor.get_text().replace(',',"&#44")  + "," + location.get_text())




    def addToFile(self, line):
        self.file.write("\n" + line)

test = Scraper()

test.getClasses("https://classes.usc.edu/term-20181/")

print(test.log)



