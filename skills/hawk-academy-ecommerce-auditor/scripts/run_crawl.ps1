<#
run_crawl.ps1 - SiteOne crawl wrapper for the Hawk Academy eCommerce Auditor.

Windows-native equivalent of run_crawl.sh, for attendees who do not have Git
Bash. Same outputs, same crawler flags, no Homebrew and no admin rights needed.

Usage:
  powershell -ExecutionPolicy Bypass -File scripts\run_crawl.ps1 `
      -Url "https://store.example.com" -OutDir ".\audit\crawl" -MaxDepth 3

Extra crawler flags can be appended and are passed straight through:
  ... -MaxDepth 3 --max-visited-urls=400

Produces, inside <OutDir>:
  offline\     mirrored HTML export (what analyze_ecommerce.py reads)
  crawl.json   JSON inventory of every URL crawled
  report.html  the crawler's own interactive report
  robots.txt   copied out of the export when the crawler saved it

The crawler is located in this order:
  1. $env:SITEONE_CRAWLER (explicit override)
  2. siteone-crawler.exe already on PATH
  3. a previous install in %USERPROFILE%\siteone-crawler or C:\siteone-crawler
  4. the bundled binary shipped with the sibling site-crawler skill
  5. a download from the SiteOne GitHub release
#>

param(
    [Parameter(Mandatory = $true)][string]$Url,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [int]$MaxDepth = 3,
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$ExtraArgs
)

$ErrorActionPreference = 'Stop'
$CrawlerVersion = 'v2.3.0'
$PackageName = "siteone-crawler-$CrawlerVersion-win-x64.zip"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Url -notmatch '^https?://') {
    Write-Error "Store URL must start with http:// or https:// (got: $Url)"
    exit 2
}

if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}
$OutDir = (Resolve-Path $OutDir).Path

function Find-Crawler {
    if ($env:SITEONE_CRAWLER -and (Test-Path $env:SITEONE_CRAWLER)) {
        return $env:SITEONE_CRAWLER
    }
    $onPath = Get-Command 'siteone-crawler.exe' -ErrorAction SilentlyContinue
    if ($onPath) { return $onPath.Source }

    $candidates = @(
        (Join-Path $env:USERPROFILE 'siteone-crawler\siteone-crawler.exe'),
        'C:\siteone-crawler\siteone-crawler.exe'
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }
    return $null
}

function Find-BundledPackage {
    # The sibling site-crawler skill ships the Windows build under binaries\.
    $roots = @(
        (Join-Path $ScriptDir '..'),
        (Join-Path $ScriptDir '..\..'),
        (Join-Path $ScriptDir '..\..\..'),
        (Join-Path $env:USERPROFILE '.claude\plugins\cache'),
        (Join-Path $env:USERPROFILE '.claude\skills'),
        (Join-Path $env:USERPROFILE '.claude\plugins')
    )
    foreach ($root in $roots) {
        if (-not (Test-Path $root)) { continue }
        $hit = Get-ChildItem -Path $root -Filter $PackageName -Recurse -File -ErrorAction SilentlyContinue |
               Select-Object -First 1
        if ($hit) { return $hit.FullName }
    }
    return $null
}

function Install-Crawler {
    $dest = Join-Path $env:USERPROFILE 'siteone-crawler'
    if (-not (Test-Path $dest)) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
    }
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("siteone-" + [System.Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $tmp -Force | Out-Null

    $archive = Find-BundledPackage
    if ($archive) {
        Write-Host "-> Installing SiteOne Crawler from the bundled site-crawler binary (no download needed)."
        Write-Host "   $archive"
    }
    else {
        Write-Host "-> No bundled binary found. Downloading the official release..."
        $archive = Join-Path $tmp $PackageName
        $url = "https://github.com/janreges/siteone-crawler/releases/download/$CrawlerVersion/$PackageName"
        try {
            # Progress rendering makes large downloads very slow in PS 5.1.
            $prev = $ProgressPreference
            $ProgressPreference = 'SilentlyContinue'
            Invoke-WebRequest -Uri $url -OutFile $archive -UseBasicParsing
            $ProgressPreference = $prev
        }
        catch {
            Write-Error "Download failed: $url`n$($_.Exception.Message)"
            return $null
        }
    }

    Expand-Archive -Path $archive -DestinationPath (Join-Path $tmp 'x') -Force
    $inner = Join-Path $tmp 'x\siteone-crawler'
    if (Test-Path $inner) {
        Copy-Item -Path (Join-Path $inner '*') -Destination $dest -Recurse -Force
    }
    else {
        Copy-Item -Path (Join-Path $tmp 'x\*') -Destination $dest -Recurse -Force
    }
    Remove-Item -Path $tmp -Recurse -Force -ErrorAction SilentlyContinue

    $exe = Join-Path $dest 'siteone-crawler.exe'
    if (Test-Path $exe) { return $exe }
    return $null
}

