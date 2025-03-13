import csv
import random
import math
from rdflib import Graph, Namespace, RDF, RDFS, Literal

# Create a namespace
ns = Namespace('http://example.org/')

# Create a graph
g = Graph()

areas = ['machine learning', 'database', 'natural language processing']
g.add((ns.Area1, RDF.type, ns.Area))
g.add((ns.Area2, RDF.type, ns.Area))
g.add((ns.Area3, RDF.type, ns.Area))
g.add((ns.Area1, ns.topic, Literal(areas[0])))
g.add((ns.Area2, ns.topic, Literal(areas[1])))
g.add((ns.Area3, ns.topic, Literal(areas[2])))

with open('clean/conference.csv', encoding='ISO-8859-1') as csvfile:
    data = [dict(row) for row in csv.DictReader(csvfile)]

conferences = {}
i = 1
for row in data:
    if row['name'] not in conferences:
        conferences[row['name']] = i
        if i % 4 == 1:
            g.add((ns.Conference + str(i), RDF.type, ns.Workshop))
        elif i % 4 == 2:
            g.add((ns.Conference + str(i), RDF.type, ns.Symposium))
        elif i % 4 == 3:
            g.add((ns.Conference + str(i), RDF.type, ns.Regular_conference))
        else:
            g.add((ns.Conference + str(i), RDF.type, ns.Expert_group))
        g.add((ns.Conference + str(i), ns.venueName, Literal(row['name'])))
        if i % 3 == 1:
            g.add((ns.Conference + str(i), ns.venueRelatedTo, ns.Area1))
        elif i % 3 == 2:
            g.add((ns.Conference + str(i), ns.venueRelatedTo, ns.Area2))
        else:
            g.add((ns.Conference + str(i), ns.venueRelatedTo, ns.Area3))
        i += 1

with open('clean/journal.csv', encoding='ISO-8859-1') as csvfile:
    data = [dict(row) for row in csv.DictReader(csvfile)]

journals = {}
i = 1
for row in data:
    if row['name'] not in journals:
        journals[row['name']] = i
        g.add((ns.Journal + str(i), RDF.type, ns.Journal))
        g.add((ns.Journal + str(i), ns.venueName, Literal(row['name'])))
        if i % 3 == 1:
            g.add((ns.Journal + str(i), ns.venueRelatedTo, ns.Area1))
        elif i % 3 == 2:
            g.add((ns.Journal + str(i), ns.venueRelatedTo, ns.Area2))
        else:
            g.add((ns.Journal + str(i), ns.venueRelatedTo, ns.Area3))
        i += 1

with open('clean/writes.csv', encoding='ISO-8859-1') as csvfile:
    data = [dict(row) for row in csv.DictReader(csvfile)]

