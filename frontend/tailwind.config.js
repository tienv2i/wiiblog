module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      transitionProperty: {
        'height': 'max-height'
      }
    },
  },
  variants: {
    extend: {
      borderWidth: ['last', 'first'],
    },
  },
  plugins: [],
}
