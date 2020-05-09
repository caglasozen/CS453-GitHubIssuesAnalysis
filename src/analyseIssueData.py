from github import Github
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import github.GithubObject

class AnalyseIssues:

    def __init__(self, git, repo_add):
        self.git = git
        self.repo_add = repo_add
        self.repo = git.get_repo(repo_add)
        self.all_issues = self.repo.get_issues(state='all')
        self.closed_issues = self.repo.get_issues(state='closed')
        self.open_issues = self.repo.get_issues(state='open')
        self.pulls = self.repo.get_pulls(state='merged')
        self.colors = ['#2d026d', '#704a9c', '#af90cd', '#eedbff']
        self.labels = self.repo.get_labels()


    def getRepoInfo(self):
        print "Fetching Data for ", self.repo.full_name.upper() , "Repository... \n"

        all_branches = self.repo.get_branches()
        print "- Branch Count", all_branches.totalCount, "\n"

        all_contributors = self.repo.get_contributors()
        print "-Contributor Count", all_contributors.totalCount, "\n"

        all_commits = self.repo.get_commits()
        print "- Commit Count", all_commits.totalCount, "\n"

        print "- Total Issue Count", self.all_issues.totalCount

        return

    def getProjectInfo(self):

        print "-- PROCESS SMELL 9.1.1 : No Project", "\n"

        has_Project = self.repo.has_projects

        if has_Project is False:
            print "- No Project defined in the repository" "\n"
        else:
            all_projects = self.repo.get_projects()
            print "- Project Count", all_projects.totalCount, "\n"

        all_milestones = self.repo.get_milestones(state='all')
        open_milestones = self.repo.get_milestones(state='open')
        closed_milestones = self.repo.get_milestones(state='closed')

        print "- Total Milestone Count", all_milestones.totalCount
        print "- Open Milestone Count", open_milestones.totalCount
        print "- Closed Milestone Count", closed_milestones.totalCount, "\n"

        print "\n"

        return

    def getUnassignedIssues(self):

        print "-- PROCESS SMELL 9.2.1: Unassigned Issues ", "\n"

        open_issues = self.repo.get_issues(state='open', assignee="none")
        closed_issues = self.repo.get_issues(state='closed', assignee="none")

        unassigned_issues = closed_issues.totalCount + open_issues.totalCount

        print "- Number of Issues without any assignees in total", (unassigned_issues)
        print "- Number of Open Issues without any assignees", open_issues.totalCount
        print "- Number of Closed Issues without any assignees", closed_issues.totalCount

        print "- Sample Issue:", open_issues[3] , " Assignees: ", open_issues[3].assignee, ", State:" ,open_issues[3].state
        print "- Sample Issue:", open_issues[15] , " Assignees: ", open_issues[15].assignee, ", State:" ,open_issues[15].state
        print "- Sample Issue:", closed_issues[102] , " Assignees: ", closed_issues[3].assignee, ", State:", closed_issues[102].state
        print "- Sample Issue:", closed_issues[40] , " Assignees: ", closed_issues[3].assignee, ", State:", closed_issues[40].state

        data = [self.all_issues.totalCount-unassigned_issues, open_issues.totalCount, closed_issues.totalCount]
        categ = ["Assigned Issues","Open Unassigned Issues", "Closed Unassigned Issues"]

        self.drawPieChart(data,categ, "PROCESS SMELL 9.2.1: Assigned Issues vs. Unassigned Issues" )
        print "\n"
        return

    def getUnlabeledIssues(self):

        print "-- PROCESS SMELL 9.2.2: Unlabeled Issues ", "\n"

        open_issues = []
        closed_issues = []
        unlabeled_open = []
        unlabeled_closed = []
        labeled = False

        for label in self.labels:
            issues = self.repo.get_issues(state='open', labels=[label])
            count = len(open_issues)
            for issue in issues:
                open_issues.append(issue)

        for issue in self.open_issues:
            labeled = False
            for issue_2 in open_issues:
                if issue.number == issue_2.number:
                    labeled = True
            if labeled is False:
                unlabeled_open.append(issue)

        for label in self.labels:
            issues = self.repo.get_issues(state='closed', labels=[label])
            for issue in issues:
                closed_issues.append(issue)

        for issue in self.closed_issues:
            labeled = False
            for issue_2 in closed_issues:
                if issue.number == issue_2.number:
                    labeled = True
            if labeled is False:
                unlabeled_closed.append(issue)

        labeled_issues = len(closed_issues) + len(open_issues)
        unlabeled_issues = len(unlabeled_open) + len(unlabeled_closed)


        print "- Number of Issues without any labels in total", unlabeled_issues
        print "- Number of Open Issues without any labels", len(unlabeled_open)
        print "- Number of Closed Issues without any labels", len(unlabeled_closed)

        print "- Sample Issue:", unlabeled_open[3], " Labels: ", unlabeled_open[3].labels, ", State:", unlabeled_open[3].state
        print "- Sample Issue:", unlabeled_open[5], " Labels: ", unlabeled_open[15].labels, ", State:", unlabeled_open[15].state
        print "- Sample Issue:", unlabeled_closed[3], " Labels: ", unlabeled_closed[3].labels, ", State:", unlabeled_closed[3].state
        print "- Sample Issue:", unlabeled_closed[5], " Labels: ", unlabeled_closed[5].labels, ", State:", unlabeled_closed[5].state

        data = [labeled_issues, len(unlabeled_open), len(unlabeled_closed)]
        categ = ["Labeled Issues", "Open Unlabeled Issues", "Closed Unlabeled Issues"]

        self.drawPieChart(data, categ, "PROCESS SMELL 9.2.2: Labeled Issues vs. Unlabeled Issues")

        print "\n"

    def getIssuesClosedBeforeFix(self):

        print "-- PROCESS SMELL 9.2.3 : Issues closed before their Pull Request/Commit", "\n"

        issues_PR = []

        for i in range(self.closed_issues.totalCount):
            issue = self.closed_issues[i]
            if issue.pull_request is not None:
                curr_PR = issue.as_pull_request()
                if curr_PR.merged is True:
                    date = (issue.closed_at - curr_PR.merged_at).seconds
                    if 0 < date:
                        issues_PR.append(issue)

        print "- Issues closed before their Pull Request/Commit ", len(issues_PR)
        print "- Sample Issue:", issues_PR[2], " Labels: ", issues_PR[2].labels, ", State:", issues_PR[2].state
        print "- Sample Issue:", issues_PR[4], " Labels: ", issues_PR[4].labels, ", State:", issues_PR[4].state

        data = [self.all_issues.totalCount - len(issues_PR), len(issues_PR)]
        categ = ["Issues closed after their Pull Request/Commit", "Issues closed before their Pull Request/Commit"]

        self.drawPieChart(data, categ, "PROCESS SMELL 9.2.3 : Issues closed before their Pull Request/Commit")

        print "\n"

        return

    def getIssuesNotClosedByPR(self):

        print "-- PROCESS SMELL 9.2.4 : Issues not closed by a commit or a PR", "\n"

        t = datetime.utcnow()

        issues_PR = []

        for i in range(self.open_issues.totalCount):
            issue = self.open_issues[i]
            if issue.pull_request is not None:
                curr_PR = issue.as_pull_request()
                date = (t - curr_PR.created_at).days
                if curr_PR.mergeable is True and 30 < date:
                    issues_PR.append(issue)

        print "- Number of Open Issues with a mergeable PR over a month: ", len(issues_PR)
        print "- Sample Issue:", issues_PR[2], " Labels: ", issues_PR[2].labels, ", State:", issues_PR[2].state
        print "- Sample Issue:", issues_PR[4], " Labels: ", issues_PR[4].labels, ", State:", issues_PR[4].state

        print "\n"

        return

    def getIdle(self):

        print "-- PROCESS SMELL 9.2.5 : Issues idle for over a year", "\n"

        t = datetime.utcnow()

        issues_PR = []

        for i in range(self.open_issues.totalCount):
            issue = self.open_issues[i]
            issue_date = issue.created_at
            date = (t - issue_date).days

            if issue.pull_request is None and 365 < date:
                issues_PR.append(issue)

        print "- Number of Issues idle for over year: ", len(issues_PR)
        print "- Sample Issue:", issues_PR[2], " Created at: ", issues_PR[2].created_at, ", State:", issues_PR[2].state
        print "- Sample Issue:", issues_PR[40], " Created at: ", issues_PR[40].created_at, ", State:", issues_PR[40].state

        print "\n"

        return

    def getIncompPRReview(self):

        print "-- PROCESS SMELL 9.2.6 : Incomplete PR Review for over 3 months", "\n"

        t = datetime.utcnow()

        issues_PR = []

        for i in range(self.open_issues.totalCount):
            issue = self.open_issues[i]

            if issue.pull_request is not None:
                curr_PR = issue.as_pull_request()
                reviews = curr_PR.get_reviews()

                if reviews is not None:
                    for review in reviews:
                        submit_time = review.submitted_at

                        date = (t - submit_time).days
                        if 365 < date:
                            issues_PR.append(issue)

        print "- Number of Issues with idle PR Review for over year: ", len(issues_PR)
        print "- Sample Issue:", issues_PR[2], " Created at: ", issues_PR[2].created_at, ", State:", issues_PR[2].state
        print "- Sample Issue:", issues_PR[8], " Created at: ", issues_PR[8].created_at, ", State:", issues_PR[8].state

        print "\n"

        return

    def func(self, pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    def drawPieChart(self, data, categ, plot_name):
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: self.func(pct, data), textprops=dict(color="w"), colors = self.colors)
        ax.legend(wedges, categ, title="Issues", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title(plot_name)

        plt.show()
        return

