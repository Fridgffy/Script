@echo off
@START python -m http.server > NUL 2>&1
@python ./GetIncident.py --manually
