# Load DeepSeek credentials
# https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code
$deepseekConfig = "$HOME\.deepseek\credentials.ps1"
if (Test-Path $deepseekConfig) {
    . $deepseekConfig
}

# DeepSeek backend for Claude Code
function deepseek {
    $env:ANTHROPIC_BASE_URL             = "https://api.deepseek.com/anthropic"
    $env:ANTHROPIC_AUTH_TOKEN           = $env:DEEPSEEK_API_KEY
    $env:ANTHROPIC_MODEL                = "deepseek-v4-pro[1m]"
    $env:ANTHROPIC_DEFAULT_OPUS_MODEL   = "deepseek-v4-pro[1m]"
    $env:ANTHROPIC_DEFAULT_SONNET_MODEL = "deepseek-v4-pro[1m]"
    $env:ANTHROPIC_DEFAULT_HAIKU_MODEL  = "deepseek-v4-flash"
    $env:CLAUDE_CODE_SUBAGENT_MODEL     = "inherit"

    # --- Swap CLAUDE.md for DeepSeek-optimized version ---
    $swapBackup = ".\CLAUDE.md.deepseek-backup"
    $deepseekMd = ".\DEEPSEEK.md"
    $didSwap = $false

    # Crash recovery: restore from stale backup from a previous crashed session
    if (Test-Path $swapBackup) {
        Move-Item $swapBackup .\CLAUDE.md -Force
        Write-Host "[deepseek] Restored CLAUDE.md from crashed session" -ForegroundColor Yellow
    }

    # Swap DEEPSEEK.md → CLAUDE.md (only if DEEPSEEK.md exists in CWD)
    if (Test-Path $deepseekMd) {
        Copy-Item .\CLAUDE.md $swapBackup -Force
        Copy-Item $deepseekMd .\CLAUDE.md -Force
        $didSwap = $true
        Write-Host "[deepseek] Swapped DEEPSEEK.md → CLAUDE.md" -ForegroundColor Cyan
    }

    try {
        & $env:USERPROFILE\AppData\Roaming\npm\claude.cmd @args
    } finally {
        # Always restore original CLAUDE.md, even if claude crashes
        if ($didSwap -and (Test-Path $swapBackup)) {
            Move-Item $swapBackup .\CLAUDE.md -Force
            Write-Host "[deepseek] Restored original CLAUDE.md" -ForegroundColor Cyan
        }
    }
}

function claude {
    $env:ANTHROPIC_BASE_URL             = ""
    $env:ANTHROPIC_AUTH_TOKEN           = ""
    $env:ANTHROPIC_MODEL                = ""
    $env:ANTHROPIC_DEFAULT_OPUS_MODEL   = ""
    $env:ANTHROPIC_DEFAULT_SONNET_MODEL = ""
    $env:ANTHROPIC_DEFAULT_HAIKU_MODEL  = ""
    $env:CLAUDE_CODE_SUBAGENT_MODEL     = ""
    $env:CLAUDE_CODE_EFFORT_LEVEL       = ""
    & $env:USERPROFILE\AppData\Roaming\npm\claude.cmd @args
}

# # Load DeepSeek credentials
# $deepseekConfig = "$HOME\.deepseek\credentials.ps1"
# if (Test-Path $deepseekConfig) {
#     . $deepseekConfig
# }

# function Use-DeepSeek {
#     $env:ANTHROPIC_BASE_URL             = "https://api.deepseek.com/anthropic"
#     $env:ANTHROPIC_AUTH_TOKEN           = $env:DEEPSEEK_API_KEY
#     $env:ANTHROPIC_MODEL                = "deepseek-v4-pro[1m]"
#     $env:ANTHROPIC_DEFAULT_OPUS_MODEL   = "deepseek-v4-pro[1m]"
#     $env:ANTHROPIC_DEFAULT_SONNET_MODEL = "deepseek-v4-pro[1m]"
#     $env:ANTHROPIC_DEFAULT_HAIKU_MODEL  = "deepseek-v4-flash"
#     $env:CLAUDE_CODE_SUBAGENT_MODEL     = "deepseek-v4-flash"
#     $env:CLAUDE_CODE_EFFORT_LEVEL       = "max"
#     Write-Host "Switched to DeepSeek" -ForegroundColor Cyan
# }

# function Use-Claude {
#     $env:ANTHROPIC_BASE_URL             = ""
#     $env:ANTHROPIC_AUTH_TOKEN           = ""
#     $env:ANTHROPIC_MODEL                = ""
#     $env:ANTHROPIC_DEFAULT_OPUS_MODEL   = ""
#     $env:ANTHROPIC_DEFAULT_SONNET_MODEL = ""
#     $env:ANTHROPIC_DEFAULT_HAIKU_MODEL  = ""
#     $env:CLAUDE_CODE_SUBAGENT_MODEL     = ""
#     $env:CLAUDE_CODE_EFFORT_LEVEL       = ""
#     Write-Host "Switched to Claude (Anthropic)" -ForegroundColor Yellow
# }

# # Default to DeepSeek on startup (so Intelligent Terminal inherits it)
# Use-DeepSeek

# function deepseek { claude @args }
# function claude-native { Use-Claude; claude @args; Use-DeepSeek }