/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.html', './node_modules/flowbite/**/*.js', './node_modules/tw-elements/dist/js/**/*.js'],
    theme: {
        extend: {},
        colors: {
            'primary': {
                50: '#f5f3ff',
                100: '#ede9fe',
                200: '#ddd6fe',
                300: '#d8b4fe',
                400: '#a78bfa',
                500: '#8b5cf6',
                600: '#7c3aed',
                700: '#6d28d9',
                800: '#5b21b6',
                900: '#4c1d95',
            }
        },
    },
    plugins: [
        require('flowbite/plugin'),
        require('tw-elements/dist/plugin')
    ],
}

// 'primary': {
//   100: '#fecfcf',
//   200: '#fca5a5',
//   300: '#f96767',
//   400: '#ee2222',
//   500: '#d40606',
//   600: '#b20808',
//   700: '#900e0e',
//   800: '#751515',
//   900: '#631616',
// },
