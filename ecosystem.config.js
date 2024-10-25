module.exports = {
    apps: [
      {
        name: "server",
        script: "/app/server/server.js",
        interpreter: "node",
        watch: true,
      },
      {
        name: "backend",
        script: "/app/backend/rag_api.py",
        interpreter: "python3",
        watch: true,
      },
    ],
  };
  