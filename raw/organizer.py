import os
import re
import shutil
from datetime import datetime
import pypandoc

if __name__ == '__main__':
    if os.path.exists("../_posts"):
        shutil.rmtree("../_posts")
        os.mkdir("../_posts")
    # start from project dir
    for year in os.listdir():
        if os.path.isdir(year):
            for book in os.listdir(year):
                if os.path.isdir(year + "/" + book):
                    for parsha_raw in os.listdir(year + "/" + book):
                        match_object = re.match(r'\d.\s(.*)\sשנה.*.docx', parsha_raw)
                        if match_object:
                            # Makes folder
                            parsha_name = match_object.groups()[0]
                            if not os.path.exists("../_posts/" + parsha_name):
                                os.mkdir("../_posts/" + parsha_name)

                            # Copies the file into the new folder structure

                            old_path = year + "/" + book + "/" + parsha_raw
                            #old_path = "../_posts/" + parsha_name + "/" + parsha_raw

                            c_date = datetime.fromtimestamp(os.stat(old_path).st_birthtime)
                            #new_name = c_date.year + "-" + c_date.month + "-" + c_date.day + "-" + parsha_name + "/" + \
                            #           year[-2] + ".docx"

                            shutil.copy(old_path, "../_posts/" + parsha_name)


                            # Convert it to html

                            # Open in pandox and add the docx

                            txt = pypandoc.convert_file(old_path, to = 'plain', format = 'docx')

                            title = txt.partition('\n')[0]

                            # Extract the title
                            new_name = "{}-{}-{}-{}-{}.html".format(c_date.year, c_date.month, c_date.day, parsha_name, title)
                            os.rename("../_posts/"+parsha_name + "/" + parsha_raw, "../_posts/" + parsha_name + "/"+new_name)


                            # Adding front matter

                            front_matter = "---\nlayout: post\ntitle:" + title.split(':')[1] + "\n---\n"
                            html = pypandoc.convert_file(old_path, to = 'html', format = 'docx')

                            html = ''.join(html.partition('</p>')[1:])[4:]
                            f = open("../_posts/" + parsha_name + "/"+new_name, 'w')
                            f.write(front_matter)
                            f.write(html)

