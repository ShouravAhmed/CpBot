import urllib
from urllib.request import urlopen as Ureq, Request
import json
import time
import random
import threading

#------------------
import datetime
import webbrowser
#------------------

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

def get_json(url):
	req = Request(url, headers=hdr)
	page = Ureq(req)
	try:
		js = page.read().decode()
		js = json.loads(js)
	except:
		js = None
	return js

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

user_solve = set()
user_rating = 600
contest_list = dict()
problem_list = list()
solved_tags = dict()

# -----------------------------------------------------------------------------
def get_user_solve(username):
	url = "https://codeforces.com/api/user.status?handle=" + username

	print("calling for ", username ," solved problems.")
	start_time = time.time()

	js = get_json(url)
	if not js or "status" not in js or js["status"] != "OK":
		return

	print("--- %s seconds ---" % (time.time() - start_time))
	print("got ", username, " solved problems.")

	oldsz = len(user_solve)
	time_lim = time.time() - (10*24*60*60)

	for submission in js["result"]:
		if submission["verdict"] == "OK":
			user_solve.add(str(submission["problem"]["contestId"])+submission["problem"]["index"])

			if submission["creationTimeSeconds"] >= time_lim:
				try:
					for tag in submission["problem"]["tags"]:
						solved_tags[tag] = solved_tags.get(tag, 0) + 1
				except:
					pass
	print(username,"solved",len(user_solve) - oldsz,"\n")

# -----------------------------------------------------------------------------
def get_user_rating(username):
	username = username.split()

	url = "https://codeforces.com/api/user.info?handles="
	url += username[0]

	for i in range(1, len(username)):
		url += str(";"+username[i])

	print("calling for user rating")
	start_time = time.time()

	js = get_json(url)

	if not js or "status" not in js or js["status"] != "OK":
		return

	print("--- %s seconds ---" % (time.time() - start_time))
	print("got user rating.")

	global user_rating
	for user in js["result"]:
		try:
			print("user rating", user["handle"], ":",  user["rating"])
			user_rating = max(user_rating, user["rating"])
		except:
			pass

	print("")

	user_rating = int(user_rating / 100)
	user_rating = int(user_rating * 100)


# -----------------------------------------------------------------------------
def get_contest_list():
	url = "https://codeforces.com/api/contest.list"

	print("calling for contest list")
	start_time = time.time()

	js = get_json(url)
	if not js or "status" not in js or js["status"] != "OK":
		return

	print("--- %s seconds ---" % (time.time() - start_time))
	print("got contest list.")

	for contest in js["result"]:
		name = contest["name"]
		age = contest["startTimeSeconds"]
		id = contest["id"]
		if "Div" in name:
			contest_list[id] = age
	print("")
# -----------------------------------------------------------------------------
def get_problem_list():
	url = "https://codeforces.com/api/problemset.problems"

	print("calling for problems list")
	start_time = time.time()

	js = get_json(url)

	if not js or "status" not in js or js["status"] != "OK":
		return

	print("--- %s seconds ---" % (time.time() - start_time))
	print("got problems list.")

	global problem_list
	problem_list = js["result"]["problems"]

	print("")

# -----------------------------------------------------------------------------
def not_taken(ls, tags):
	for i in tags:
		if i in solved_tags and solved_tags[i] > 10:
			return False

	mx = 0
	for i in ls:
		cnt = 0;
		for j in i[2]:
			if j in tags:
				cnt += 1
		try:
			per =  min(int((cnt / len(i[2])) * 100), int(int((cnt / len(tags)) * 100)))
		except:
			return False
		mx = max(mx, per)
	if mx >= 80 or len(tags) == 0:
		return False
	return True


