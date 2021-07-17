const fs = require('fs')
const path = require('path')

const news = fs.readFileSync(path.resolve(__dirname, 'news.json'))
JSON.parse(news)

const alerts = fs.readFileSync(path.resolve(__dirname, 'alerts.json'))
JSON.parse(alerts)
