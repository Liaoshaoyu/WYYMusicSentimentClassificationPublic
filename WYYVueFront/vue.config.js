module.exports = {
    publicPath: './',
    assetsDir: 'static',
    productionSourceMap: false,
    
    devServer: {
        host: '0.0.0.0',
        port: 8002,
        proxy: {
            '/api':{
                target:'http://0.0.0.0:8001/',
                changeOrigin:true,
                pathRewrite:{
                    '/api':''
                }
            }
        }
    }
}