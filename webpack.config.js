const path = require('path');

module.exports = {
  mode: 'development',
  devtool: 'eval-source-map',

  entry: './app/assets/main.js',

  output: {
    path: path.resolve(__dirname, 'static'),  // Must be in STATICFILES_DIRS
    publicPath: '/static/',  // STATIC_URL
    filename: '[name].js',
    chunkFilename: '[id]-[chunkhash].js',
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          { loader: 'css-loader', options: { importLoaders: 1 } },
          'postcss-loader',
        ]
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf|png|svg|jpg|gif)$/,
        loader: 'file-loader',
        options: { name: '[name].[ext]' }
      }
    ]
  }
};
