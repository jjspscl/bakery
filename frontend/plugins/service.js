// import _ from 'lodash'
// const FALLBACK_INTERVAL = 30 * 60 * 1000

export default function (ctx) {
  async function update () {
    while (true) {
      await new Promise(resolve => setTimeout(resolve, 27 * 1000))
      // .then(() => return !done})
      ctx.$store.dispatch('pastry/GetIngredients', ctx)
    }
  }
  update()
}
