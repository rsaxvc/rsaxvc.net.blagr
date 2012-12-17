import os
import fileinput
import glob
import shutil
from pyatom import AtomFeed
from datetime import datetime

#configuration
BLOG_TITLE      = "RSAXVC Development"
BLOG_SUBTITLE   = "Software, Hardware, Radios, Algorithms"
BLOG_FEED_URL   = "http://rsaxvc.net/blog/atom.xml"
BLOG_URL        = "http://rsaxvc.net/blog/"
BLOG_AUTHOR     = "rsaxvc"

PATH_BASE       = "../blog/"
POST_PATH_BASE  = PATH_BASE
TAG_PATH_BASE   = PATH_BASE + "tags/"
CSS_PATH_BASE   = PATH_BASE + "css/"
ATOM_PATH		= PATH_BASE + "atom.xml"

INPUT_PATH_BASE = "input/"
INPUT_CSS_PATH  = INPUT_PATH_BASE + "css/"
INPUT_POST_PATH = INPUT_PATH_BASE + "posts/"
INPUT_INC_TAIL_PATH = INPUT_PATH_BASE + "inc/tail/"

shutil.rmtree(PATH_BASE,True)

#Contains a single post
class post:
	author = ""
	title = ""
	tags = []
	text = ""
	dt = ""
	def __cmp__(self, other):
		if( self.dt < other.dt ):
			return 1
		elif( self.dt == other.dt ):
			return 0
		else:
			return -1

	def relpath(self):
		return str(self.dt.year) + "/" + str(self.dt.month) + "/" + str(self.dt.day) + "/" + str(self.title) + ".html"

	def path(self):
		return POST_PATH_BASE + self.relpath()

	def wobpath(self):
		return BLOG_URL + self.relpath()

	def has_tag(self, search_tag):
		for tag in self.tags:
			if( tag == search_tag ):
				return True
		return False

class tag:
	text = ""
	def __init__(self,the_text):
		self.text = the_text
	def __cmp__(self,other):
		if( self.text < other.text ):
			return -1
		elif( self.text == other.text ):
			return 0
		else:
			return 1
	def path(self):
		return TAG_PATH_BASE + self.text + ".html"
	def __str__(self):
		return self.text

def parse_blagr_tophalf_line( line ):
	(first,sep,last) = line.partition(':')
	if( len(last) == 0 or len(sep) == 0 ):
		print "error parsing file:",first
	else:
		return (first,last.rstrip("\n"))

def parse_blagr_entry( filename ):
	"parse a blagr entry file into a structure"
	p = post()
	p.tags = []
	post_sep_found = False
	for line in fileinput.input(filename):
		if( post_sep_found == False ):
			if( line == "---\n" ):
				post_sep_found = True
			else:
				(chunk,text) = parse_blagr_tophalf_line( line )
				if( chunk == "Tag" ):
					p.tags.append( tag( text ) )
				elif( chunk == "Author" ):
					p.author = text
				elif( chunk == "CreatedDateTime" ):
					p.dt = datetime.strptime( text, "%Y-%m-%dT%H:%M:%S" )
				elif( chunk == "Title" ):
					p.title = text
		else:
			p.text += line
	return p

def globulate_tags( posts ):
	"Build a list of all tags from all posts"
	tags = []
	for post in posts:
		for tag in post.tags:
			if( tags.count( tag ) == 0 ):
				tags.append( tag )
	return tags

