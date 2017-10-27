const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

// See https://github.com/gaearon/react-hot-boilerplate/tree/next for details on prod settings too

module.exports = {
  context: __dirname,

  entry: {
    venueDetail: [
      'react-hot-loader/patch',
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      './src/frontend/js/apps/VenueDetail.jsx',
    ],

    teamDetail: [
      'react-hot-loader/patch',
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      './src/frontend/js/apps/TeamDetail.jsx',
    ],

    oppositionClubDetail: [
      'react-hot-loader/patch',
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      './src/frontend/js/apps/OppositionClubDetail.jsx',
    ],
  },

  output: {
    path: path.resolve('./src/static/bundles/'),
    filename: '[name]-[hash].js',
    publicPath: 'http://localhost:3000/static/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
  },

  plugins: [
    new ExtractTextPlugin('[name]-[hash].css'),

    new webpack.HotModuleReplacementPlugin(),
    // enable HMR globally

    new webpack.NamedModulesPlugin(),
    // prints more readable module names in the browser console on HMR updates

    new webpack.NoEmitOnErrorsPlugin(),
    // do not emit compiled assets that include errors

    new BundleTracker({ filename: './webpack-stats.json' }),

    new webpack.optimize.CommonsChunkPlugin({
      name: 'common',
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

  devtool: 'source-map',
};
