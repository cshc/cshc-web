const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

// See https://github.com/gaearon/react-hot-boilerplate/tree/next for details on prod settings too

module.exports = {
  context: __dirname,

  entry: [
    'babel-polyfill',
    'react-hot-loader/patch',
    'webpack-dev-server/client?http://localhost:3000',
    'webpack/hot/only-dev-server',
    './src/assets/js/index',
  ],

  output: {
    path: path.resolve('./src/assets/bundles/'),
    filename: '[name]-[hash].js',
    publicPath: 'http://localhost:3000/assets/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    // enable HMR globally

    new webpack.NamedModulesPlugin(),
    // prints more readable module names in the browser console on HMR updates

    new webpack.NoEmitOnErrorsPlugin(),
    // do not emit compiled assets that include errors

    new BundleTracker({ filename: './webpack-stats.json' }),
  ],

  module: {
    loaders: [{ test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader' }],
  },

  resolve: {
    modules: ['node_modules', './src'],
    extensions: ['.js', '.jsx'],
  },

  devServer: {
    headers: { 'Access-Control-Allow-Origin': '*' },
    host: 'localhost',
    port: 3000,

    historyApiFallback: true,
    // respond to 404s with index.html

    hot: true,
    // enable HMR on the server
  },
};
