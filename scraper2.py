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
                        self.addCourseToCsv(url, link.attrs['href'])
        except AttributeError as e:
            return None

    def addCourseToCsv(self, url, urlCourseName):
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None

        urlCourseName = urlCourseName[:-1]

        try:
            bsObj = BeautifulSoup(html,"html.parser")

            courseName = urlCourseName.rsplit('/', 1)[-1].upper()
            print("\t-" + courseName)

            classObj = bsObj.find("div", {"id": courseName})

            className = classObj.find("div", {"class": "course-id"}).get_text()

            units = classObj.find("span", {"class": "units"}).get_text()

            description = classObj.findAll("div", {"class": "catalogue"})
            section = classObj.findAll("td", {"class": "section"})
            session = classObj.findAll("td", {"class" : "session"})
            type = classObj.findAll("td", {"class": "type"})
            time = classObj.findAll("td", {"class": "time"})
            days = classObj.findAll("td", {"class": "days"})
            registered = classObj.findAll("td", {"class": "registered"})
            instructor = classObj.findAll("td", {"class": "instructor"})
            location = classObj.findAll("td", {"class": "location"})

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
        self.addToFile(courseName.replace(',',"&#44") + "," + className.replace(',',"&#44") + "," +
                       units.replace(',',"&#44") + "," + description.get_text().replace(',',"&#44")  +
                       "," + section.get_text() + "," + session.get_text() + "," + type.get_text() +
                       "," + time.get_text() + "," + days.get_text().replace(',',"&#44") +
                       "," + registered.get_text() + "," + instructor.get_text().replace(',',"&#44")
                       + "," + location.get_text())




    def addToFile(self, line):
        self.file.write("\n" + line)

test = Scraper()

test.getClasses("https://classes.usc.edu/term-20181/")

print(test.log)
