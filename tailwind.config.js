/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
  corePlugins: {
    preflight: false, // disable preflight to avoid conflicting with Docusaurus styles
  },
  blocklist: ['container'], // prevent conflict with Docusaurus container
}
