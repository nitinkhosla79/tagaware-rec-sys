'''
Created on Aug 1, 2015

@author: maged, hossam
'''

from math import exp, log
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr
from sklearn.cluster import KMeans
import codecs
import datetime
import dateutil.relativedelta
import numpy as np
import time
from cmath import sqrt

users, problems, tags, users_problems, problems_tags, users_tags, \
        temporal_values, users_problems_temporal_score, labels = (0,)*9

count_problems, count_users, count_tags = (0,)*3
flag_print = 0
submissions_file = 'All-Submissions.txt'

'''
Parse Submissions.txt, generate dict of user_handle --> user_id (0-based)
Length of dict is the number of users.
'''
  
def create_users():
    global users, count_users
    f = open(submissions_file, 'r')
    handles = set([line.split(' ')[1].rstrip()
                   for line in f if line.split(' ')[0] == 'Handle:'])
    users = dict(zip(list(handles), range(len(handles))))
    count_users = len(users)
    f.close()
    if(flag_print):
        print(users)

'''
Parse Problems-tags.txt, the unique problem name is ContestID + Index
generate dict of problem_name --> problem_id (0-based)
Length of dict is the number of problems
'''

def create_problems():
    global problems, count_problems
    f = codecs.open('Problems-tags.txt', 'r', 'utf-8')
    contest = []
    index = []
    for line in f:
        if line == '\n':
            continue
        s = line.split(' ')
        if s[0] == 'Contest':
            contest += [int(s[2])]
        if s[0] == 'Index:':
            index += [s[1].rstrip()]
    problems = [str(c) + i for c, i in zip(contest, index)]
    problems = dict(zip(problems, range(len(problems))))
    count_problems = len(problems)
    f.close()
    if(flag_print):
        print(problems)

'''
Parse Problems-tags.txt, generate dict of tag --> tag_id (0-based)
Length of dict is the number of tags
'''

def create_tags():
    global tags, count_tags
    f = codecs.open('Problems-tags.txt', 'r', 'utf-8')
    tags = set()
    for line in f:
        if line == '\n':
            continue
        s = line.split(' ')
        if s[0] == 'Tags:':
            tags |= set(line.split(' ', 1)[1:][0].rstrip().split(','))
    tags = set(map(lambda x: x.lstrip(), tags))
    tags = dict(zip(list(tags), range(len(tags))))
    count_tags = len(tags)
    f.close()
    if(flag_print):
        print(tags)

'''
Parse Submissions.txt, for all submissions -> get user_id, problem_id, build adjacency list
Build user-problem graph.
'''

def create_users_problems():
    global users_problems
    f = open(submissions_file, 'r')
    contest_id = ''
    index = ''
    handle = ''
    users_problems = []
    for _ in users:
        users_problems.append([])
    for l in f:
        if l == '\n':
            continue
        arr = l.split(' ')
        if arr[0] == 'Contest':
            contest_id = arr[2].rstrip()
        if arr[0] == 'Index:':
            index = arr[1].rstrip()
        if arr[0] == 'Handle:':
            handle = arr[1].rstrip()
            user_id = users[handle]
            #problem_id = problems[contest_id + index]
            problem_id = get_problem_id(contest_id+index)
            users_problems[user_id].append(problem_id)
    f.close()
    if(flag_print):
        print(users_problems)

def get_problem_id(i):
    global problems
    if i not in problems:
        idx = count_problems
        problems[i] = idx
        return idx
    else:
        return problems[i]

'''
Parse Submissions.txt, for all submissions -> get problem_id, tag_id -> build adjacency list.
Build problem-tag graph.
Build tag-problem graph.
'''

def create_problems_tags():
    global problems_tags
    f = codecs.open('Problems-tags.txt', 'r', 'utf-8')
    contest_id = ''
    index = ''
    current_tags = ''
    problems_tags = []
    for _ in problems:
        problems_tags.append([])
    for l in f:
        arr = l.split(' ')
        if arr[0] == 'Contest':
            contest_id = arr[2].rstrip()
        if arr[0] == 'Index:':
            index = arr[1].rstrip()
        if arr[0] == 'Tags:':
            current_tags = l.split(':')[1][1:].rstrip()
            current_tags = list(map(lambda x: x.rstrip(), current_tags.split(',')))
            current_tags = list(map(lambda x: x.lstrip(), current_tags))
            tags_ids = [tags[tag] for tag in current_tags]
            problem_id = problems[contest_id + index]
            problems_tags[problem_id] += tags_ids
    f.close()
    if(flag_print):
        print(problems_tags)

'''
For each user, we loop over all problems. For each problem, we loop over all tags. We increment the count of this tag for this user.
At the end, we divide by the number of problems for this user.

NOTE: Might need to add all tags in user-tag graph even if with zero weights.
NOTE: Might need to use PrettyPrint/better printing for defaultdict
'''
    
def create_users_tags_matrix():
    global users_tags
    users_tags = [[0 for t in tags] for u in users]
    for handle in users:
        u = users[handle]
        for p in users_problems[u]:
            for t in problems_tags[p]:
                users_tags[u][t] += 1
            for t in tags.values():
                users_tags[u][t] /= (len(users_problems[u]) * 1.0)
    #print('Users Tags: ', users_tags)
