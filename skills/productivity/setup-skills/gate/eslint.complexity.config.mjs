// Cyclomatic complexity, the gate's own bar. Lives beside the gate's
// node_modules: this is an ESM module and its imports resolve from its own
// directory, not from the project's.
import tsParser from "@typescript-eslint/parser";

export default [
  { ignores: [".agents/**"] },
  {
    files: ["**/*.{js,mjs,cjs,jsx,ts,mts,cts,tsx}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
    },
    rules: { complexity: ["error", { max: 10 }] },
  },
];