papers = {}
authors = {}
i = 1   # counter for authors
j = 1   # counter for papers
k = 1   # counter for revisions
for row in data:
    if row['title'] not in papers:
        papers[row['title']] = j
        if j % 4 == 1:
            g.add((ns.Paper + str(j), RDF.type, ns.Short_paper))
        elif j % 4 == 2:
            g.add((ns.Paper + str(j), RDF.type, ns.Poster_paper))
        elif j % 4 == 3:
            g.add((ns.Paper + str(j), RDF.type, ns.Demo_paper))
        else:
            g.add((ns.Paper + str(j), RDF.type, ns.Full_paper))
        g.add((ns.Paper + str(j), ns.paperTitle, Literal(row['title'])))
        if i % 3 == 1:
            g.add((ns.Paper + str(j), ns.paperRelatedTo, ns.Area1))
        elif i % 3 == 2:
            g.add((ns.Paper + str(j), ns.paperRelatedTo, ns.Area2))
        else:
            g.add((ns.Paper + str(j), ns.paperRelatedTo, ns.Area3))
        g.add((ns.Submission + str(j), RDF.type, ns.Submission))
        g.add((ns.Paper + str(j), ns.submittedTo, ns.Submission + str(j)))
        if j % 2 == 1:
            g.add((ns.Submission + str(j), ns.accepted, Literal("yes")))
            if j % 4 == 1:  #Short_paper
                g.add((ns.Chair + str(int(j / 2) + 1), RDF.type, ns.Chair))
                g.add((ns.Chair + str(int(j / 2) + 1), ns.personName, Literal("Chair" + str(int(j / 2) + 1))))
                g.add((ns.Chair + str(int(j / 2) + 1), ns.handles, ns.Submission + str(j)))
                g.add((ns.Proceeding + str(j), RDF.type, ns.Proceeding))
                g.add((ns.Paper + str(j), ns.includedIn, ns.Proceeding + str(j)))
                year = random.randint(2000, 2020)
                g.add((ns.Proceeding + str(j), ns.publicationYear, Literal(year)))
                keysList = list(conferences.keys())
                g.add((ns.Submission + str(j), ns.presentedAt, ns.Conference + str(conferences[keysList[(j-1) % 5]])))
                g.add((ns.Conference + str(conferences[keysList[(j-1) % 5]]), ns.publishes, ns.Proceeding + str(j)))
            elif j % 4 == 3:    #Demo_paper
                g.add((ns.Editor + str(int(j / 2)), RDF.type, ns.Editor))
                g.add((ns.Editor + str(int(j / 2)), ns.personName, Literal("Editor" + str(int(j / 2)))))
                g.add((ns.Editor + str(int(j / 2)), ns.handles, ns.Submission + str(j)))
                g.add((ns.Volume + str(j), RDF.type, ns.Volume))
                g.add((ns.Paper + str(j), ns.includedIn, ns.Volume + str(j)))
                year = random.randint(2000, 2020)
                g.add((ns.Volume + str(j), ns.publicationYear, Literal(year)))
                number = random.randint(1, 10)
                g.add((ns.Volume + str(j), ns.volumeNumber, Literal(number)))
                keysList = list(journals.keys())
                g.add((ns.Submission + str(j), ns.presentedAt, ns.Journal + str(journals[keysList[(j-1) % 20]])))
                g.add((ns.Journal + str(journals[keysList[(j-1) % 20]]), ns.publishes, ns.Volume + str(j)))
        elif j % 2 == 0:
            g.add((ns.Submission + str(j), ns.accepted, Literal("no")))
            if j % 4 == 2:  # Poster_paper
                g.add((ns.Chair + str(int(j / 2) + 1), RDF.type, ns.Chair))
                g.add((ns.Chair + str(int(j / 2) + 1), ns.personName, Literal("Chair" + str(int(j / 2) + 1))))
                g.add((ns.Chair + str(int(j / 2) + 1), ns.handles, ns.Submission + str(j)))
                keysList = list(conferences.keys())
                g.add((ns.Submission + str(j), ns.presentedAt, ns.Conference + str(conferences[keysList[(j-1) % 5]])))
            elif j % 4 == 0:    #Full_paper
                g.add((ns.Editor + str(int(j / 2)), RDF.type, ns.Editor))
                g.add((ns.Editor + str(int(j / 2)), ns.personName, Literal("Editor" + str(int(j / 2)))))
                g.add((ns.Editor + str(int(j / 2)), ns.handles, ns.Submission + str(j)))
                keysList = list(journals.keys())
                g.add((ns.Submission + str(j), ns.presentedAt, ns.Journal + str(journals[keysList[(j-1) % 20]])))

        nrevisions = random.randint(2, 5)
        for n in range(nrevisions):
            g.add((ns.Revision + str(k), RDF.type, ns.Revision))
            g.add((ns.Submission + str(j), ns.goesThrough, ns.Revision + str(k)))
            g.add((ns.Reviewer + str(k), RDF.type, ns.Reviewer))
            g.add((ns.Reviewer + str(k), ns.personName, Literal("Reviewer" + str(k))))
            g.add((ns.Reviewer + str(k), ns.does, ns.Revision + str(k)))
            if j % 2 == 1:
                g.add((ns.Revision + str(k), ns.decision, Literal("yes")))
                g.add((ns.Revision + str(k), ns.reviewText, Literal("good")))
            else:
                g.add((ns.Revision + str(k), ns.decision, Literal("no")))
                g.add((ns.Revision + str(k), ns.reviewText, Literal("bad")))
            k += 1
        j += 1

    if row['author'] not in authors:
        authors[row['author']] = i
        g.add((ns.Author + str(i), RDF.type, ns.Author))
        g.add((ns.Author + str(i), ns.personName, Literal(row['author'])))
        i += 1
    g.add((ns.Author + str(authors[row['author']]), ns.writes, ns.Paper + str(papers[row['title']])))

g.serialize('abox.ttl', format='turtle')