'''
Calcultaing user similarity using Pearson's Correlation
NOTE: If needed (if this is taking too much time), possible optimization:
    p(x,y) = p(y,x)
'''
def create_users_correlations(u1):
    correlation = [0] * len(users)
    id1 = users[u1]
    for u2 in users:
        id2 = users[u2]
        l1 = users_tags[id1]
        l2 = users_tags[id2]
        #correlation[id1][id2] = pearsonr(l1, l2)[0]
        correlation[id2] = cosine(l1, l2)

'''
Calculating Temporal Weight between users and tags
'''

def create_temporal():
    global temporal_values
    temporal_values = [[0] * len(tags)] * len(users)
    users_problems_in_tags = [[0] * len(tags)] * len(users)
    f = open('Submissions.txt', 'r')
    contest_id = ''
    index = ''
    handle = ''
    time_stamp = ''
    current_date = datetime.datetime.now()
    half_life = 2
    for l in f:
        if l == '\n':
            continue
        arr = l.split(' ')
        if arr[0] == 'Contest':
            contest_id = arr[2].rstrip()
        if arr[0] == 'Index:':
            index = arr[1].rstrip()
        if arr[0] == 'Handle:':
            handle = arr[1].rstrip()
        if arr[1] == 'Time:':
            time_stamp = arr[2].rstrip()
            user_id = users[handle]
            problem_id = problems[contest_id + index]
            current_problem_tags = problems_tags[problem_id]
            problem_date = datetime.datetime.fromtimestamp(int(time_stamp))
            date_diff = dateutil.relativedelta.relativedelta(
                current_date,
                problem_date)
            days = abs(date_diff.days)
            temporal_value = exp(-log(2) * days / half_life)
            for t in current_problem_tags:
                temporal_values[user_id][t] += temporal_value
                users_problems_in_tags[user_id][t] += 1
    temporal_values = np.matrix(temporal_values)
    users_problems_in_tags = np.matrix(users_problems_in_tags)
    temporal_values = (temporal_values / users_problems_in_tags).tolist()

def compute_temporal_score():
    global users_problems_temporal_score
    users_problems_temporal_score = [dict()] * len(users)
    for u in users:
        uid = users[u]
        for p in problems:
            pid = problems[p]
            user_tag = temporal_values[uid]
            problem_tag = [0] * len(tags)
            for t in problems_tags[pid]:
                problem_tag[t] = 1
            users_problems_temporal_score[uid][pid] = pearsonr(user_tag, problem_tag)[0]

'''
Incorporating Diversity
1. Clustering tags
'''
def create_clusters():
    global labels    
    cluster_vecs = [list(x) for x in zip(*users_tags)]
    
    k = 5
    
    engine = KMeans(n_clusters=k)
    labels = engine.fit(cluster_vecs).labels_
    
    print("Tag labels: ", labels)
    inverse_tags = dict()
    
    for tag in tags:
        inverse_tags[tags[tag]] = tag
    
    for i in range(k):
        print("Cluster ", i)
        for tag_idx in range(len(labels)):
            if labels[tag_idx] == i:
                print(inverse_tags[tag_idx])

def compute_diversity_score():
    # Some function on labels, problems in each tag, return score
    return 

'''
# final scores
alpha = 0.7
user_problem_final_score = [dict()] * len(users)
for u in users:
  uid = users[u]
  for p in problems:
    pid = problems[p]
    user_problem_final_score[uid][pid] = alpha * user_problem_collaborative_score[
        uid][pid] + (1 - alpha) * users_problems_temporal_score[uid][pid]
print(user_problem_final_score[0])
'''

if __name__ == '__main__':
    start_time = time.time()
    create_users()
    print("create users --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    create_problems()
    print("create problems --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    create_tags()
    print("create tags --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    create_users_problems()
    print("create users problems --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    
    print("There are %i users, %i problems and %i tags" % (count_users, count_problems, count_tags))
    
    create_problems_tags()
    print("create problems tags --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    create_users_tags_matrix()
    print("create users tags --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    #create_users_correlations()
    print("correlations --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    #create_temporal()
    print("create temporal --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    #compute_temporal_score()
    print("compute temporal score --- %s seconds ---" % (time.time() - start_time))
    create_clusters() #Gives error!
    
   

'''
Introduction:
1. Start by introducing the importance of the problem, i.e: competitive programming. Include Stats
2. Current status of competitive programming systems. Online judges. Problems. Interests diversify.
3. Current status of recommender systems algorithms. Don't incorporate both diversity and temporality
in tag-aware systems. How will diversity and temporality affect users.
4. List of contributions of this paper.

Background:
DO NOT list papers.
Goal: We did our homework. Nothing in literature exactly covers what we do. Critical eye.

Disclaimer:
PLAGIARISM
Copying word-for-word. Paraphrasing. Read your papers, close them, then write using your own
language.

List of authors:
Ethical restrictions. People who had contributions in the contributions.
'''

'''
Java to XML: Java ML
CPP to XML: Src ML
XML Queries: XPATH
'''

'''
Must write justification for each feature. Something numerical or something referencable. Or use
correlation.
'''