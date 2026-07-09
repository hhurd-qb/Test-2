import { Octokit } from '@octokit/rest'

const octokit = new Octokit({ auth: process.env.GH_TOKEN })
const [owner, repo] = process.env.GH_REPO.split('/')

const PAGE_IDS = ['6429147235', '6429769806']

async function main() {
  for (const pageId of PAGE_IDS) {
    await syncPage(pageId)
  }
}

async function syncPage(pageId) {
  const content = await fetchPageMarkdown(pageId)
  const path = `skills/${pageId}.md`
  const encoded = Buffer.from(content).toString('base64')

  let sha
  try {
    const { data } = await octokit.repos.getContent({ owner, repo, path })
    sha = data.sha
  } catch (e) {
    // 404 = new file, no sha needed
  }

  await octokit.repos.createOrUpdateFileContents({
    owner, repo, path,
    message: `sync: page ${pageId}`,
    content: encoded,
    ...(sha && { sha })
  })

  console.log(`✓ Synced page ${pageId}`)
}

async function fetchPageMarkdown(pageId) {
  const creds = Buffer.from(
    `${process.env.CONFLUENCE_EMAIL}:${process.env.CONFLUENCE_TOKEN}`
  ).toString('base64')

  const res = await fetch(
    `https://${process.env.CONFLUENCE_DOMAIN}/wiki/api/v2/pages/${pageId}?body-format=markdown`,
    { headers: { Authorization: `Basic ${creds}` } }
  )
  const data = await res.json()
  return data.body?.markdown?.value ?? ''
}

main()
