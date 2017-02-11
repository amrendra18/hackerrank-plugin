import json
import requests
import sys,os

"""
data = {"code":"print \"AMY\"","language":"python","customtestcase":"false"}
encoded_data = json.dumps(data)
print encoded_data
"""

filename = ""
problem = ""
language = ""
data = ""
response = ""

LANG = {}
LANG['c']='c'
LANG['cpp']='cpp'
LANG['cc']='cpp'
LANG['py']='python'
LANG['java']="java"
LANG['csharp']='cs'
LANG['php']='php'
LANG['rb']='ruby'
LANG['pl']='perl'
LANG['hs']='haskel'
LANG['clj']='clojure'
LANG['scala']='scala'
LANG['lua']='lua'
LANG['go']='go'
LANG['js']='javascript'
LANG['erl']='erlang'
LANG['lisp']='sbcl'
LANG['cl']='sbcl'
LANG['d']='d'
LANG['ocamal']='ocaml'
LANG['pas']='pascal'
LANG['pp']='pascal'
#LANG['py']='python3'
LANG['groovy']='groovy'
LANG['m']='objectivec'
LANG['fs']='fsharp'
LANG['vb']='visualbasic'
LANG['lol']='lolcode'
LANG['lols']='lolcode'
LANG['st']='smalltalk'
LANG['tcl']='tcl'


# gets argument of the file to be compiled and run
def getSubmission():
    global filename,problem,language, data
    try:
        full = sys.argv[1]
        filename = full[full.rfind('/')+1:]
	#print full,filename
        parts = filename.split('.')
        problem = parts[0]
        language = LANG[parts[1]]
        data = open(full,'r').read()
	#print data
	#exit(0)
    except:
        print "Error reading input file"
        exit(0)

# fetch the submission 
getSubmission()

#prepare json data to be sent as post request
tobesent = {}
tobesent["code"] = str(data)
tobesent["language"] = str(language)
tobesent["customtestcase"]=False
encoded_data = json.dumps(tobesent)
#print tobesent,encoded_data



#begin a session, so as to maintain common state between consecutive visits
s = requests.Session()

#making post request
def postData(url,data,headers):
    r = s.post(url, data=encoded_data, headers=headers)
    try:
    	return json.loads((r.text))
    except:
	print "Error: No such problem exists, or server is too busy. exiting..."
	exit(0)
    

#making get request
def getData(url):
    r = s.get(url,headers={'Content-Type': 'text/plain; charset=utf-8 ','User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36','Accept': '*/*','Accept-Encoding': 'gzip,deflate,sdch' })
    try:
    	return json.loads((r.text.decode('utf-8')))
    except:
	print "Error: No such problem exists, or server is too busy. exiting..."
	exit(0)

submit_url = "https://www.hackerrank.com/rest/contests/master/challenges/"+problem+"/compile_tests/"
headers = {'Content-Type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
           }


response = postData(submit_url,encoded_data,headers);
status = response['status']

if status == True:
    model_status = response['model']['status']
    model_id = response['model']['id']
    print "submission made with id %d"%(model_id)
    fetch_url = submit_url+str(model_id)
    result = ""
    while True:
        result = getData(fetch_url)
        r_status = result['status']
        if r_status == False:
            print "Unexpected Error in fetching the result"
            break
        current_status = int(result['model']['status'])
        if current_status == 1:
            break
        print "present status --> "+result['model']['status_string']

    COMPILE_MSG = result['model']['compilemessage']
    STDIN = result['model']['stdin']
    EXP_OUTPUT = result['model']['expected_output']
    OUTPUT = result['model']['stdout']
    RESULT = result['model']['testcase_message']
    
    print "\n*********************************************"
    print "STDIN : ",json.dumps(STDIN)
    print "Expected Output : ",json.dumps(EXP_OUTPUT)
    print "Your Output : ",json.dumps(OUTPUT)
    print "Result : ",json.dumps(RESULT)
    print "*********************************************"
else:
    print "Un-expected error occured, contact developer"

