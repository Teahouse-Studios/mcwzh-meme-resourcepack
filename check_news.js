const fs = require('fs')
const path = require('path')

const content = fs.readFileSync(path.resolve(__dirname, 'news.json'))
JSON.parse(content)
