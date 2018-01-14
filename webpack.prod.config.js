const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

const config = require('./webpack.base.config.js');

config.output.path = path.resolve('./src/static/dist/');

config.plugins = config.plugins.concat([
  new BundleTracker({ filename: './webpack-stats-prod.json' }),

  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('production'),
    },
  }),

  // keeps hashes consistent between compilations
  new webpack.optimize.OccurrenceOrderPlugin(),

  // minifies the code
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false,
    },
  }),
]);

module.exports = config;
