def all_users():
	list_user = db(db.auth_user).select().as_list()
	return dict(list_user=list_user)

def test_credentials():
	u_name = request.vars.u
	pw = request.vars.pw
	print('rq',u_name)
	print('rq',pw)
	test = auth.login_bare(u_name,pw)
	#untuk logout: ke mambo/default/user.json/logout
	return dict(t=test)

@auth.requires_membership('kepala_sekolah')
def test_something():
	return dict(a='ok')
	