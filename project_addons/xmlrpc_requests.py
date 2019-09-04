import functools
import xmlrpc.client
HOST = 'localhost'
PORT = 8069
DB = 'exercicedb'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print("Logged in as %s (uid:%d)" % (USER,uid))

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# Reading sessions
sessions = call('models.session','search_read', [], ['name','seats'])
for session in sessions:
    print("Session %s (%s seats)" % (session['name'], session['seats']))

# Creating a course
course_id = call('models.course', 'create', {
    'name': 'Odootest'
})

# Creating a new session for the "Odootest" course
course_id = call('models.course', 'search', [('name','ilike','Odootest')])[0]
session_id = call('models.session', 'create', {
    'name': 'My session3',
    'course_id': course_id,
})
