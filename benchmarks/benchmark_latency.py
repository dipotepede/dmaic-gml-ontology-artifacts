import time
import numpy as np
import rdflib

# Load combined ontology graph
g = rdflib.Graph()
g.parse("ontology/dmaic_gml_tbox.ttl", format="turtle")
g.parse("ontology/abox/folioshield.ttl", format="turtle")

with open("queries/cq1_invalidation.rq", "r") as f:
    query_str = f.read()

assertion_times = []
query_times = []

print("Running 1,000 latency benchmark cycles...")
for i in range(1000):
    # Benchmark ABox assertion
    t0 = time.perf_counter()
    stmt = (
        rdflib.URIRef(f"https://w3id.org/dmaic-gml#TestMetric_{i}"),
        rdflib.URIRef("https://w3id.org/dmaic-gml#hasObservedValue"),
        rdflib.Literal("0.96", datatype=rdflib.XSD.decimal)
    )
    g.add(stmt)
    t1 = time.perf_counter()
    assertion_times.append((t1 - t0) * 1000.0)

    # Benchmark SPARQL invalidation query
    t2 = time.perf_counter()
    res = g.query(query_str)
    t3 = time.perf_counter()
    query_times.append((t3 - t2) * 1000.0)

    # Clean up test assertion
    g.remove(stmt)

assert_arr = np.array(assertion_times)
query_arr = np.array(query_times)
total_arr = assert_arr + query_arr

print("\nBenchmark Summary (1,000 Cycles):")
print(f"ABox Assertion (ms) : Mean = {np.mean(assert_arr):.4f} +/- {np.std(assert_arr):.4f} | Median = {np.median(assert_arr):.4f}")
print(f"SPARQL Query (ms)   : Mean = {np.mean(query_arr):.4f} +/- {np.std(query_arr):.4f} | Median = {np.median(query_arr):.4f}")
print(f"Total Overhead (ms) : Mean = {np.mean(total_arr):.4f} +/- {np.std(total_arr):.4f} | Median = {np.median(total_arr):.4f}")
