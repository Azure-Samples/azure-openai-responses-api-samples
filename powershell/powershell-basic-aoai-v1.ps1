<#
Minimal Azure OpenAI Responses API (v1 preview) PowerShell sample.
Prereqs (set env vars before running)
These may be set in your PowerShell profile (echo $PROFILE to find it):
    $env:AZURE_OPENAI_API_KEY
    $env:AZURE_OPENAI_V1_API_ENDPOINT  (e.g. https://your-resource.openai.azure.com/openai/v1)
    $env:AZURE_OPENAI_API_MODEL        (e.g. gpt-4.1-mini)
#>


param([string]$Prompt = "Tell me a joke.")

$endpoint = $env:AZURE_OPENAI_V1_API_ENDPOINT.TrimEnd('/') + "/responses"

$body = @{ model = $env:AZURE_OPENAI_API_MODEL; input = $Prompt } | ConvertTo-Json

$resp = Invoke-RestMethod -Method Post -Uri $endpoint -Headers @{ 'api-key'=$env:AZURE_OPENAI_API_KEY; 'Content-Type'='application/json' } -Body $body

# Print assistant text segments
$resp.output | Where-Object { $_.type -eq 'message' -and $_.role -eq 'assistant' } | ForEach-Object {
        $_.content | ForEach-Object { if ($_.text) { $_.text } }
}
