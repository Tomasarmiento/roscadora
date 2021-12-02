const HTMLWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "development",
  entry: './src/main.js',
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // Crea nodos `style` a partir de cadenas JS
          " style-loader ",
          // Traduce CSS a CommonJS
          " css-loader ",
          // Compila Sass a CSS
          " sass-loader ",
        ],
      },
      {
        test: /\.html$/i,
        loader: 'html-loader',
    }
    ],
  },
  plugins: [
      new HTMLWebpackPlugin({
        template: './src/index.html'
      })
    ]
}
