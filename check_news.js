const fs = require('fs')
const path = require('path')

const news = fs.readFileSync(path.resolve(__dirname, './dynamic/news.json'))
JSON.parse(news)

const alerts = fs.readFileSync(path.resolve(__dirname, './dynamic/alerts.json'))
JSON.parse(alerts)
