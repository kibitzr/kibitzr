var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'src/client/public');
var APP_DIR = path.resolve(__dirname, 'src/client/app');

var config = {
  entry: APP_DIR + '/index.jsx',
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  devtool: 'source-map',
  module : {
    loaders : [
        { test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery,$=jquery' },
        { test: /\.jsx?$/, include : APP_DIR, exclude: /(node_modules|bower_components)/, loader: 'babel' },
        { test: /\.css$/, loader: 'style-loader!css-loader' },
        { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file" },
        { test: /\.woff2?$/, loader:"url?prefix=font/&limit=5000" },
        { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&mimetype=application/octet-stream" },
        { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&mimetype=image/svg+xml" }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({$: "jquery", jQuery: "jquery"})
    , new webpack.DefinePlugin({
        'process.env': {
            'NODE_ENV': JSON.stringify('production')
        }
    })
    // , new webpack.optimize.UglifyJsPlugin({
    //     include: /\.min\.js$/,
    //     minimize: true
    // })
  ],
  resolve: {
      alias: {
          'yaml-js': 'yaml-js/yaml.js',
          'fs': ''
      }
  }
};

module.exports = config;
