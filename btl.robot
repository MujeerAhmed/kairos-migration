Fetch_all_tags
    [Documentation]     Fetching dataTagIDs
    remove file    ${CURDIR}/Resources/tags.json
    create file    ${CURDIR}/Resources/tags.json
    create session      APIs_session        ${Base_URL}     verify=true
    ${item}=    configVar.getting variable      item
    ${response}=   Get on Session    APIs_session      /exactapi/boilerStressProfiles?     params=filter={"where":{"and":[{"type":"boilerTubeLeakPredictParameters_V3"}]}}   headers=${header}
    ${res}=    create list    @{response.json()}
    ${length}=      Get Length    ${res}
    ${boilerstring}=    Convert To String    Boiler
    ${data_dictionary}=     Create Dictionary
    FOR    ${i}    IN RANGE    ${length}
        ${model_res}    Set Variable    ${res}[${i}]
        ${boilers}=     Get From Dictionary    ${model_res}[input]    paramModelConf
        ${boilerkeys}=      Get Dictionary Keys    ${boilers}
        ${boilerkey_count}=     Get Length    ${boilerkeys}
        ${main_dict}=     create dictionary
        FOR    ${a}    IN RANGE    ${boilerkey_count}
            ${boiler_count}=      Convert To String    ${a+1}
            ${models}=    Get From Dictionary    ${model_res}[input][paramModelConf][${boiler_count}]    modelDet
            ${len}=     Get Length    ${models}
            ${sub_dict}=     create dictionary
            ${boilerjson}   Catenate       ${boilerstring}   ${boiler_count}
            Set To Dictionary    ${sub_dict}    OutputTags=${EMPTY}
            ${output_tags}=     Create List
            FOR    ${j}    IN RANGE    ${len}
                ${tag}=    Set Variable   ${models[${j}]['Output']}
                Append To List    ${output_tags}    ${tag}
            END
            Set To Dictionary  ${sub_dict}  OutputTags  ${output_tags}
            Set To Dictionary    ${main_dict}    ${boilerjson}    ${sub_dict}
        END
        ${bool}     configVar.Setting Tags    ${item[${i}]['name']}     ${main_dict}
    END
