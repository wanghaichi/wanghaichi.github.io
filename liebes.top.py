import os
import re
import yaml

def convert_md(filePath):
	file = open(filePath, 'r')
	content = file.read()
	pattern = re.compile(r'---([\s\S]*)---\n([\s\S]*)')
	content = re.search(pattern, content)
	prefix = content.group(1)
	main = content.group(2)
	pattern = re.compile(r'[-`#\s]')
	# print(prefix)
	main = re.sub(pattern, "", main)
	mLen = min(len(main), 250)
	main = main.decode('utf-8')[0:mLen].encode('utf-8')

	pattern = re.compile(r'title:( *)(.*?)( *)\n')
	title = re.search(pattern, prefix).group(2)
	pattern = re.compile(r'date:( *)(.*?)( *)\n')
	date = re.search(pattern, prefix).group(2)
	pattern = re.compile(r'img:( *)(.*?)( *)\n')
	img = ""
	try: 
		img = "https://blog.liebes.top" + re.search(pattern, prefix).group(2)
	except:
		img = "img/portfolio-01.jpg"
	webSite = "https://blog.liebes.top"
	url = date[0:10]
	url = url.replace("-", "/")
	basename = os.path.basename(filePath)
	basename = os.path.splitext(basename)[0]

	return {
		'title': title,
		'date' : date,
		'main' : main,
		'url'  : webSite + "/" + url + "/" + basename,
		'src'  : img
	}

def change_html(html_path, mdList, totalCount):


	html = ""
	s = ""
	template = ""

	with open(os.getcwd() + "/source/_data/li-article.html", "r") as file:
		template = file.read()

	for idx, item in enumerate(mdList):
		tem = template
		tem = tem.replace("{title}", item['title'])
		tem = tem.replace("{url}", item['url'])
		tem = tem.replace("{content}", item['main'])
		tem = tem.replace("{src}", item['src'])
		s = s + tem
		if idx % 3 == 2:
			s = "<li>" + s + "</li>"
			html = html + s
			s = ""
	content = ""
	with open(html_path, 'r') as file:
		content = file.read()
	content = content.replace("{articles}", html)
	content = content.replace("{count}", str(totalCount))
	with open(html_path, 'w') as file:
		file.write(content)

def convert_links(filePath):
	links = {}
	template = ""
	html = ""
	with open(filePath + "/links.yaml", 'r') as file:
		links = yaml.load(file)
	
	with open(filePath + "/li-links.html", "r") as file:
		template = file.read()

	s = ""
	for idx, k in enumerate(links):
		tem = template
		tem = tem.replace("{link}", links[k]["link"])
		tem = tem.replace("{pic}", links[k]["avatar"])
		tem = tem.replace("{desc}", links[k]["descr"])
		tem = tem.replace("{name}", k)
		s = s + tem
		if idx % 3 == 2:
			s = "<li>" + s + "</li>"
			html = html + s
			s = ""
	if s != "":
		s = "<li>" + s + "</li>"
		html = html + s
		s = ""

	content = ""
	with open(os.getcwd() + "/liebes.top/index.html", "r") as file:
		content = file.read()

	content = content.replace("{links}", html.encode("utf-8"))
	
	with open(os.getcwd() + "/liebes.top/index.html", "w") as file:
		file.write(content)

def convert_gallery(filePath):
	links = {}
	template = ""
	html = ""
	with open(filePath + "/gallery.yaml", 'r') as file:
		links = yaml.load(file)
	
	with open(filePath + "/li-gallery.html", "r") as file:
		template = file.read()

	s = ""
	for idx, k in enumerate(links):
		tem = template
		tem = tem.replace("{src}", "https://blog.liebes.top%s"%links[k]["full_link"])
		s = s + tem
		if idx % 2 == 1:
			s = "<div class=\"col-md-4 wp4\">" + s + "</div>"
			html = html + s
			s = ""
		if idx == 5:
			break
	if s != "":
		s = "<div class=\"col-md-4 wp4\">" + s + "</div>"
		html = html + s
		s = ""
	content = ""
	with open(os.getcwd() + "/liebes.top/index.html", "r") as file:
		content = file.read()

	content = content.replace("{gallery}", html.encode("utf-8"))
	
	with open(os.getcwd() + "/liebes.top/index.html", "w") as file:
		file.write(content)

baseDir = os.getcwd()
mds = os.listdir(baseDir + "/source/_posts")
totalCount = len(mds)

mdList = []
for md in mds:
	md = baseDir + "/source/_posts" + "/" + md
	turple = convert_md(md)
	mdList.append(turple)
	
mdList = sorted(mdList, key = lambda item: item['date'], reverse=True)
mdList = mdList[0:6]

change_html(baseDir + "/liebes.top/index.html", mdList, totalCount)
convert_links(baseDir + "/source/_data")
convert_gallery(baseDir + "/source/_data")



