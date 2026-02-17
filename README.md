# Data_Ingestion_manipulation_workflow_Lab

## 1. Setup

```
$ uv init
$ uv sync
```

## Data Quality Checks

**Accept**

- Correct data is accepted.

**Transform**

- Incorrect data in forms of datatype, space e.g is transformed without changing the _meaning_ of the data.

**Flag**

- The data that _could_ be wrong is flagged.
- It is excludet from the calculations-

**Reject**

- Invalid data (e.g where obligated fields are missing) is rejeted and stored in a file: _rejected_products.csv_
