*** Settings ***
Library         RequestsLibrary
Suite Setup     Start Server
Suite Teardown  Stop Server

*** Variables ***
${SERVER URL}   http://localhost:5000

*** Test Cases ***
Test Get Person
    [Documentation]  Verify response for GET /people/{person_id}
    [Tags]           GET
    ${response}=     Get Request    ${SERVER URL}/people/1
    Should Be Equal  ${response.status_code}  200
    Should Be True   ${response.json()['name']} == 'Luke Skywalker'

Test Get Planet
    [Documentation]  Verify response for GET /planets/{planet_id}
    [Tags]           GET
    ${response}=     Get Request    ${SERVER URL}/planets/3
    Should Be Equal  ${response.status_code}  200
    Should Be True   ${response.json()['name']} == 'Yavin IV'

Test Get Starship
    [Documentation]  Verify response for GET /starships/{starship_id}
    [Tags]           GET
    ${response}=     Get Request    ${SERVER URL}/starships/101
    Should Be Equal  ${response.status_code}  404
    Should Be True   ${response.json()['error']} == 'Starship not found.'
    Should Be True   ${response.json()['message']} == 'No starship with id 101 exists.'

*** Keywords ***
Start Server
    [Documentation]  Start Flask server
    Run Process  python  app.py
    Wait Until Keyword Succeeds  10s  1s  Get Server Status

Stop Server
    [Documentation]  Stop Flask server
    Run Keyword If  '${SERVER PROCESS}' != ''  Terminate Process  ${SERVER PROCESS}

Get Server Status
    ${resp}=  Get Request  ${SERVER URL}
    Should Be Equal As Strings  ${resp.status_code}  200
    ${SERVER PROCESS}=  Get Process ID  name=python
