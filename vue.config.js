const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  publicPath: '/',
  outputDir: 'dist',
  transpileDependencies: true,
  devServer: {
    proxy: {
      // FastAPI (основной бэкенд)
      '^/api/reviews': { target: 'http://127.0.0.1:8000', changeOrigin: true, secure: false },
      '^/api/send-order': { target: 'http://127.0.0.1:8000', changeOrigin: true, secure: false },
      // Express (если потребуется /api/profanity и пр.)
      '^/api/profanity': { target: 'http://localhost:3001', changeOrigin: true },
    },
  },
});
