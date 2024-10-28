module.exports = {
  apps: [
    {
      name: 'FlaskApp',
      script: 'flask',
      args: '--app backend/rag_api.py run --host=0.0.0.0 --port=5000',
      interpreter: 'python3',
    },
    {
      name: 'ExpressServer',
      script: 'server/server.js',
      args: '',
      interpreter: 'node',
    },
    {
      name: 'ReactClient',
      script: 'npx',
      args: 'serve -s client/build -l 3000',
    },
  ],
};
