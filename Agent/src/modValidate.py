import reasoner_validator


nominal = {
    "message": {
        "query_graph": {
            "edges": {
                "e00": {
                    "subject": "n00",
                    "object": "n01",
                    "type": "biolink:associated"
                }
            },
            "nodes": {
                "n00": {
                    "curie": "MONDO:0004981",
                    "type": "biolink:Disease"
                },
                "n01": {
                    "type": "biolink:Gene"
                }
            }
        }
    }
}

reasoner_validator.validate_Query(nominal)

x = 5