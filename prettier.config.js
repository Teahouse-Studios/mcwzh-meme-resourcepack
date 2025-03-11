module.exports = {
  semi: false,
  useTabs: false,
  singleQuote: true,
  trailingComma: 'all',
  tabWidth: 2,
  printWidth: 80,
  endOfLine: 'lf',
  overrides: [
    {
      files: '*.json',
      options: {
        tabWidth: 4,
        useTabs: false,
      },
    },
  ],
}
