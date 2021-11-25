
const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');


module.exports = {
    entry: {
        main: path.resolve(__dirname, 'src/index.js')
    },
    output: {
        path: path.join(__dirname, "static"),
        filename: "js/[name].[fullhash:8].js",
        publicPath: "/static/",
    },
    optimization: {
    splitChunks: {
        chunks: "all",
    },
    runtimeChunk: "single",
    },
    module: {
        rules: [
            {
                test: /\.(|m)js(|x)0$/,
                exclude: /node_modules/,
                loader: "babel-loader",
            },
            {
                test: /\.css$/i,
                use: [ MiniCssExtractPlugin.loader, 'css-loader','postcss-loader',],

            },
            {
                test: /\.s(c|a)ss$/i,
                use: [ MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader'],

            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'img/[name][hash]ext][query]'
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[name][hash][ext][query]'
                }
            },
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: 'css/[name].[chunkhash:8].css'
        }),
        new BundleTracker({filename: './webpack-stats.json'}),
    ],
    resolve: {
        fallback: {
        }
    }
}
