from github import Github
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class AnalyseIssues:

    def __init__(self, git, repo_add):
        self.git = git
        self.repo_add = repo_add
        self.repo = git.get_repo(repo_add)
        self.all_issues = self.repo.get_issues(state='all')
        self.closed_issues = self.repo.get_issues(state='closed')
        self.open_issues = self.repo.get_issues(state='open')
        self.pulls = self.repo.get_pulls(state='open')
        self.colors = ['#008f85', '#3ca289', '#63b68c', '#88c88f', '#aeda93', '#d6ea9a', '#fffaa4', '#fcdd86', '#f9bf6e', '#f4a15c', '#ed8153', '#e2614f', '#d43d51']
        self.labels = self.repo.get_labels()
        plt.ioff()


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

        #Detailed Analysis#

        #OPEN ISSUES#

        self.det_Analysis(open_issues, "Open Unassigned Issues")

        print "\n"

        #CLOSED ISSUES#

        self.det_Analysis(closed_issues, "Closed Unassigned Issues")

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

        # Detailed Analysis#

        # OPEN ISSUES#

        self.det_Analysis(unlabeled_open, "Open Unlabeled Issues")

        print "\n"

        # CLOSED ISSUES#

        self.det_Analysis(unlabeled_closed, "Closed Unlabeled Issues")

        return

    def getIssuesClosedBeforeFix(self):

        print "-- PROCESS SMELL 9.2.3 : Issues closed before their Pull Request/Commit", "\n"

        issues_PR = []

        for i in range(self.closed_issues.totalCount/4):
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

        data = [self.closed_issues.totalCount - len(issues_PR), len(issues_PR)]
        categ = ["Issues closed after their Pull Request/Commit", "Issues closed before their Pull Request/Commit"]

        self.drawPieChart(data, categ, "PROCESS SMELL 9.2.3 : Issues closed before their Pull Request/Commit")

        print "\n"

        # Detailed Analysis#

        self.det_Analysis(issues_PR, "Issues closed before their Pull Request/Commit")

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

        # Detailed Analysis#

        self.det_Analysis(issues_PR, "Issues not closed by a commit or a PR")

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

        # Detailed Analysis#

        self.det_Analysis(issues_PR, "Issues idle for over a year")

        print "\n"

        return

    def getIncompPRReview(self):

        print "-- PROCESS SMELL 9.2.6 : PR Review Request not addressed for over 3 months", "\n"

        issues_PR = []
        t = datetime.utcnow()

        for issue in self.open_issues:
            issue_event = issue.get_events()
            for event in issue_event:
                if event.event == "review_requested":
                    date_created = event.created_at
                    date = (t-date_created).days
                    if 90 < date:
                        issues_PR.append(issue)

        print "- Number of Issues with idle PR Review for 3 months: ", len(issues_PR)
        print "- Sample Issue:", issues_PR[2], " Created at: ", issues_PR[2].created_at, ", State:", issues_PR[2].state
        print "- Sample Issue:", issues_PR[8], " Created at: ", issues_PR[8].created_at, ", State:", issues_PR[8].state

        print "\n"

        # Detailed Analysis#

        self.det_Analysis(issues_PR, "PR Review Request not addressed for over 3 months")

        print "\n"

        return

    def func(self, pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))

        if absolute == 0:
            return ''

        return "{:.1f}%".format(pct)

    def drawPieChart(self, data, categ, plot_name):
        fig, ax = plt.subplots(figsize=(12, 4), subplot_kw=dict(aspect="equal"))
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: self.func(pct, data), textprops=dict(color="w"), colors = self.colors, radius = 1.235)

        labels = ['%s: %i' % (l, v) for l, v in zip(categ, data)]

        ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1.1, 0, 0.5, 1))
        plt.setp(autotexts, size=8)
        ax.set_title(plot_name)
        plt.show()

        #plt.savefig("../out/" + plot_name + ".png")

        return

    def det_Analysis(self, issues, title):
        no_body, short_body, med_body, long_body, no_PR, with_PR, duplicate, merged, referenced, lot_comm, few_comm, med_comm, assigned, unassigned = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 03

        for issue in issues:

            if issue.body is None:
                no_body += 1
            else:
                body_len = len(issue.body)

                if body_len <= 250:
                    short_body += 1
                elif 250 < body_len and body_len <= 500:
                    med_body += 1
                else:
                    long_body += 1

            comments = issue.comments

            if comments is None or comments <= 10:
                few_comm += 1
            elif 10 < comments and comments <= 30:
                med_comm += 1
            else:
                lot_comm += 1

            if issue.pull_request is None:
                no_PR += 1
            else:
                with_PR += 1

            if (title != "Open Unassigned Issues") and (title != "Closed Unassigned Issues") :
                if issue.assignee is None: unassigned += 1
                else: assigned += 1

            issue_events = issue.get_events()

            for event in issue_events:
                if event == "marked_as_duplicate":
                    duplicate += 1
                if event == "merged":
                    merged += 1
                if event == "referenced":
                    referenced += 1

        if (title == "Open Unassigned Issues") or (title == "Closed Unassigned Issues"):
            data = [short_body, med_body, long_body, no_PR, with_PR, duplicate, merged, referenced, lot_comm, few_comm,
                    med_comm]
            categ = ["Short Body", "Medium Body", "Long Body", "No PR", "With PR", "Duplicate", "Merged", "Referenced",
                     "Few Comments", "Medium Comments", "A Lot of Comments"]

        else:
            data = [short_body, med_body, long_body, no_PR, with_PR, duplicate, merged, referenced, lot_comm, few_comm,
                    med_comm, assigned, unassigned]
            categ = ["Short Body", "Medium Body", "Long Body", "No PR", "With PR", "Duplicate", "Merged", "Referenced",
                     "Few Comments", "Medium Comments", "A Lot of Comments", "No Assignee", "Assigned"]

        self.drawPieChart(data, categ, title)

        return
