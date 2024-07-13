module.exports = {
    // ... other configurations
    resolve: {
      fallback: {
        "url": require.resolve("url/"),
        "buffer": require.resolve("buffer/"),
        "stream": require.resolve("stream-browserify"),
        "util": require.resolve("util/"),
        "crypto": require.resolve("crypto-browserify"),
        "assert": require.resolve("assert/"),
        "http": require.resolve("stream-http"),
        "https": require.resolve("https-browserify"),
        "os": require.resolve("os-browserify/browser"),
        "path": require.resolve("path-browserify"),
        "tty": require.resolve("tty-browserify"),
        "zlib": require.resolve("browserify-zlib")
      }
    }
  };
  
