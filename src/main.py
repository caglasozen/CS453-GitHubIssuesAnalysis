from github import Github
from analyseIssueData import AnalyseIssues

# First create a Github instance
# using an access token
g = Github("****************************")
repo_add = "tensorflow/magenta"

analyse_tool = AnalyseIssues(g, repo_add)
analyse_tool.getRepoInfo()

#Process Smells 9.1.1

#analyse_tool.getProjectInfo()

#Process Smells 9.2.1

#analyse_tool.getUnassignedIssues()

#Process Smells 9.2.2

analyse_tool.getUnlabeledIssues()

#Process Smells 9.2.3

#analyse_tool.getIssuesClosedBeforeFix()

#Process Smells 9.2.4

#analyse_tool.getIssuesNotClosedByPR()

#Process Smells 9.2.5

#analyse_tool.getIdle()

#Process Smells 9.2.6

#analyse_tool.getIncompPRReview()

