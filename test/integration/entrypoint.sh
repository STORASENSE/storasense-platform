#!/bin/sh
python -m test.integration.cleanup_database
pytest ./test/integration/
python -m test.integration.cleanup_database
