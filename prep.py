from KG.kg import ingest_Chunks, embed_text, create_nodes, create_relationship, create_vector_index
from KG.chunking import split_data_from_file
from KG.config import load_neo4j_graph
import json
# Load the Neo4j graph connection and OpenAI API details
graph, openAI_api, openAI_endpoint = load_neo4j_graph()


file_names = ["Talleyrand", "Napoleon", "Battle_of_Waterloo"]
# Iterate over the file names and process each JSON file
for name in file_names:
    #  Load JSON file
    file = f"data/{name}.json"
    # Chunking
    chunks = split_data_from_file(file)
    # Assuming `file` is a path to your JSON file
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    #Create nodes
    if name == "Battle_of_Waterloo":
        create_nodes(graph=graph, data=data, node_label="Event", node_name=name)
    else:
        create_nodes(graph=graph, data=data, node_label="Person", node_name=name)
    # Ingest Chunks
    ingest_Chunks(graph=graph, chunks=chunks, node_name=name, node_label='Chunk')


# Create relationships
rel_section_chunk = """ 
MATCH (s:Section), (c:Chunk)
WHERE s.type = c.source AND s.parent_name = c.node_name
MERGE (s)-[:HAS_CHUNK]->(c);

"""

rel_person_person = """
MATCH (p1:Person), (p2:Person)
WHERE id(p1) < id(p2)
MERGE (p1)-[:RELATED_TO]->(p2)
MERGE (p2)-[:RELATED_TO]->(p1);

"""

rel_person_event = """
MATCH (p:Person), (e:Event)
MERGE (p)-[:RELATED_TO]->(e)
MERGE (e)-[:RELATED_TO]->(p);

"""

rel_person_section = """
MATCH (p:Person), (s:Section)
WHERE p.name = s.parent_name
MERGE (p)-[:HAS_SECTION]->(s);

"""

rel_event_section = """
MATCH (e:Event), (s:Section)
WHERE e.name = s.parent_name
MERGE (e)-[:HAS_SECTION]->(s);

"""

queries = [rel_section_chunk, rel_person_person, rel_person_event, rel_person_section, rel_event_section]

for query in queries:
    create_relationship(graph=graph, query=query)


# Create a vector index for the Chunk nodes
create_vector_index(graph=graph, index_name='Chunk')

# Embed text in the Chunk nodes
embed_text(graph = graph, OPENAI_API_KEY=openAI_api, OPENAI_ENDPOINT=openAI_endpoint, node_name='Chunk')
