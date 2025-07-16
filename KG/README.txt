This program is a version of the original project (https://github.com/homayounsrp/kg_youtube/tree/main)
Functionality is identical but my version has been updated to use more current libraries due to deprecation

Operations Instructions : 
	1. Create .env file with details of Neo4j database and openAI api key
	2. Run prep.py to create and populate the Neo4j knowledge graph database
	3. Edit and run main.py to see how the RAG agents respond to the provided question

Details of Knowledge Graph Creation (prep.py):
	1. Program begins by connecting to a local Neo4j server. (config.py)
	2. Three biographical CSV documents detailaing the life of Napoleon are then loaded. (prep.py)
	3. Each file is then processed : (prep.py)
		a1. Program uses recursive character text splitting to chunk the data from CSV files. (chunking.py)
		a2. These chunks are then processed into a record containing both chunk text and chunk metadata. (kg.py)
		b1. A main node is created for each CSV file and added to the Neo4j Graph (kg.py)
		b2. Section nodes are created for each section within a CSV file and added to the Neo4j Graph (kg.py)
		c1. ChunkRecord is processed, merging chunks based on keys (kg.py)
		c2. Merged chunks are injested, turned into nodes and added to the Neo4j Graph (kg.py).
	4. Using hardcoded relationships, relationships are added to the Neo4j Graph (kg.py).
	5. A VectorIndex is created using the dynamic node label (kg.py).
	6. An embedding is made using OpenAI and dynamic labelling (kg.py).

RAG : Knowledge graph can be interrogated using VectorRAG(.py) and GraphRAG(.py) both powered by OpenaAI
	1. Question must be hard coded (main.py)
	2. Program utilises a prompt template to ensure improve results (prompt.py)