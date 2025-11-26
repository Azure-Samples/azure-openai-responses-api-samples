<#
PSOpenAI Azure OpenAI Responses API PowerShell sample.
Prereqs (set env vars before running)
These may be set in your PowerShell profile (echo $PROFILE to find it):
    $env:OPENAI_API_KEY
    $env:OPENAI_API_BASE  (e.g. https://sweden-fp-resource.openai.azure.com/)
    $env:AZURE_OPENAI_API_MODEL        (e.g. gpt-4.1-mini)
#>

# Install once
#Install-Module PSOpenAI -Scope CurrentUser

# Load module
Import-Module PSOpenAI # NB - PSOpenAI is a community project: https://github.com/mkht/PSOpenAI/

# Auth (Azure OpenAI key)
$AuthType = 'Azure'

Request-Response `
    -Model $env:AZURE_OPENAI_API_MODEL `
    -Message 'Tell me a joke.' `
    -ApiType $AuthType
