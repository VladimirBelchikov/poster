const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');

const ImageMinimizerPlugin = require('image-minimizer-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const isDev = process.env.NODE_ENV !== 'production';

const pagesDir = path.join(__dirname, './src/templates/');
const fs = require("fs");
const pages = fs.readdirSync(pagesDir).filter(fileName => fileName.endsWith('.pug'));

const PugAlias = require('pug-alias');
const pug = require('pug');


const config = {
    mode: isDev ? 'development' : 'production',

    devtool: isDev ? 'source-map' : false,

    entry: {
      main: path.resolve(__dirname, './src/godDamn.js'),
    },

    output: {
      filename: '[name].[hash].bundle.js',
      path: path.resolve(__dirname, './dist/'),
      assetModuleFilename: "assets/[name][ext][query]",
    },

    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: ['babel-loader'],
        },
        {
          test: /\.(woff(2)?|eot|ttf|otf|svg)$/,
          type: 'asset/resource',
          exclude: /images/,
          generator: {
            filename: 'assets/fonts/[name][ext]',
          },
        },
        {
          test: /\.svg$/,
          type: 'asset/inline',
          exclude: /fonts/,
        },
        {
          test: /\.(png|jpe?g|gif|svg)$/i,
          type: 'asset',
          exclude: /fonts/,
          generator: {
            filename: 'assets/img/[name][ext]',
          },
        },
        {
          test: /\.(sa|sc|c)ss$/i,
          use: [
            isDev ? "style-loader" : MiniCssExtractPlugin.loader,
            "css-loader",
            "postcss-loader",
            "sass-loader",
          ],
        },
        {
          test: /\.(pug|jade)$/,
          loader: "pug-loader",
        },
      ],
    },

    optimization: {
      minimizer: [
        new ImageMinimizerPlugin({
          minimizer: {
            implementation: ImageMinimizerPlugin.squooshMinify,
            options: {
              encodeOptions: {
                mozjpeg: {
                  quality: 90,
                },
                webp: {
                  lossless: 1,
                },
              },
            },
          },
        }),
      ],
    },

    devServer: {
      historyApiFallback: true,
      static: {
        directory: path.join(__dirname, './dist'),
      },
      open: true,
      compress: true,
      port: 9000,
    },
    plugins: [
      new CleanWebpackPlugin(),
      ...pages.map(page => new HtmlWebpackPlugin({
        template: `${pagesDir}/${page}`,
        filename: `./${page.replace(/\.pug/, '.html')}`,
      })),
    ].concat(isDev ? [] : [
      new MiniCssExtractPlugin({
        filename: '[name].[contenthash].min.css',
        chunkFilename: '[name].[contenthash].min.css',
      }),
    ]),
  }
;

module.exports = config;
