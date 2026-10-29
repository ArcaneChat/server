import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        privacy: resolve(__dirname, "privacy.html"),
        imprint: resolve(__dirname, "imprint.html"),
        channels: resolve(__dirname, "channels.html"),
      },
    },
  },
});
