/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.html', './node_modules/flowbite/**/*.js', './node_modules/tw-elements/dist/js/**/*.js'],
  theme: {
    extend: {},
    colors: {
      'primary': {
        100: '#fecfcf',
        200: '#fca5a5',
        300: '#f96767',
        400: '#ee2222',
        500: '#d40606',
        600: '#b20808',
        700: '#900e0e',
        800: '#751515',
        900: '#631616',
      },
    },
  },
  plugins: [
      require('flowbite/plugin'),
      require('tw-elements/dist/plugin')
  ],

}