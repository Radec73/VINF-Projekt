import time
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader,IndexOptions
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.document import FieldType

RECORDS = 1200000

# LOADING ALL RECORDS FROM DATAFILE
def get_lines():
    with open("all_cats.txt", encoding='utf-8') as file:
        lines = file.readlines()
        return [line.rstrip() for line in lines]

#CREATION OF INDEX OVER COLUMNS ID,NAME,BREED
def create_index(lines):
    store = MMapDirectory(Paths.get("index"))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    start_time = time.time()
    for a in lines:
        rec = a.replace(';', '').split('|')
        document = Document()
        #CREATION OF FIELD TYPE FOR ID
        field_type = FieldType()
        field_type.setStored(True)
        field_type.setIndexOptions(IndexOptions.NONE)
        document.add(Field("ID", str(rec[0]), field_type))
        document.add(Field("NAME", rec[1], TextField.TYPE_STORED))
        document.add(Field("BREED", rec[10], TextField.TYPE_STORED))
        writer.addDocument(document)
    writer.commit()
    writer.close()
    end_time = time.time()
    print("Index time taken: " + str(end_time - start_time) + " seconds")

# SEARCH FUNCTION FOR FILTERING NAMES or BREEDS returning IDS results
def search(max_r, column, query, start_time):
    resultsIDS = []
    directory = MMapDirectory(Paths.get("index"))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    results = searcher.search(query, max_r).scoreDocs
    end_time = time.time()
    print("Search time over " + column + " taken: " + str(end_time - start_time) + " seconds")
    for res in results:
        doc = searcher.doc(res.doc)
        resultsIDS.append(doc.get('ID'))
    return resultsIDS

# HELPING FUNCTION TO PRINT RESULTS
def print_results(results, column, searcher):
    print(str(len(results)) + " total matches.")
    for res in results:
        doc = searcher.doc(res.doc)
        pos = doc.get('ID')
        print(' ID:', pos, "NAME", ':', doc.get(column))
        print(lines[int(pos)-1])
    print("\nDo you want to display full content of records? y/n")
    if input() == "y":
        printt(results)

# HELPING FUNCTION TO PRINT RESULTS

def printt(resultsa):
    if len(resultsa) >0:
        print("Search succesful "+str(len(resultsa)) + " total matches.")
    else:
        print("Search unsuccesful no records found!")
    print()
    for res in resultsa:
        print(lines[int(res) - 1])



#MAIN FUNCTION USER INTERFACE
def choose_option():
    analyzer = StandardAnalyzer()
    while 1:
        print("\n----------------------------------------------------------")
        print("Options:")
        print("1 - Search -> FIELD NAME")
        print("2 - Search -> FIELD BREEDS")
        print("3 - Search -> FIELDS NAME & BREEDS")
        print("4 - Search -> SAMPLE TEST 1a (Searching all cats names 'Victoria')")
        print("5 - Search -> SAMPLE TEST 1b (Searching all cats names 'Vyctoria')")
        print("6 - Search -> SAMPLE TEST 2 (Searching all cats with breed 'SER' which states for Serval breed)")
        print("7 - Search -> SAMPLE TEST 3 (Searching all cats with breed 'RAG' meaning ragdols named 'Oswald')")
        print("x - EXIT SEARCH")
        setup = input()
        # FILTER NAMES
        if setup == '1':
            print("Enter name to find: ")
            setup2 = input()
            start_time = time.time()
            resultsIDS = search(RECORDS, "NAME", QueryParser("NAME", analyzer).parse(setup2),
                                                   start_time)
            printt(resultsIDS)
        #FILTER BREEDS
        elif setup == '2':
            print("Enter breed to find: ")
            setup2 = input()
            start_time = time.time()
            resultsIDS= search(RECORDS, "BREED", QueryParser("BREED", analyzer).parse(setup2),
                                                   start_time)
            printt(resultsIDS)
        # FILTER NAME AND BREED
        elif setup == '3':
            print("Enter name to find: ")
            setup2 = input()
            print("Enter breed to find: ")
            setup3 = input()
            start_time = time.time()
            resultsIDS1 = search(RECORDS, "NAME", QueryParser("NAME", analyzer).parse(setup2),
                                                     start_time)
            resultsIDS2 = search(RECORDS, "BREED", QueryParser("BREED", analyzer).parse(setup3),
                                                     start_time)
            resultsa = set(resultsIDS1) & set(resultsIDS2)
            printt(resultsa)
        # TEST 1
        elif setup == '4':
            start_time = time.time()
            resultsIDS = search(RECORDS, "NAME", QueryParser("NAME", analyzer).parse('Victoria'),
                                                   start_time)
            printt(resultsIDS)
        #TEST 2
        elif setup == '5':
            start_time = time.time()
            resultsIDS = search(RECORDS, "NAME", QueryParser("NAME", analyzer).parse('Vyctoria'),
                                                   start_time)
            printt(resultsIDS)
        # TEST 3
        elif setup == '6':
            start_time = time.time()
            resultsIDS = search(RECORDS, "BREED", QueryParser("BREED", analyzer).parse('SER'),
                                                   start_time)
            printt(resultsIDS)
        #TEST 4
        elif setup == '7':
            start_time = time.time()
            resultsIDS1 = search(RECORDS, "NAME", QueryParser("NAME", analyzer).parse('Oswald'),
                                                     start_time)
            resultsIDS2 = search(RECORDS, "BREED", QueryParser("BREED", analyzer).parse('RAG'),
                                                     start_time)
            resultsa = set(resultsIDS1) & set(resultsIDS2)
            printt(resultsa)
        elif setup == 'x':
            return
        else:
            print("You pressed invalid key. Try Again!")

# INIT LUCENE MACHINE
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print("CONNECTED")
# GET ALL RECORDS IN ARRAY FORMAT
lines = get_lines()
# CREATE INDEX
create_index(lines)
print("INDEXES CREATED")
# CALL MAIN FUNCTION TO BEGIN SEARCHING
choose_option()
