// @vitest-environment nuxt
import { it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createI18n } from 'vue-i18n'
import { BcrosTypographyH2 } from '#components'

const i18n = createI18n({
  // vue-i18n options here ...
})

it('can mount h2 component', async () => {
  const text = 'Test Text'
  const cssClass = 'TestClass'
  const typography = await mountSuspended(BcrosTypographyH2,
    {
      global: {
        plugins: [i18n]
      },
      props: {
        text
      },
      attrs: {
        class: cssClass
      }
    })
  expect(typography.find('[data-test-id="h2"]').exists()).toBe(true)
  expect(typography.text()).toContain(text)
  expect(typography.classes()).toContain(cssClass)
})