Write-Host "-> Platform: Windows (win-x64)"

$crawler = Find-Crawler
if ($crawler) {
    Write-Host "-> Using SiteOne Crawler at: $crawler"
}
else {
    Write-Host "-> SiteOne Crawler not found. Installing it now (free, no licence or signup)."
    $crawler = Install-Crawler
    if (-not $crawler) {
        Write-Error @"
Could not install SiteOne Crawler automatically.
Download the Windows build, extract it, then set SITEONE_CRAWLER to the .exe and re-run:
  https://github.com/janreges/siteone-crawler/releases/tag/$CrawlerVersion
"@
        exit 1
    }
    Write-Host "-> Installed to: $crawler"
}

$offlineDir = Join-Path $OutDir 'offline'
$jsonFile   = Join-Path $OutDir 'crawl.json'
$htmlReport = Join-Path $OutDir 'report.html'

Write-Host "-> Crawling $Url (max depth $MaxDepth)..."
Write-Host "   Output: $OutDir"

$crawlArgs = @(
    "--url=$Url",
    "--max-depth=$MaxDepth",
    "--offline-export-dir=$offlineDir",
    '--offline-export-preserve-url-structure',
    '--offline-export-no-auto-redirect-html',
    '--offline-export-remove-unwanted-code=0',
    "--output-json-file=$jsonFile",
    "--output-html-report=$htmlReport"
)
if ($ExtraArgs) { $crawlArgs += $ExtraArgs }

& $crawler @crawlArgs
$crawlStatus = $LASTEXITCODE

if (-not (Test-Path $offlineDir)) {
    Write-Error @"
The crawl produced no offline export at $offlineDir (exit $crawlStatus).
The site may block crawlers, or the URL may be wrong. Try a lower -MaxDepth,
or check the URL in a browser first.
"@
    exit 1
}

if ($crawlStatus -ne 0) {
    Write-Host "WARNING: crawler exited with status $crawlStatus but an export was produced."
    Write-Host "Continuing with what it captured - note the limitation in the audit."
}

# robots.txt - the offline export keeps it when the crawler fetched it. When it
# did not, the skill fetches it with web_fetch instead (see SKILL.md Step 2).
$robotsSrc = Get-ChildItem -Path $offlineDir -Filter 'robots.txt' -Recurse -File -Depth 3 -ErrorAction SilentlyContinue |
             Select-Object -First 1
if ($robotsSrc) {
    Copy-Item -Path $robotsSrc.FullName -Destination (Join-Path $OutDir 'robots.txt') -Force
    Write-Host "-> robots.txt saved to $(Join-Path $OutDir 'robots.txt')"
}
else {
    Write-Host "ROBOTS_MISSING: robots.txt was not in the crawl."
    Write-Host "Fetch $($Url.TrimEnd('/'))/robots.txt with the web_fetch tool and save it to"
    Write-Host "$(Join-Path $OutDir 'robots.txt') before running analyze_ecommerce.py."
    Write-Host "Do not use curl or wget for this."
}

$pageCount = (Get-ChildItem -Path $offlineDir -Include '*.html', '*.htm' -Recurse -File -ErrorAction SilentlyContinue |
              Measure-Object).Count

Write-Host ""
Write-Host "Crawl complete."
Write-Host "  HTML pages exported : $pageCount"
Write-Host "  Offline export      : $offlineDir"
Write-Host "  JSON inventory      : $jsonFile"
Write-Host "  HTML report         : $htmlReport"
Write-Host ""
Write-Host "Next: python scripts\analyze_ecommerce.py --crawl-dir `"$OutDir`" --base-url `"$Url`" --out `"<work-dir>\findings.json`""
