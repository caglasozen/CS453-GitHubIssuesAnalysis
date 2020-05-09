from github import Github

# First create a Github instance
# using an access token
g = Github("****************************")

# Get the desired repo
repo = g.get_repo("tensorflow/magenta")

print "Fetching Data for ", repo.full_name.upper() , "Repository... \n"

###################################### RAW DATA #################################################

#ISSUES INFO

print "----Issues Data-----"
all_issues = repo.get_issues(state='all')
open_issues = repo.get_issues(state='open')
closed_issues = repo.get_issues(state='closed')

print "Total Issue Count",all_issues.totalCount
print "Open Issue Count",open_issues.totalCount
print "Closed Issue Count",closed_issues.totalCount, "\n"

print "----Issue Comments-----"
all_comments = repo.get_issues_comments()
print "Issue Comment Count",all_comments.totalCount, "\n"


#MILESTONES INFO
print "----Milestones Data-----"
all_milestones = repo.get_milestones(state='all')
open_milestones = repo.get_milestones(state='open')
closed_milestones = repo.get_milestones(state='closed')

print "Total Milestone Count",all_milestones.totalCount
print "Open Milestone Count",open_milestones.totalCount
print "Closed Milestone Count",closed_milestones.totalCount, "\n"

#PULL REQUEST INFO
print "----Pull Request Data-----"

all_pulls = repo.get_pulls(state='all')
open_pulls = repo.get_pulls(state='open')
closed_pulls = repo.get_pulls(state='closed')

print "Total Pull Request Count",all_pulls.totalCount
print "Open Pull Request Count",open_pulls.totalCount
print "Closed Pull Request Count",closed_pulls.totalCount, "\n"

print "----Pull Request Comments-----"
all_pull_comments = repo.get_pulls_comments()
print "Pull Request Comment Count",all_pull_comments.totalCount, "\n"

print "----Pull Request Review Comments-----"
all_pull_review_comments = repo.get_pulls_review_comments()
print "Pull Request Review Comment Count",all_pull_review_comments.totalCount, "\n"

#BRANCH INFO
print "----Branch Data-----"
all_branches = repo.get_branches()
print "Branch Count",all_branches.totalCount, "\n"

#COMMENT INFO
print "----Comment Data-----"
all_comments = repo.get_comments()
print "Comment Count",all_comments.totalCount, "\n"

#COMMIT INFO
print "----Commit Data-----"
all_commits = repo.get_commits()
print "Commit Count",all_commits.totalCount, "\n"

#PROJECT INFO
print "----Project Data-----"
#all_projects = repo.get_projects()
#print "Project Count",all_projects.totalCount, "\n"

#CONTRIBUTOR INFO
print "----Contributor Data-----"
all_contributors = repo.get_contributors()
print "Contributor Count",all_contributors.totalCount, "\n"

#LABEL INFO
print "----Label Data-----"
all_labels = repo.get_labels()
print "Label Count",all_labels.totalCount, "\n"

#RELEASE INFO
print "----Release Data-----"
all_releases = repo.get_releases()
print "Release Count",all_releases.totalCount, "\n"

###################################### STATS  #################################################
#For later use

contributor_stats = repo.get_stats_contributors()
commit_stats = repo.get_stats_commit_activity()
code_freq = repo.get_stats_code_frequency()

