#!/usr/bin/env python
# coding: utf-8

# In[1]:


from neo4j import GraphDatabase
import pandas as pd

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "88888888")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

driver = GraphDatabase.driver(URI, auth=("neo4j", "888888888"))


# In[3]:


def create_projection_papers(sess):
    query = '''
         CALL gds.graph.project.cypher(
            'graphPaperc',
            'MATCH (n:paper)-[r:cites]->(p:paper) WITH DISTINCT n RETURN id(n) AS id',
            'MATCH (n)-[c:cites]->(p) RETURN id(n) AS source, id(p) AS target',
            {validateRelationships: false})
        YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels 
    '''
    sess.run(query)


def trigger_Louvain(sess):
    query = '''
       CALL gds.louvain.stream('graphPaperc')
        YIELD nodeId, communityId, intermediateCommunityIds
        WITH gds.util.asNode(nodeId) AS p, communityId
        MATCH (pa:paper)-[r:cites]->(p)
        WITH p,count(*) as citations,communityId
        RETURN p.title as title,communityId,p.year as year,citations
        ORDER BY p.title,communityId,p.year,citations
    '''
    result=sess.run(query)
    return result
                    


def create_projection_keywords(sess):
    query = '''
    CALL gds.graph.project(
        'graphKeywordsp',
        ['paper', 'keyword'],
        {
            contains: {
                properties: {
                }
            }
        }
    )

    '''
    sess.run(query)


def trigger_similarities(sess):
    query = '''
        CALL gds.nodeSimilarity.stream('graphKeywordsp')
        YIELD node1, node2, similarity
        WITH similarity,gds.util.asNode(node1) AS paper1,gds.util.asNode(node2) AS paper2
        RETURN similarity,paper1.title as title1,paper2.title as title2
        ORDER BY similarity DESCENDING, paper1, paper2
    '''
    result=sess.run(query)
    return result


# In[28]:


driver = GraphDatabase.driver(URI, auth=("neo4j", "88888888"))
with driver.session() as session:
    create_projection_papers(session)
    papers=trigger_Louvain(session)
    create_projection_keywords(session)
    keywords=trigger_similarities(session)

    papers_df = pd.DataFrame(columns=['Title', 'Community','Year','Citations'])
    keys_df = pd.DataFrame(columns=['Similarity', 'Paper1','Paper2'])
    
    for paper in papers:
        a = pd.DataFrame({'Title': paper['title'], 'Community': paper['communityId'],'Year': paper['year'], 'Citations': paper['citations']}, index=[0])
        papers_df = pd.concat([papers_df, a], ignore_index=True)
        
    
    for key in keywords:
        a = pd.DataFrame({'Similarity': key['similarity'], 'Paper1': key['title1'],'Paper2': key['title2']}, index=[0])
        keys_df = pd.concat([keys_df, a], ignore_index=True)
    
    print('------------Query 1: Community detection using Louvain----------------')
    print(papers_df)
    print('##################################################################################')

    print('------------------Query 2: Node Similarities-------------------------')
    print(keys_df.head)
    print('###################################################################################')

