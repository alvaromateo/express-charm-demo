import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 3010,
  },
  plugins: [react()],
  /*
  build: {
    // treat this as a library / single-entry server bundle
    lib: {
      entry: path.resolve(__dirname, 'src/server-entry.js'), // change to your entry
      formats: ['cjs'], // produce CommonJS for Node
      fileName: () => 'output' // -> dist/output.cjs (or .js depending on node)
    },

    // disable default minifier if you want readable output (optional)
    minify: false,

    rollupOptions: {
      // Do NOT mark deps as external: default is to externalize some things,
      // so we explicitly set `external` to an empty array or only node builtins.
      external: (id) => {
        // keep Node builtins external (fs, path, etc.), but include everything else:
        const builtins = ['fs','path','os','stream','crypto','util','http','https','zlib'];
        if (builtins.includes(id.split('/')[0])) return true;
        return false; // include everything else (node_modules)
      },
      plugins: [
        // resolve node_modules (including exports fields), and convert CJS -> ESM so Rollup can bundle.
        nodeResolve({ preferBuiltins: true, exportConditions: ['node'] }),
        commonjs()
      ],
      output: {
        // ensure CommonJS export style
        exports: 'auto'
      }
    },

    // target Node — adjust to the Node version you run
    target: 'node18' // or node16/node20, etc.
  }
  */
});
