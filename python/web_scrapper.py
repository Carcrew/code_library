import urllib2
import bs4
import codecs
import httplib
from urlparse import urlparse

############################Initialize
uid = 0
ext_links = {}
# url = 'https://boodmo.com/'
url = "compare.html"
url = 'http://www.oriparts.com'
ext_links[url] = 0
# ext_links['http://www.oriparts.com'] = 100000
orig_data_scrapper = {}
root_uid = 0
demo = []
Take_Tags = ['a', 'div', 'p', 'span', 'b']
Non_Take_Tags = ['script']
div = None
comment = None

skip_links_with_substrings = ['privacy', 'account', 'google', 'youtube', 'gmail', 'signin', 'login', 'setting', 'play.google.com', 'support.twitter.com', 'signup', 'itunes.apple.com',  'twitter.com/iTunesMovies', 'itunes', 'apple.com', 'http://oriparts.com/?search', 'www.oriparts.com/redirect']

##########################define Lambdas#######################
rem_nl = lambda s: " ".join((s.replace('\n', ' ')).split())


#################################################Functions##########

def checkUrl(url):
	try:
	    p = urlparse(url)
	    conn = httplib.HTTPConnection(p.netloc)
	    conn.request('HEAD', p.path)
	    resp = conn.getresponse()
	    return resp.status < 400
	except:
		return False

def body_from_external_link(url):
	'''
	Returns body element of page from url
	'''
	source = urllib2.urlopen(url).read()
	soup = bs4.BeautifulSoup(source, 'html.parser')
	return soup.body

def recursive_data_scrap_dfs(node):
	'''
	Function to scrap children of node
	'''
	# print '====>>  ', node
	global uid, ext_links, comment, div, demo, root_uid
	try:
		if isinstance(node, bs4.element.NavigableString):
			uid += 1
			print rem_nl(node)
			demo.append(rem_nl(node))
			return {uid : rem_nl(node)}
		data_scrapper = {}
		# print '------------>>>>>   ', node.name
		idx = 0
		for child in node.children:
			if isinstance(child, bs4.element.NavigableString) == False:
				if child.name == 'a':
					if checkUrl(child.get('href')):
						new_link = child.get('href')
						
						if ext_links.has_key(new_link) == False:
							leave = False
							for blocked_s in skip_links_with_substrings:
								if blocked_s in new_link:
									leave = True
									break
							if leave:
								continue
							print '->>>>>>>>>>>>>>>>>>>>>>>>>  NEW LINK starts    ', new_link
							root_uid += 1
							ext_links[new_link] = root_uid
							output = recursive_data_scrap_dfs(body_from_external_link(new_link))
							if output:
								orig_data_scrapper[root_uid] = output
							print '->>>>>>>>>>>>>>>>>>>>>>>>>  NEW LINK ends    ', new_link
					output = recursive_data_scrap_dfs(child)
					if output:
						uid += 1
						data_scrapper[uid] = output
				else:
					if child.name in Non_Take_Tags:
						continue
					uid += 1
					output = recursive_data_scrap_dfs(child)
					if output:
						data_scrapper[uid] = output
						# demo.append(output)

			else:
				if isinstance(child, list):
					for data in child:
						if rem_nl(data):
							print rem_nl(data)
							demo.append(rem_nl(data))
							uid += 1	
							data_scrapper[uid] = rem_nl(data)
				else:
					if rem_nl(child):
						print rem_nl(child)
						demo.append(rem_nl(child))
						uid += 1
						data_scrapper[uid] = rem_nl(child)
		# print '------->>>>>>end>>>>>>  ', node.name
		return data_scrapper
	except Exception as e:
		print e
		return ''

def main():
	global url, orig_data_scrapper	
	if checkUrl(url):
		source = urllib2.urlopen(url).read()
	else:
		source = codecs.open(url, 'r').read() #if local page url
	
	soup = bs4.BeautifulSoup(source, 'html.parser')
	# print soup.body.prettify()
	orig_data_scrapper[0] =  recursive_data_scrap_dfs(soup.body)
	# print tree
	# print ext_links
	# print orig_data_scrapper[0]
	print demo
	# print 'scrapped data : ', orig_data_scrapper
	# print 'external links : ', ext_links

	for link in ext_links.keys():
		print link , ' ------>>   ', orig_data_scrapper[ext_links[link]]

	# print '>>>>>>>>11   ', type(div), div
	# print '--------------------------------------------'
	# for child in div.children:
	# 	if isinstance(child, bs4.element.Tag):
	# 		print child.contents
	# 	else:
	# 		print child

	# print '>>>>>>>>22   ', type(comment), comment.contents

#########################main function##############



if __name__ == '__main__':
	main()





#remove code
				# for content in child.contents:
				# 	if isinstance(content, bs4.element.Tag):
				# 		if content.name in Non_Take_Tags:
				# 			continue			
				# 		a_s = [link.get('href') for link in content.findAll('a') if link.get('href')[:4]=='http']
				# 		for link in a_s:
				# 			if ext_links.has_key(link):
				# 				continue
				# 			root_uid += 1
				# 			ext_links[link] = root_uid
				# 			# orig_data_scrapper[root_uid] = recursive_data_scrap_dfs(body_from_external_link(link))
				# 		uid += 1
				# 		data_scrapper[uid] = recursive_data_scrap_dfs(content)
				# 	else:
				# 		if isinstance(content, list):
				# 			for data in content:
				# 				if rem_nl(data) != '':
				# 					demo.append(rem_nl(data))
				# 					uid += 1
				# 					data_scrapper[uid] = rem_nl(data)
				# 		else:
				# 			if rem_nl(content) != '':
				# 				demo.append(rem_nl(content))
				# 				uid += 1
				# 				data_scrapper[uid] = rem_nl(content)

