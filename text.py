
import re
import argparse
import webbrowser
from filestack import Client
client = Client("AO0lhLyhmQJqnVt7juhQHz")

params = {'mimetype': 'text/plain'}

parser = argparse.ArgumentParser()
parser.add_argument('file',  type=str, help='Add the main entrypoint of the api file most probbaly app.js or index.js')
parser.add_argument('baseurl', type=str, help='Add API base url')
args = parser.parse_args()
def generate(file,baseurl):
        y=open(file,"r")
        x=y.read()
        
                
        ss=re.findall(r'app\.(?:get|post).*',x)
        y.close()
        #print(ss)
        html='''<style>
                        .GETspan{
                          border: 2px solid orange;
                          border-radius:13px;
                          padding: 10px;
                          color:white;
                          background: orange;
                        }
                        .GEThide{
                          display:none;
                        }
                        .POSTspan{
                          border: 2px solid blue;
                          border-radius:13px;
                          padding: 10px;
                          color:white;
                          background: blue;
                        }
                        .GETapi{
                          width: 70%;
                          margin-left: auto;
                          margin-right: auto;
                          padding: 20px;
                          border: 2px solid orange;
                          border-radius:13px;
                          margin-bottom:10px;
                          box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
                        }
                         .POSTapi{
                          width: 70%;
                          margin-left: auto;
                          margin-right: auto;
                          padding: 20px;
                          border: 2px solid blue;
                          border-radius:13px;
                          margin-bottom:10px;
                          box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
                        }
                        h4{
                          font-style: italic;
                           font-family: "Courier New", Courier, monospace;
                        }
                        .endpoint{
                              font-size:20px;
                              font-family: "Courier New", Courier, monospace;
                        }


                        </style>'''


        for post in ss:
                try:
                        a,t='',''
                        i=x.find(post)
                        v=0
                        while a!="})":
                                
                                if a=="({":
                                        v+=1
                                a=x[i]+x[i+1]
                                t+=x[i]
                                i+=1
                                if v>=1 and a=="})":
                                        a=''
                                        v-=1
                        t+=x[i]
                        #print(t)
                        auth=re.findall(r"app.+",t)[0].split(",")
                        method="GET" if "get" in auth[0] else "POST"
                        
                        if len(auth)==4:
                                auth=re.findall(r"app.+",t)[0].split(",")[1]
                        else:auth=False
                         

                        endpoint=baseurl+re.findall(r'\".*\"',re.findall(r"app.+",t)[0])[0].replace('"','')
                        cc=re.findall(r"new .+\(",t) if len(re.findall(r"new .+\(",t))>0 else re.findall(r"await .+\.find",t)
                        #print()
                        schema=cc[0].replace("await",'').replace(".find","").replace("new ","").strip()
                        if "(" in schema:
                                schema=re.findall(r"^(.*?)\(",cc[0])[0].replace("new ","").strip()+"SH"
                        else:schema+="SH"
                        #print(schema)
                        ss=re.findall(f'const {schema}.+\=.+',x) if len(re.findall(f'const {schema}.+\=.+',x))>0 else re.findall(f'const {schema}\=.+',x)
                        if len(ss)==0:
                                schema=schema.replace("SH","schema")
                                ss=re.findall(f'const {schema}.+\=.+',x) if len(re.findall(f'const {schema}.+\=.+',x))>0 else re.findall(f'const {schema}\=.+',x)
                        
                        #print(ss)
                        a=''
                        t=''
                        i=x.find(ss[0])
                        v=0
                        while a!="})":

                                if a=="({":
                                        v+=1
                                a=x[i]+x[i+1]
                                t+=x[i]
                                i+=1
                                if v>=1 and a=="})":
                                        a=''
                                        v-=1
                        t+=x[i]
                        body=re.findall(r'\([^)]*\)',t)[0].replace("(","").replace(")","")
                        authstatus='content-type:application/json' if not auth else f"Authorization:{auth}\n,content-type:application/json" 
                        html+=f'''

                        <div class="{method}api">
  <h3 class="endpoint">
  <span class="{method}span">{method}</span> {endpoint}
</h3>
<hr>
<h4>HEADERS:
<hr></h4>
  <pre contenteditable="true"><h3>
{authstatus}
</h3>
</pre>
<hr>
<h4 class="{method}hide">BODY:
<hr></h4>
<pre class="{method}hide" contenteditable="true">
  <h3>
{body}
  </h3>
  </pre>
<h4>Description:
<hr></h4>
<p contenteditable="true">if the endpoint have [[ /:something ]] <-- this type of syntex you must replace it with the actual value\n
now if it wants Authorization token that means you have to pass a authentication token which ig gevn at the time of login,
</p>
<b>**NOTE:</b><span>You can edit the avobe description as well as body and headers, after editing just press ctrl+s it will save on your local pc </span>
</div>'''
                        
                        
                except:pass
        
        return html


if(args.file and args.baseurl):
        
        with open("Documentation_of_"+re.findall(r'([A-Za-z]+(\.[A-Za-z]+)+)',args.baseurl)[0][0]+'.html',"w") as x:
                x.write(generate(args.file,args.baseurl))
        new_filelink =client.upload(filepath="Documentation_of_"+re.findall(r'([A-Za-z]+(\.[A-Za-z]+)+)',args.baseurl)[0][0]+'.html',store_params=params)
        print(new_filelink.url)
        print("Document generated \nDocumentation_of_"+re.findall(r'([A-Za-z]+(\.[A-Za-z]+)+)',args.baseurl)[0][0]+'.html')
        #webbrowser.open("Documentation_of_"+re.findall(r'([A-Za-z]+(\.[A-Za-z]+)+)',args.baseurl)[0][0]+'.html')
