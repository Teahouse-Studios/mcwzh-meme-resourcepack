const fs = require('fs')
const path = require('path')

const news = fs.readFileSync(path.resolve(__dirname, './dymanic/news.json'))
JSON.parse(news)

const alerts = fs.readFileSync(path.resolve(__dirname, './dymanic/alerts.json'))
JSON.parse(alerts)
