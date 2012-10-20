import os
import fileinput
import glob
import shutil
from datetime import datetime

BLOG_TITLE      = "RSAXVC Development"
POST_PATH_BASE  = "posts/"
TAG_PATH_BASE   = "tags/"
INPUT_PATH_BASE = "input/"

shutil.rmtree(POST_PATH_BASE,True)
shutil.rmtree(TAG_PATH_BASE,True)

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

	def path(self):
		return POST_PATH_BASE + str(self.dt.year) + "/" + str(self.dt.month) + "/" + str(self.dt.day) + "/" + str(self.title) + ".html"

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

def generate_html_start( f, title ):
	f.write( "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n" )
	f.write( "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">\n" )
	f.write( "<head>\n" )
	f.write( "<meta http-equiv=\"Content-type\" content=\"text/html;charset=UTF-8\" />\n")
	f.write( "<title>"+title+"</title>\n")
	f.write( "</head><body>\n" )

def generate_html_end( f ):
	f.write( "</body></html>\n" )

def generate_tag_html( f, tag, posts, path_depth ):
	f.write( "<h4>Posts tagged with " + tag.text + "</h4>\n" )
	f.write( "<ul>\n" )
	upbuffer = ""
	for i in range(path_depth):
		upbuffer += "../"
	for post in posts:
		if( post.has_tag( tag ) ):
			f.write( "<li><a href=\""+upbuffer+post.path()+"\">"+post.title+"</a></li>\n" )
	f.write("</ul>\n")

def write_tag_html( tag, posts ):
	filename = tag.path()
	if( os.path.exists( os.path.dirname( filename ) ) == False ):
		os.makedirs( os.path.dirname( filename ) )
	f = open(filename, 'w')
	generate_html_start( f, "Tag listing for "+tag.text )
	generate_tag_html( f, tag, posts, 1 )
	generate_html_end( f )
	f.close()
	
def generate_post_html( f, post, path_depth ):
	upbuffer = ""
	for i in range(path_depth):
		upbuffer += "../"
	f.write("<h1>"+post.title+"</h1>\n" )
	f.write("<h4> Written "+str(post.dt.date())+"</h4>\n" )
	f.write("<h4> Tags:")
	for tag in post.tags:
		f.write( "<a href=\"" + upbuffer + tag.path()+"\">" + tag.text + "</a>&nbsp;" )
	f.write("</h4>\n")
	f.write(post.text)

def write_post_html( post ):
	filename = post.path()
	if( os.path.exists( os.path.dirname( filename ) ) == False ):
		os.makedirs( os.path.dirname( filename ) )
	f = open( filename, 'w' )
	generate_html_start( f, post.title )
	generate_post_html( f, post, 4 )
	generate_html_end( f )
	f.close();

def write_posts_html( filename, title, posts ):
	if( os.path.exists( os.path.dirname( filename ) ) == False ):
		os.makedirs( os.path.dirname( filename ) )
	f = open( filename, 'w' )
	generate_html_start( f, title )
	for post in posts:
		generate_post_html( f, post, 1 )
	generate_html_end( f )
	f.close()
	
posts = []
for infile in glob.glob( os.path.join(INPUT_PATH_BASE, '*.blagr') ):
	print "Parsing: " + infile
	posts.append( parse_blagr_entry( infile ) )

posts.sort()
for post in posts:
	write_post_html( post )
write_posts_html( POST_PATH_BASE + "index.html", BLOG_TITLE, posts )

tags = globulate_tags( posts )
tags.sort()
for tag in tags:
	write_tag_html( tag, posts )
