
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import os

con = None

try:

	con = mdb.connect('localhost', 'root', 'worstrootpassword', 'movabletype');

	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute("select * from mt_entry JOIN mt_author ON author_id = entry_author_id ")

	numrows = int(cur.rowcount)
	for i in range(numrows):
		row = cur.fetchone()
		filename = str(row["entry_title"])
		filename = filename.replace('/','')
		f = open("output/%s.blagr" % (filename), 'w' )
		f.write( "Title:%s\n" % (row["entry_title"]) )
		f.write("Author:%s\n" % (row["author_name"]) )
		f.write("CreatedDateTime:%s\n" % (row["entry_created_on"].isoformat()) )
		f.write("ModifiedDateTime:%s\n" % (row["entry_modified_on"].isoformat()) )
		minicur = con.cursor(mdb.cursors.DictCursor)
		minicur.execute("select tag_name from mt_objecttag join mt_tag on tag_id = objecttag_tag_id where objecttag_object_datasource = \"entry\" and objecttag_object_id = %i;" % (row["entry_id"]) )
		mininumrows = int(minicur.rowcount)
		for j in range(mininumrows):
			minirow = minicur.fetchone()
			f.write("Tag:%s\n" % (minirow["tag_name"]) )
		minicur.close()
		f.write( "---\n" )
		f.write("%s\n" % (row["entry_text"]) )
		f.close()
except mdb.Error, e:

	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
    
finally:    
	if con:    
		con.close()