# -----------------------------------------------------------------------------
def recommender(username):
	print("calling for user rating and solve and contest and problem list.")
	start_time = time.time()

	p1 = threading.Thread(target=get_user_rating, args=(username,))
	p2 = [threading.Thread(target=get_user_solve, args=(usr, )) for usr in username.split()]
	p3 = threading.Thread(target=get_contest_list, args=())
	p4 = threading.Thread(target=get_problem_list, args=())

	p1.start()
	p3.start()
	p4.start()
	for th in p2:
		th.start()

	p1.join()
	p3.join()
	p4.join()
	for th in p2:
		th.join()

	if user_rating is None:
		return []

	print("--- %s seconds ---" % (time.time() - start_time))
	print("got user rating and solved problems and contest and problem list.\n")

	print("\nrecent tag solved:")
	for (x, y) in solved_tags.items():
		print(x, y)
	print("\n")

	# ----------------------------------------------------------

	ret = list()
	prob_a = 0
	prob_b = 0
	prob_c = 0

	global problem_list
	random.shuffle(problem_list)

	time_lim = time.time() - (730*24*60*60)
	old_problems = list()

	for problem in problem_list:
		link = "https://codeforces.com/contest/" + str(problem["contestId"]) + "/problem/" + problem["index"]
		name = problem["name"]
		try:
			rating = problem["rating"]
		except:
			continue
		tags = problem["tags"]
		contest_id = problem["contestId"]

		prob_id = str(problem["contestId"]) + problem["index"]
		if prob_id not in user_solve and contest_id in contest_list:
			if contest_list[contest_id] < time_lim:
				if rating >= user_rating+100:
					old_problems.append([link, name, tags, rating])
				continue

			if rating == user_rating+100 and prob_a < 2:
				if not_taken(ret, tags):
					ret.append([link, name, tags, rating])
					prob_a += 1
			elif rating == user_rating+200 and prob_b < 2:
				if not_taken(ret, tags):
					ret.append([link, name, tags, rating])
					prob_b += 1
			elif rating == user_rating+300 and prob_c < 6:
				if not_taken(ret, tags):
					ret.append([link, name, tags, rating])
					prob_c += 1

		if len(ret) >= 10:
			break

	for problem in old_problems:
		if problem[3] == user_rating+100 and prob_a < 2:
			if not_taken(ret, problem[2]):
				ret.append(problem)
				prob_a += 1
		elif problem[3] == user_rating+200 and prob_b < 2:
			if not_taken(ret, problem[2]):
				ret.append(problem)
				prob_b += 1
		elif problem[3] == user_rating+300 and prob_c < 6:
			if not_taken(ret, problem[2]):
				ret.append(problem)
				prob_c += 1

		if len(ret) >= 10:
			break


	print("--- %s seconds ---" % (time.time() - start_time))
	print("Problem recomendation done.\n")

	return ret;


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# test code
# -----------------------------------------------------------------------------

def recommend_cf_problem():
	username = input("Please enter your codeforces usernames -- ")
	print("\n")
	print("Recommended Problems for '" + username + "'")
	print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

	day = datetime.datetime.now()
	day = str(day.strftime("%Y-%m-%d"))

	with open("recomhtm/data", "r", encoding = "utf-8") as fin:
		fs = fin.read().split('\n')

		if fs[0] == day and username == fs[1]:
			for i in range(2, len(fs)):
				print(fs[i])
			input("\nPress enter to Open in Browser __ ")
			webbrowser.open('/home/ahmed/Desktop/web/projects/cf_chaser/recomhtm/recommended_problems.html', new=2)
			return

	problems = recommender(username)

	with open("recomhtm/data", "w") as fw:
		fw.write(day+"\n")
		fw.write(username+"\n")


	with open("recomhtm/tmp_html", "r", encoding = "utf-8") as fin:
		htm = fin.read().split('\n')

		htm.append("    <h1 class=\"title\">Recommended Problems</h1>\n")
		htm.append("    <h1 class=\"title\">" + day + "</h1>\n")
		htm.append("    <h1 class=\"handle\">" + username + "</h1>\n")
		htm.append("    <ol>\n")

		for problem in problems:

			htm.append("      <li>\n")
			htm.append("        <h4><a href=\"" + problem[0] + "\"  target=\"_blank\">" + problem[1] + "</a></h4>\n")

			ptag = problem[2][0]
			for j in range(1, len(problem[2])):
				ptag = ptag + ", "+problem[2][j]

			htm.append("        <h4>" + str(problem[3]) + "</h4>\n")
			htm.append("        <h4>" + ptag + "</h4>\n")

			print("\n\n::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
			print("Problem Name:  ", problem[1])
			print("Problem Tags:   ", end = "")
			print(problem[2][0], end = "")
			for j in range(1, len(problem[2])):
				print(",",problem[2][j],end="")
			print("")
			print("Problem Rating:", problem[3])
			print("Link:          ", problem[0])
			print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n\n")

			htm.append("      </li>\n")
		htm.append("    </ol>\n")
		htm.append("  </body>\n")
		htm.append("</html>\n")

		with open("recomhtm/recommended_problems.html", "w") as fw:
			for i in htm:
				fw.write(i+"\n")
	input("\nPress enter to Open in Browser __ \n")
	webbrowser.open('/home/ahmed/Desktop/web/projects/cf_chaser/recomhtm/recommended_problems.html', new=2)


# -----------------------------------------------------------------------------

if __name__ == '__main__':
	recommend_cf_problem()

# -----------------------------------------------------------------------------
