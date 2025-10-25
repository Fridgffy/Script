@echo off
@START python -m http.server > NUL 2>&1

rem @START chrome http://127.0.0.1:8000/desktop/GetIncident/portal.html
@START chrome http://127.0.0.1:8000/portal.html
@python ./Getincident.py --automatic