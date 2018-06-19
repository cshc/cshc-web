const webpack = require('webpack');
const { buildEntries, RelativeBundleTracker } = require('./webpack-helper.js');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const config = require('./webpack.base.config.js');

config.entry = buildEntries(true);
config.output.publicPath = 'http://localhost:3000/static/bundles/'; // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  // new webpack.NoErrorsPlugin(),
  new RelativeBundleTracker({ filename: './webpack-stats.json', indent: 2 }),

  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('debug'),
    },
  }),

  // Bundle Analyzer
  // Ref: https://github.com/webpack-contrib/webpack-bundle-analyzer
  new BundleAnalyzerPlugin({
    analyzerMode: 'static',
    reportFilename: 'webpack-report.html',
    openAnalyzer: false,
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
