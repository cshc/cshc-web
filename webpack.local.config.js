const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const webpackHelper = require('./webpack-helper.js');

const config = require('./webpack.base.config.js');

config.entry = webpackHelper.buildEntries(true);
config.output.publicPath = 'http://localhost:3000/static/bundles/'; // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  // new webpack.NoErrorsPlugin(),
  new BundleTracker({ filename: './webpack-stats.json' }),

  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('debug'),
    },
  }),
]);

config.devServer = {
  headers: { 'Access-Control-Allow-Origin': '*' },
  host: 'localhost',
  port: 3000,

  historyApiFallback: true,
  // respond to 404s with index.html

  hot: true,
  // enable HMR on the server
};

config.devtool = 'source-map';

module.exports = config;
