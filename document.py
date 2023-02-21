import glob
import re
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file',  type=str, help='Add the main entrypoint of the api file most probbaly app.js or index.js')
parser.add_argument('baseurl', type=str, help='Add API base url')
args = parser.parse_args()
#baseurl="http://65.2.38.131:3000"

#maxdepth 2
def compile(text):
    
    varlist=re.findall(f".+=.require....+",text)
    for i in varlist:
        vv=(i.replace("var","").replace("const","").replace("let","")).split("=")
        for i in range(len(vv)):
            #print(vv[0].strip(),vv[1].replace(";",""))
            text=text.replace(str(vv[0].strip()),str(vv[1].replace(";","")))
    return text.replace("'",'"')
def require(fi):
    return compile(open(fi,"r").read())
def clean(text):
    d=re.findall(r'"(.*?)"',text)
    if len(d)==0:pass
    else:return str(d[0])
    
def getEndpoints(entrypoint,baseurl):
    x=open(entrypoint,"r").read()
    dd=re.findall(r'app[.]..............+[A-Za-z0-0"]',x)
    
    routelist=[]
    endpoints=[]
    for i in dd:
        d=re.findall(r'"(.*?)"',i)
        
        if(len(d)==2):
            routelist.append((d[1]))
            ddd=re.findall(r'router[.]..............+[A-Za-z0-0"]',compile(open(d[1]+'.js','r').read()))
            
            for i in ddd:
                var = i.split(",")
                bb=compile(open(d[1]+'.js','r').read())
                
##                varval=[x.split("=")[1] for x in re.findall(f".+=.+",bb) if x.split("=")[0].find(var)!=-1]
##                print([x.replace("require(","").replace(");","").replace(";","").replace(")","") for x in varval])
                
                #print(i)
                print(baseurl+d[0]+str(clean(var[0]))+" ==> "+str(clean(var[1]))+".js")
                endpoints.append(baseurl+d[0]+str(clean(var[0])))
        else:
            if len(d)>0:endpoints.append((baseurl+d[0]))
            else:pass
    return endpoints
            



if(args.file and args.baseurl):
    print(getEndpoints(args.file,args.baseurl))
