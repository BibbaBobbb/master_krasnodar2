module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      },
      // Прокси для FastAPI, чтобы избегать PNA/CORS при разработке
      '^/send-order': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
};

const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
