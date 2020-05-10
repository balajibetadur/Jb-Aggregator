# Libraries
import pandas as pd
from bs4 import BeautifulSoup

import urllib.request
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def scrape():
    if request.method=="POST":
        fe=request.form
        role=fe['role']
        place=fe['place']
        Shine = shine(place,role)
        Indeed = indeed(place,role)
        webs=['shine','indeed']
        all_jobs=[Shine,Indeed]
        add_to_excel(webs,all_jobs)

        return render_template('result.html',all_jobs=all_jobs)

    return render_template('index.html')



def indeed(place,role):

  job=''
  role=role.split(' ')
  for i in role:
    if i != role[-1]:
      job+=i+'+'
    else:
      job+=i  

  url = urllib.request.urlopen(f'https://www.indeed.co.in/jobs?q={job}&l={place}')
  soup = BeautifulSoup(url,'html.parser') 
  a=soup.find_all('td', attrs={'id': 'resultsCol'})
  jobs=[]
  b=soup.find_all('a', attrs={'class': 'jobtitle turnstileLink'})

  for i in a:
      loc = i.find_all('div', attrs={'class':'recJobLoc'})
      title=i.find_all('a', attrs={'class':'jobtitle turnstileLink'})
      date='not provided'
      comp = i.find_all('span', attrs={'class':'company'})
      desc = i.find_all('div', attrs={'class':'summary'})
      href=i.find_all('a', attrs={'class':'jobtitle turnstileLink'})
      tel='not provided'
      mail='not provided'
      web='not provided'
      skills='not provided'
      exp='not provided'
      sal='not provided'
      
      for o in range(0,len(b)):
          jobs.append([title[o].text.strip(),date,comp[o].text.strip(),tel,mail,web,loc[o]['data-rc-loc'],comp[o].text.strip(),skills,desc[o].text.strip(),sal,exp,'https://www.indeed.com'+ href[o]['href']])

  return pd.DataFrame(jobs)




def shine(place,role):
  
    job=''
    role=role.split(' ')
    for i in role:
        if i != role[-1]:
            job+=i+'-'
        else:
            job+=i  


    fhand = urllib.request.urlopen(f'https://www.shine.com/job-search/{job}-jobs-in-{place}')
    soup = BeautifulSoup(fhand,'html.parser') 
    jobs2=[]
    j=0
    regex = re.compile('^search_listing')
    content_lis = soup.find_all('li', attrs={'class': regex})

    for i in content_lis:

        if i!=None:

            
            title = i.find_all('li', attrs={'class': 'snp cls_jobtitle'})[0].text
            date = i.find_all('li', attrs={'class': 'time share_links jobDate'})          
            employer = i.find_all('li', attrs={'class': 'snp_cnm cls_cmpname cls_jobcompany'})         
            tel='not provided in dashboard'
            mailid='not provided in dashboard'
            web=i.find_all('li', attrs={'class': 'snp_cnm cls_cmpname cls_jobcompany'})[0].text
            loc=i.find_all('em')[0].text
            web=i.find_all('li', attrs={'class': 'snp_cnm cls_cmpname cls_jobcompany'})[0].text
            skill=[]
            skills = i.find_all('div', attrs={'class': 'sk jsrp cls_jobskill'})[0]
            skill=skills.text
            desc = i.find_all('li', attrs={'class': 'srcresult'})
            salary='not provided in dashboard'
            exp = i.find_all('span', attrs={'class': 'snp_yoe cls_jobexperience'})[0].text.strip()
            link = i.find('a', attrs={'class': 'cls_searchresult_a searchresult_link'})
        
            jobs2.append([title.strip(),date[j].get_text().strip(),employer[j].get_text().strip(),tel,mailid,web.strip(),loc.strip(),web.strip(),skill,desc[j].get_text().strip(),salary,exp,'https://www.shine.com'+ link['href']])

    return pd.DataFrame(jobs2)
    


def add_to_excel(webs,all_jobs):
    import os
    cwd = os.getcwd()
    path=cwd+'jobstest.xlsx'
    print(path)
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    number=0
    for jobs in all_jobs:
        jobs.columns=['Job Title','	Date','	Recruiter name','	Tel','	Mailid','	Website ','	Location','	Company	','Skills','	Desc','	Salary','	Experince','	Link']

        jobs.to_excel(writer, sheet_name=webs[number])
        
        print(f'{webs[number]} added to excel file')

        number+=1


    writer.save()


# if __name__=="__main__":
#   place='bangalore'
#   role='Java'
#   Shine = shine(place,role)
#   Indeed = indeed(place,role)
#   webs=['shine','indeed']
#   all_jobs=[Shine,Indeed]
#   add_to_excel(webs,all_jobs)
  

        

        #  try other websites //  hosting

   




if __name__ == "__main__":
    app.run(debug=True)
