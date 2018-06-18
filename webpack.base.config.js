const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const webpackHelper = require('./webpack-helper.js');

// See https://github.com/gaearon/react-hot-boilerplate/tree/next for details on prod settings too

module.exports = {
  context: __dirname,

  entry: webpackHelper.buildEntries(),

  output: {
    path: path.resolve('./src/static/bundles/'),
    filename: '[name]-[hash].js',
  },

  plugins: [
    new ExtractTextPlugin('[name]-[hash].css'),

    new webpack.NamedModulesPlugin(),
    // prints more readable module names in the browser console on HMR updates

    new webpack.NoEmitOnErrorsPlugin(),
    // do not emit compiled assets that include errors

    new webpack.optimize.CommonsChunkPlugin({
      name: 'common',
      minChunks: 2,
    }),
  ],

  module: {
    loaders: [
      { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader' },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',

          use: [
            {
              loader: 'css-loader',
              query: {
                modules: true,
                localIdentName: '[name]__[local]___[hash:base64:5]',
              },
            },
            'postcss-loader',
          ],
        }),
      },
      {
        test: /\.scss$/,
        exclude: /node_modules/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',

          use: [
            {
              loader: 'css-loader',
              query: {
                modules: true,
                sourceMap: true,
                importLoaders: 2,
                localIdentName: '[name]__[local]___[hash:base64:5]',
              },
            },
            'sass-loader',
          ],
        }),
      },
    ],
  },

  resolve: {
    modules: ['node_modules', './src/frontend/js'],
    extensions: ['.js', '.jsx', '.css', 'scss'],
    alias: {
      react_table_css: path.join(__dirname, '/node_modules/react-table/react-table.css'),
    },
  },
};