def generate_html_start( f, title, path_depth ):
	"Writes common header/title/css-includes/..."
	upbuffer = ""
	for i in range(path_depth):
		upbuffer += "../"
	f.write( "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n" )
	f.write( "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">\n" )
	f.write( "<head>\n" )
	f.write( "<meta http-equiv=\"Content-type\" content=\"text/html;charset=UTF-8\" />\n")
	f.write( "<title>"+title+"</title>\n")
	f.write( '<LINK href="' + upbuffer + CSS_PATH_BASE + 'blog.css" rel="stylesheet" type="text/css">')
	f.write( "</head><body>\n" )

def parse_inc_directory( dir ):
	the_text = ""
	for infile in glob.glob( os.path.join( dir, '*.inc') ):
		print "Parsing: " + infile
		f = open( infile )
		the_text += f.read()
		f.close()
	return the_text


def generate_html_end( f, last_body_text ):
	"terminate the html document"
	f.write( last_body_text )
	f.write( "</body></html>\n" )

def generate_tag_html( f, tag, posts, path_depth ):
	"makes the html for a tag page"
	f.write( "<h4>Posts tagged with " + tag.text + "</h4>\n" )
	f.write( "<ul>\n" )
	upbuffer = ""
	for i in range(path_depth):
		upbuffer += "../"
	for post in posts:
		if( post.has_tag( tag ) ):
			f.write( "<li><a href=\""+upbuffer+post.path()+"\">"+post.title+"</a></li>\n" )
	f.write("</ul>\n")

def write_tag_html( tag, posts, end_text ):
	"makes the file and writes the text for a tag page"
	filename = tag.path()
	if( os.path.exists( os.path.dirname( filename ) ) == False ):
		os.makedirs( os.path.dirname( filename ) )
	f = open(filename, 'w')
	generate_html_start( f, "Tag listing for "+tag.text, 1 )
	generate_tag_html( f, tag, posts, 1 )
	generate_html_end( f, end_text )
	f.close()
	
def generate_post_html( f, post, path_depth ):
	"makes the html for a post"
	upbuffer = ""
	for i in range(path_depth):
		upbuffer += "../"
	f.write('<div class="post">')
	f.write('<h1 class="title"><a href=\"'+upbuffer+post.path()+"\">" + post.title + "</a></h1>\n" )
	f.write('<h4 class="post_date"> Written '+str(post.dt.date())+"</h4>\n" )
	f.write('<h4 class="tag_list"> Tags:')
	for tag in post.tags:
		f.write( "<a href=\"" + upbuffer + tag.path()+"\">" + tag.text + "</a>&nbsp;" )
	f.write("</h4>\n")
	f.write('<div class="body_text">')
	f.write(post.text)
	f.write("</div>")
	f.write("</div>")

def write_post_html( post, end_text ):
	"makes the file and writes the text for a post"
	filename = post.path()
	if( os.path.exists( os.path.dirname( filename ) ) == False ):
		os.makedirs( os.path.dirname( filename ) )
	f = open( filename, 'w' )
	generate_html_start( f, post.title, 3 )
	generate_post_html( f, post, 3 )
	generate_html_end( f, end_text )
	f.close()

def write_posts_html( filename, title, posts, end_text ):
	"writes all the posts"
	if( os.path.exists( os.path.dirname( filename ) ) == False ):
		os.makedirs( os.path.dirname( filename ) )
	f = open( filename, 'w' )
	generate_html_start( f, title, 0 )
	for post in posts:
		generate_post_html( f, post, 0 )
	generate_html_end( f, end_text )
	f.close()

posts = []
for infile in glob.glob( os.path.join(INPUT_POST_PATH, '*.blagr') ):
	print "Parsing: " + infile
	posts.append( parse_blagr_entry( infile ) )

posts.sort()

end_text = parse_inc_directory( INPUT_INC_TAIL_PATH )

for post in posts:
	write_post_html( post, end_text )
write_posts_html( POST_PATH_BASE + "index.html", BLOG_TITLE, posts, end_text )

tags = globulate_tags( posts )
tags.sort()
for tag in tags:
	write_tag_html( tag, posts, end_text )

feed = AtomFeed(title=BLOG_TITLE,
	subtitle=BLOG_SUBTITLE,
	feed_url=BLOG_FEED_URL,
	url=BLOG_URL,
	author=BLOG_AUTHOR)

for post in posts:
	feed.add(title=post.title,
		content=post.text,
		content_type="html",
		author=post.author,
		url=post.wobpath(),
		updated=post.dt
		)

f = open(ATOM_PATH, 'w')
f.write( feed.to_string() )
f.close()

shutil.copytree( INPUT_CSS_PATH, CSS_PATH_BASE )
