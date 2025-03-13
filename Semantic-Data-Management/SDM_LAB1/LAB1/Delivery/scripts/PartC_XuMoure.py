from neo4j import GraphDatabase
import pandas as pd

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "sdm12345")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

driver = GraphDatabase.driver(URI, auth=("neo4j", "sdm12345"))


# CREATE NODE COMMUNITY WITH NAME database
def create_db_community(sess):
    print('Creating db community')
    query = '''
        CREATE(:community {name: 'database'})
    '''
    sess.run(query)

# WHAT DEFINES A COMMUNITY IS A SET OF KEYWORDS, SO WE CREATE THE EDGE BETWEEN COMMUNITY AND THE DATABASE KEYWORDS
def create_edge_community_keyword(sess):
    print('Creating edge between community and keyword')
    query = '''
        MATCH (k: keyword)
        WHERE toLower(k.keyword) IN  ['data management', 'indexing', 'data modeling', ' big data', 'data processing', 'data storage', 'data querying']
        MATCH(c:community {name:'database'})
        CREATE (c)-[:definedby]->(k)
    '''
    sess.run(query)

# FIND CONFERENCES RELATED TO THE COMMUNITY
# WE FIND THE CONFERENCES AND THEN WE CREATE AN EDGE BETWEEN THEM AND THE COMMUNITY
def conference_community(sess):
    print('Creating edge between conference and community')
    query = '''
        MATCH (p:paper)-[pres:presented]->(e:edition)-[part:partof]->(conf:conference)
        WITH conf, toFloat(COUNT(DISTINCT p)) as total_number_papers
        CALL {
            WITH conf
            MATCH (conf)<-[:partof]-(e:edition)<-[:presented]-(pap:paper)-[:contains]->(k:keyword)<-[:definedby]-(c:community {name: 'database'})
            RETURN  toFloat(COUNT(DISTINCT pap)) as community_papers, c
        }
        WITH community_papers / total_number_papers AS proportion_community, conf, c
        WHERE proportion_community >= 0.9
        CREATE (conf)-[:relates]->(c)
    '''
    sess.run(query)

# FIND JOURNALS RELATED TO THE COMMUNITY
# WE FIND THE JOURNALS AND THEN WE CREATE AN EDGE BETWEEN THEM AND THE COMMUNITY
def journal_community(sess):
    print('Creating edge between journal and community')
    query = '''
        MATCH (p:paper)-[pub:publishedin]->(v:volume)-[b:belongs]->(jour:journal)
        WITH jour, toFloat(COUNT(DISTINCT p)) as total_number_papers
        CALL {
            WITH jour 
            MATCH (jour)<-[:belongs]-(v:volume)<-[:publishedin]-(pap:paper)-[:contains]->(k:keyword)<-[:definedby]-(c:community {name: 'database'})
            RETURN toFloat(COUNT(DISTINCT pap)) as community_papers, c
        }
        WITH community_papers / total_number_papers AS proportion_community, jour, c
        WHERE proportion_community >= 0.9
        CREATE (jour)-[:relates]->(c) 
    '''
    sess.run(query)

# We create a projection of the graph (a subgraph)
def page_rank(sess):
    print('Creating projection of the graph')
    query = '''
         CALL gds.graph.project.cypher(
            'page_rank_database_papers',
            'MATCH (n:paper)-[r]->()-[]->()-[:relates]->(c:community { name: "database" }) WHERE type(r) IN ["publishedin", "presented"] WITH DISTINCT n RETURN id(n) AS id',
            'MATCH (n)-[c:cites]->(p) RETURN id(n) AS source, id(p) AS target',
            {validateRelationships: false})
         YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels 
    '''
    sess.run(query)

# We compute the pageRank score of the subgraph created and then
# WE ADD A LABEL TO THE PAPERS TO DISTINGUISH IF THEY BELONG TO THE 100 TOP
# WE FIRST ORDER THE PAPERS BY SCORE AND THEN USE LIMIT TO ONLY ADD THE LABEL TO ONLY 100 PAPERS
def top100(sess):
    print('Creating top 100 label')
    query = '''
            CALL gds.pageRank.stream('page_rank_database_papers')
            YIELD nodeId, score
            WITH gds.util.asNode(nodeId) AS paper
            ORDER BY score DESC
            LIMIT 100
            SET paper :top_100_db_community
            RETURN paper
    '''
    result = sess.run(query)
    return result

# an author of the top-100 papers
def get_potential_reviewers(sess):
    print('Getting potential reviewers')
    query = '''
        MATCH (a:author)-[:writes] -> (p:top_100_db_community)
        RETURN DISTINCT a
    '''
    pot_rev = sess.run(query)
    return pot_rev

# gurus: authors that are authors of, at least, two papers among the top-100 identified.
def get_gurus(sess):
    print('Getting gurus')
    query = '''
        MATCH (a:author)-[:writes]->(p:top_100_db_community)
        WITH a, COUNT(p) AS papers
        WHERE papers >= 2
        RETURN DISTINCT a   
    '''
    result = sess.run(query)
    return result

def print_top100(result):
    top_100_df = pd.DataFrame(columns=['Title', 'Id'])
    print('------------Top 100 papers----------------')
    for i in result:
        top = pd.DataFrame({'Title': i.data()['paper']['title'] ,'Id': i.data()['paper']['id']}, index=[0])
        top_100_df = pd.concat([top_100_df, top], ignore_index=True)
    print(top_100_df)
    print('################################################################')

def print_reviewers(result):
    reviewers_df = pd.DataFrame(columns=['Name', 'Id'])
    print('----------------Potential Reviewers----------------')
    for rev in result:
        reviewer = pd.DataFrame({'Name': rev.data()['a']['name'], 'Id': rev.data()['a']['id']}, index=[0])
        reviewers_df = pd.concat([reviewers_df, reviewer], ignore_index=True)
    print(reviewers_df)
    print('################################################################')

def print_gurus(result):
    gurus_df = pd.DataFrame(columns=['Name', 'Id'])
    print('----------------Gurus----------------')
    for guru in result:
        a = pd.DataFrame({'Name': guru.data()['a']['name'], 'Id': guru.data()['a']['id']}, index=[0])
        gurus_df = pd.concat([gurus_df, a], ignore_index=True)
    print(gurus_df)
    print('################################################################')


if __name__ == '__main__':
    driver = GraphDatabase.driver(URI, auth=("neo4j", "sdm12345"))
    with driver.session() as session:
        create_db_community(session)
        create_edge_community_keyword(session)
        conference_community(session)
        journal_community(session)
        page_rank(session)
        top_100 = top100(session)
        print_top100(top_100)
        reviewers = get_potential_reviewers(session)
        print_reviewers(reviewers)
        gurus = get_gurus(session)
        print_gurus(gurus)
