const path = require('path');

module.exports = {
  mode: 'production',
  entry: {
    // 'home': './pages/home.js',
    'listings': './pages/listings.js',
    'leases': './pages/leases.js'
  },
  output: {
    path: path.resolve(__dirname, '../static/js/pages'),
    filename: '[name].js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },
  optimization: {
    // splitChunks: true,
    minimize: true,
  },
  performance: {
    maxEntrypointSize: 700000,
  }
};

